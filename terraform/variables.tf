variable "aws_region" {
  description = "Região da AWS"
  type        = string
}

variable "s3_bucket_name" {
  description = "Nome do bucket S3"
  type        = string
}

variable "lambda_function_name" {
  description = "Nome da função Lambda"
  type        = string
}

variable "lambda_handler" {
  description = "Handler da função Lambda (arquivo.handler)"
  type        = string
}

variable "lambda_runtime" {
  description = "Runtime da Lambda (e.g., python3.11)"
  type        = string
}

variable "lambda_role_name" {
  description = "Nome da Role para a Lambda"
  type        = string
}
