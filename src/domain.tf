# Get certificate for secure connections to domain 
resource "aws_acm_certificate" "cert" {
  domain_name               = "gamer-journey.com"
  validation_method         = "DNS"
  subject_alternative_names = ["www.gamer-journey.com"]

  tags = {
    Name = "GamerJourneyCertificate"
  }
  lifecycle {
    create_before_destroy = true
  }
}

# Route53 zone for domain
resource "aws_route53_zone" "main" {
  name = "gamer-journey.com"
}

# Define Route53 record for certificate validation
resource "aws_route53_record" "cert_validation" {
  for_each = {
    for dvo in aws_acm_certificate.cert.domain_validation_options : dvo.domain_name => {
      name   = dvo.resource_record_name
      record = dvo.resource_record_value
      type   = dvo.resource_record_type
    }
  }
  zone_id = aws_route53_zone.main.zone_id
  name    = each.value.name
  type    = each.value.type
  records = [each.value.record]
  ttl     = 60
}

# Define Route53 record for domain and www subdomain
resource "aws_route53_record" "root_record" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "gamer-journey.com"
  type    = "A"
  alias {
    name                   = aws_lb.default.dns_name
    zone_id                = aws_lb.default.zone_id
    evaluate_target_health = true
  }
}
resource "aws_route53_record" "www_record" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "www.gamer-journey.com"
  type    = "A"
  alias {
    name                   = aws_lb.default.dns_name
    zone_id                = aws_lb.default.zone_id
    evaluate_target_health = true
  }
}

# Define the certificate validation resource
resource "aws_acm_certificate_validation" "cert" {
  certificate_arn         = aws_acm_certificate.cert.arn
  validation_record_fqdns = [for record in aws_route53_record.cert_validation : record.fqdn]
}

# Setup security group for load balance 
resource "aws_security_group" "load_balancer" {
  vpc_id      = aws_vpc.default.id
  name        = "lb-https-security-group"
  description = "Allow inbound HTTPS traffic"

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Define load balancer 
resource "aws_lb" "default" {
  name               = "gamer-journey-lb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.load_balancer.id]
  # load balance needs two subnets despite server only being in subnet1
  subnets                    = [aws_subnet.subnet1.id, aws_subnet.subnet2.id]
  enable_deletion_protection = false
}

# Target group to route traffic to VPC
resource "aws_lb_target_group" "default" {
  name     = "gamer-journey-tg-https"
  port     = 443
  protocol = "HTTP"
  vpc_id   = aws_vpc.default.id
}
# Attach the EC2 instance to the target group (i.e., take traffic coming in at load balancer port 443 and send it to EC2 instance port 80)
resource "aws_lb_target_group_attachment" "default" {
  target_group_arn = aws_lb_target_group.default.arn
  target_id        = aws_instance.default.id
  port             = 80
}

# HTTPS listener for load balance 
resource "aws_lb_listener" "default" {
  load_balancer_arn = aws_lb.default.arn
  port              = "443"
  protocol          = "HTTPS"

  ssl_policy      = "ELBSecurityPolicy-2016-08"
  certificate_arn = aws_acm_certificate.cert.arn

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.default.arn
  }
}
