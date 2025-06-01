variable "aws_region" {
    description = "The AWS region to deploy resources in"
    default     = "us-east-2"
}

variable "bucket" {
    description = "The name of the S3 bucket to create"
}

provider "aws" {
    region = var.aws_region
}

resource "aws_s3_bucket" "futebol-tracker-bucket" {
    bucket = var.bucket

    tags = {
        Name        = "Futebol Tracker Bucket"
        Environment = "Development"
    }
}