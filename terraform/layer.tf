# Lambda Layer para pacotes Python compartilhados
resource "aws_lambda_layer_version" "python_dependencies" {
  filename                 = var.python_layer_zip_path
  layer_name              = "${var.project_name}-python-dependencies"
  description             = "Layer com dependências Python compartilhadas para ETL"
  compatible_runtimes     = [var.lambda_runtime]
  compatible_architectures = ["x86_64"]

  # Gerar hash do arquivo para detectar mudanças
  source_code_hash = fileexists(var.python_layer_zip_path) ? filebase64sha256(var.python_layer_zip_path) : null

  tags = merge(var.common_tags, {
    Name = "${var.project_name}-python-dependencies-layer"
    Type = "LambdaLayer"
  })

  lifecycle {
    ignore_changes = [
      filename,
      source_code_hash
    ]
  }
}

# Lambda Layer para utilitários de ETL compartilhados
resource "aws_lambda_layer_version" "etl_utilities" {
  filename                 = var.etl_utilities_layer_zip_path
  layer_name              = "${var.project_name}-etl-utilities"
  description             = "Layer com utilitários de ETL compartilhados"
  compatible_runtimes     = [var.lambda_runtime]
  compatible_architectures = ["x86_64"]

  # Gerar hash do arquivo para detectar mudanças
  source_code_hash = fileexists(var.etl_utilities_layer_zip_path) ? filebase64sha256(var.etl_utilities_layer_zip_path) : null

  tags = merge(var.common_tags, {
    Name = "${var.project_name}-etl-utilities-layer"
    Type = "LambdaLayer"
  })

  lifecycle {
    ignore_changes = [
      filename,
      source_code_hash
    ]
  }
}

# Grupo de logs CloudWatch para monitorar as layers
resource "aws_cloudwatch_log_group" "lambda_layers_logs" {
  name              = "/aws/lambda/layers/${var.project_name}"
  retention_in_days = 14

  tags = merge(var.common_tags, {
    Name = "${var.project_name}-lambda-layers-logs"
    Type = "CloudWatchLogGroup"
  })
}

# Variáveis locais para referenciar as layers
locals {
  common_layers = [
    aws_lambda_layer_version.python_dependencies.arn,
    aws_lambda_layer_version.etl_utilities.arn
  ]
}