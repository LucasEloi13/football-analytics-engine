# Outputs dos Buckets S3
output "raw_data_bucket_name" {
  description = "Nome do bucket S3 para dados brutos"
  value       = aws_s3_bucket.raw_data.bucket
}

output "raw_data_bucket_arn" {
  description = "ARN do bucket S3 para dados brutos"
  value       = aws_s3_bucket.raw_data.arn
}

output "processed_data_bucket_name" {
  description = "Nome do bucket S3 para dados processados"
  value       = aws_s3_bucket.processed_data.bucket
}

output "processed_data_bucket_arn" {
  description = "ARN do bucket S3 para dados processados"
  value       = aws_s3_bucket.processed_data.arn
}

output "lambda_code_bucket_name" {
  description = "Nome do bucket S3 para código das lambdas"
  value       = aws_s3_bucket.lambda_code.bucket
}

# Outputs das Lambdas de Extração
output "extraction_lambda_function_names" {
  description = "Nomes das funções Lambda de extração"
  value = {
    for k, v in aws_lambda_function.extraction_lambdas : k => v.function_name
  }
}

output "extraction_lambda_function_arns" {
  description = "ARNs das funções Lambda de extração"
  value = {
    for k, v in aws_lambda_function.extraction_lambdas : k => v.arn
  }
}

output "extraction_lambda_invoke_arns" {
  description = "ARNs de invoke das funções Lambda de extração"
  value = {
    for k, v in aws_lambda_function.extraction_lambdas : k => v.invoke_arn
  }
}

# Outputs das Lambdas de Transformação
output "transformation_lambda_function_names" {
  description = "Nomes das funções Lambda de transformação"
  value = {
    for k, v in aws_lambda_function.transformation_lambdas : k => v.function_name
  }
}

output "transformation_lambda_function_arns" {
  description = "ARNs das funções Lambda de transformação"
  value = {
    for k, v in aws_lambda_function.transformation_lambdas : k => v.arn
  }
}

output "transformation_lambda_invoke_arns" {
  description = "ARNs de invoke das funções Lambda de transformação"
  value = {
    for k, v in aws_lambda_function.transformation_lambdas : k => v.invoke_arn
  }
}

# Outputs das Layers
output "python_dependencies_layer_arn" {
  description = "ARN da layer de dependências Python"
  value       = aws_lambda_layer_version.python_dependencies.arn
}

output "etl_utilities_layer_arn" {
  description = "ARN da layer de utilitários ETL"
  value       = aws_lambda_layer_version.etl_utilities.arn
}

# Outputs dos Roles IAM
output "lambda_extraction_role_arn" {
  description = "ARN do role IAM para lambdas de extração"
  value       = aws_iam_role.lambda_extraction_role.arn
}

output "lambda_transformation_role_arn" {
  description = "ARN do role IAM para lambdas de transformação"
  value       = aws_iam_role.lambda_transformation_role.arn
}

# Outputs das EventBridge Rules
output "extraction_schedule_rules" {
  description = "ARNs das regras de agendamento para extração"
  value = {
    for k, v in aws_cloudwatch_event_rule.extraction_schedule : k => v.arn
  }
}

# Outputs dos CloudWatch Log Groups
output "extraction_log_groups" {
  description = "ARNs dos grupos de logs das lambdas de extração"
  value = {
    for k, v in aws_cloudwatch_log_group.extraction_lambda_logs : k => v.arn
  }
}

output "transformation_log_groups" {
  description = "ARNs dos grupos de logs das lambdas de transformação"
  value = {
    for k, v in aws_cloudwatch_log_group.transformation_lambda_logs : k => v.arn
  }
}

# Output com informações de resumo do projeto
output "project_summary" {
  description = "Resumo da infraestrutura criada"
  value = {
    project_name          = var.project_name
    environment          = var.environment
    aws_region           = var.aws_region
    total_extraction_lambdas    = length(var.extraction_lambdas)
    total_transformation_lambdas = length(var.transformation_lambdas)
    lambda_runtime       = var.lambda_runtime
    lambda_memory_size   = var.lambda_memory_size
    lambda_timeout       = var.lambda_timeout
  }
}