terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "6.15.0"
    }
  }
}

provider "aws" {
  # Configuration options
  region = "us-east-1"
}

variable "security-group-ports" {
  default = [22, 80, 443, 8080, 5432]
}

variable "instance-type" {
  default = "t2.micro"
  sensitive = true
}

resource "aws_security_group" "ports" {
  name = "ssh"
  description = "Allow inbound traffic on specified ports"

  dynamic "ingress" {
    for_each = var.security-group-ports
    content {
      from_port   = ingress.value
      to_port     = ingress.value
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

}


resource "aws_key_pair" "deployer" {
  key_name   = "projectkey"
  public_key = file("C:/Users/Hecti/AppData/Roaming/MobaXterm/home/.ssh/id_ed25519.pub")
}



#This role is typically attached to an EC2 instance (via an instance profile) 
#to allow the instance to interact with other AWS services on your behalf

# Only creates the trust relationship, not permissions
resource "aws_iam_role" "ec2_role" {
  name = "ec2_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com" #role is meant to be attached to an EC2 instance, to perform actions defined later
                                        # with aws_iam_role_policy
        }
      }
    ]
  })
  
}

resource "aws_iam_instance_profile" "ec2_profile" {
  name = "terraform-instance-profile"
  role = aws_iam_role.ec2_role.name
  
}

resource "aws_instance" "tf-ec2" {
    ami = "ami-08b5b3a93ed654d19"
    instance_type = var.instance-type
    key_name = "projectkey" #created it manualy
    vpc_security_group_ids = [aws_security_group.ports.id ]
    iam_instance_profile = aws_iam_instance_profile.ec2_profile.name
        tags = {
            Name = "Docker"
        }
        
    user_data = <<-EOF
        #!/bin/bash
        dnf update -y
        dnf install docker -y
        systemctl start docker
        systemctl enable docker
        usermod -a -G docker ec2-user
        curl -L "https://github.com/docker/compose/releases/download/1.27.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
        chmod +x /usr/local/bin/docker-compose
    EOF
}

output "ec2-public-ip" {
  value = aws_instance.tf-ec2.public_ip
}



resource "tls_private_key" "example" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "aws_key_pair" "generated" {
  key_name   = "generated-key"
  public_key = tls_private_key.example.public_key_openssh
}

output "private_key_pem" {
  value     = tls_private_key.example.private_key_pem
  sensitive = true
}