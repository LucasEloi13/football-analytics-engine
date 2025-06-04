# Configuração do Terraform e Provider AWS
terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.11"
    }
  }
}

# Configuração do Provider AWS
provider "aws" {
  region = var.aws_region
}

# Data source para obter ID da conta AWS atual
data "aws_caller_identity" "current" {}

# Data source para obter região atual
data "aws_region" "current" {}