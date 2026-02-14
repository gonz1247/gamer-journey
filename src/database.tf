# Database subnet group (since database needs to be in more than 1 subnet)
resource "aws_db_subnet_group" "default" {
  name       = "django-db-subnet-group"
  subnet_ids = [aws_subnet.subnet1.id, aws_subnet.subnet2.id]
  tags = {
    Name = "GamerJourneyDBSubnetGroup"
  }
}

# Security group for RDS instance
resource "aws_security_group" "database" {
  name        = "django-rds-security-group"
  description = "Security group for Django RDS instance"
  vpc_id      = aws_vpc.default.id
  ingress {
    from_port   = 5432
    to_port     = 5432
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
    Name = "allow-game-journey-server-access"
  }
}

# RDS Variables 
variable "db_username" {
  description = "The username for the RDS instance"
  type        = string
  sensitive   = true
}
variable "db_password" {
  description = "The password for the RDS instance"
  type        = string
  sensitive   = true
}


# RDS instance
resource "aws_db_instance" "default" {
  allocated_storage      = 20
  storage_type           = "gp2"
  engine                 = "postgres"
  engine_version         = "17.6"
  instance_class         = "db.t3.micro"
  identifier             = "gamer-journey-db"
  db_name                = "gamerjourneydb"
  username               = var.db_username
  password               = var.db_password
  db_subnet_group_name   = aws_db_subnet_group.default.name
  vpc_security_group_ids = [aws_security_group.database.id]
  skip_final_snapshot    = true
  publicly_accessible    = true # use to allow setup of database from local machine temporarily
  multi_az               = false
  tags = {
    Name = "GamerJourneyRDS"
  }
}
