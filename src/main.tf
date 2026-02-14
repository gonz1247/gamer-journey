# Specify region
provider "aws" {
  region = "us-west-2"
}

# Setup VPC to host everything within
resource "aws_vpc" "default" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = {
    Name = "GamerJourneyVPC"
  }
}

# Setup internet gateway so the VPC can access internet 
resource "aws_internet_gateway" "default" {
  vpc_id = aws_vpc.default.id
  tags = {
    Name = "GamerJourneyInternetGateway"
  }
}

# Manage routing of requests leaving the VPC
resource "aws_route_table" "default" {
  vpc_id = aws_vpc.default.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.default.id
  }
  tags = {
    Name = "GamerJourneyRouteTable"
  }
}

# Create subnets
resource "aws_subnet" "subnet1" {
  vpc_id                  = aws_vpc.default.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = false
  availability_zone       = "us-west-2a"
  tags = {
    Name = "GamerJourneySubnet1"
  }
}
resource "aws_subnet" "subnet2" {
  vpc_id                  = aws_vpc.default.id
  cidr_block              = "10.0.2.0/24"
  map_public_ip_on_launch = false
  availability_zone       = "us-west-2b"
  tags = {
    Name = "GamerJourneySubnet2"
  }
}

# Associate route table with subnets
resource "aws_route_table_association" "a" {
  subnet_id      = aws_subnet.subnet1.id
  route_table_id = aws_route_table.default.id
}
resource "aws_route_table_association" "b" {
  subnet_id      = aws_subnet.subnet2.id
  route_table_id = aws_route_table.default.id
}

# Security group for EC2 instance
resource "aws_security_group" "default" {
  vpc_id = aws_vpc.default.id
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  tags = {
    Name = "GamerJourneySecurityGroup"
  }
}

resource "aws_security_group" "ssh" {
  vpc_id = aws_vpc.default.id
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  tags = {
    Name = "GamerJourneySSH"
  }
}

# Create SECRET_KEY variable for Django
variable "secret_key" {
  description = "Django secret key"
  type        = string
  sensitive   = true
}

# EC2 instance to host the Django application
resource "aws_instance" "default" {
  ami                         = "ami-0320940581663281e"
  instance_type               = "t3.micro"
  subnet_id                   = aws_subnet.subnet1.id
  vpc_security_group_ids      = [aws_security_group.default.id, aws_security_group.ssh.id]
  associate_public_ip_address = true
  user_data_replace_on_change = true
  iam_instance_profile        = aws_iam_instance_profile.ec2_profile.name
  user_data                   = <<-EOF
              #!/bin/bash
              set -ex 
              dnf update -y
              dnf install -y dnf-plugins-core

              # Install Docker
              dnf install -y docker
              service docker start
              
              # Install AWS CLI
              dnf install -y awscli 

              # Login to ECR and pull the Docker image
              docker login -u AWS -p $(aws ecr get-login-password --region us-west-2) 251622685697.dkr.ecr.us-west-2.amazonaws.com/gamer_journey
              docker pull 251622685697.dkr.ecr.us-west-2.amazonaws.com/gamer_journey:latest

              # Run the Docker container
              docker run -d -p 80:8080 \
              --env DEBUG=False \
              --env SECRET_KEY='${var.secret_key}' \
              --env DB_NAME='${aws_db_instance.default.db_name}' \
              --env DB_USER='${aws_db_instance.default.username}' \
              --env DB_PW='${aws_db_instance.default.password}' \
              --env DB_HOST='${aws_db_instance.default.endpoint}' \
              251622685697.dkr.ecr.us-west-2.amazonaws.com/gamer_journey:latest
              EOF
  tags = {
    Name = "GamerJourneyServer"
  }
}

# IAM role for EC2 instance to access ECR
resource "aws_iam_role" "ec2_role" {
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
        Effect = "Allow"
      }
    ]
  })
}
# Attach policy to role
resource "aws_iam_role_policy_attachment" "ecr_readonly" {
  role       = aws_iam_role.ec2_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
}
# IAM instance profile to attach role to EC2 instance
resource "aws_iam_instance_profile" "ec2_profile" {
  name = "GamerJourneyProfile"
  role = aws_iam_role.ec2_role.name
}
