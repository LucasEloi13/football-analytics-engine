# Funções Lambda para Extração de Dados
resource "aws_lambda_function" "extraction_lambdas" {
  for_each = var.extraction_lambdas

  function_name = "${var.project_name}-${each.value.name}"
  description   = each.value.description
  role         = aws_iam_role.lambda_extraction_role.arn
  handler      = each.value.handler
  runtime      = var.lambda_runtime
  timeout      = var.lambda_timeout
  memory_size  = var.lambda_memory_size

  # Configuração do arquivo ZIP
  filename         = each.value.zip_path
  source_code_hash = fileexists(each.value.zip_path) ? filebase64sha256(each.value.zip_path) : null

  # Layers compartilhadas
  layers = local.common_layers

  # Variáveis de ambiente
  environment {
    variables = {
      ENVIRONMENT           = var.environment
      RAW_DATA_BUCKET      = aws_s3_bucket.raw_data.bucket
      PROCESSED_DATA_BUCKET = aws_s3_bucket.processed_data.bucket
      AWS_DEFAULT_REGION   = var.aws_region
      LOG_LEVEL           = "INFO"
    }
  }

  # Configuração de VPC (se necessário)
  # vpc_config {
  #   subnet_ids         = var.subnet_ids
  #   security_group_ids = var.security_group_ids
  # }

  tags = merge(var.common_tags, {
    Name     = "${var.project_name}-${each.value.name}"
    Type     = "LambdaFunction"
    Category = "Extraction"
  })

  # Evitar recriação desnecessária
  lifecycle {
    ignore_changes = [
      filename,
      source_code_hash
    ]
  }

  depends_on = [
    aws_iam_role_policy_attachment.lambda_extraction_basic_execution,
    aws_iam_role_policy_attachment.lambda_extraction_s3,
    aws_cloudwatch_log_group.extraction_lambda_logs
  ]
}

# Funções Lambda para Transformação de Dados
resource "aws_lambda_function" "transformation_lambdas" {
  for_each = var.transformation_lambdas

  function_name = "${var.project_name}-${each.value.name}"
  description   = each.value.description
  role         = aws_iam_role.lambda_transformation_role.arn
  handler      = each.value.handler
  runtime      = var.lambda_runtime
  timeout      = var.lambda_timeout
  memory_size  = var.lambda_memory_size

  # Configuração do arquivo ZIP
  filename         = each.value.zip_path
  source_code_hash = fileexists(each.value.zip_path) ? filebase64sha256(each.value.zip_path) : null

  # Layers compartilhadas
  layers = local.common_layers

  # Variáveis de ambiente
  environment {
    variables = {
      ENVIRONMENT           = var.environment
      RAW_DATA_BUCKET      = aws_s3_bucket.raw_data.bucket
      PROCESSED_DATA_BUCKET = aws_s3_bucket.processed_data.bucket
      AWS_DEFAULT_REGION   = var.aws_region
      LOG_LEVEL           = "INFO"
    }
  }

  # Configuração de VPC (se necessário)
  # vpc_config {
  #   subnet_ids         = var.subnet_ids
  #   security_group_ids = var.security_group_ids
  # }

  tags = merge(var.common_tags, {
    Name     = "${var.project_name}-${each.value.name}"
    Type     = "LambdaFunction"
    Category = "Transformation"
  })

  # Evitar recriação desnecessária
  lifecycle {
    ignore_changes = [
      filename,
      source_code_hash
    ]
  }

  depends_on = [
    aws_iam_role_policy_attachment.lambda_transformation_basic_execution,
    aws_iam_role_policy_attachment.lambda_transformation_s3,
    aws_cloudwatch_log_group.transformation_lambda_logs
  ]
}

# CloudWatch Log Groups para Lambdas de Extração
resource "aws_cloudwatch_log_group" "extraction_lambda_logs" {
  for_each = var.extraction_lambdas

  name              = "/aws/lambda/${var.project_name}-${each.value.name}"
  retention_in_days = 14

  tags = merge(var.common_tags, {
    Name     = "${var.project_name}-${each.value.name}-logs"
    Type     = "CloudWatchLogGroup"
    Category = "Extraction"
  })
}

# CloudWatch Log Groups para Lambdas de Transformação
resource "aws_cloudwatch_log_group" "transformation_lambda_logs" {
  for_each = var.transformation_lambdas

  name              = "/aws/lambda/${var.project_name}-${each.value.name}"
  retention_in_days = 14

  tags = merge(var.common_tags, {
    Name     = "${var.project_name}-${each.value.name}-logs"
    Type     = "CloudWatchLogGroup"
    Category = "Transformation"
  })
}

# EventBridge Rules para agendar Lambdas de Extração (opcional)
resource "aws_cloudwatch_event_rule" "extraction_schedule" {
  for_each = var.extraction_lambdas

  name                = "${var.project_name}-${each.value.name}-schedule"
  description         = "Trigger para execução da lambda ${each.value.name}"
  schedule_expression = "rate(1 hour)" # Executar a cada hora - ajuste conforme necessário

  tags = merge(var.common_tags, {
    Name     = "${var.project_name}-${each.value.name}-schedule"
    Type     = "EventBridgeRule"
    Category = "Extraction"
  })
}

# Targets para as EventBridge Rules
resource "aws_cloudwatch_event_target" "extraction_lambda_target" {
  for_each = var.extraction_lambdas

  rule      = aws_cloudwatch_event_rule.extraction_schedule[each.key].name
  target_id = "Lambda${each.key}Target"
  arn       = aws_lambda_function.extraction_lambdas[each.key].arn
}

# Permissões para EventBridge invocar as Lambdas de Extração
resource "aws_lambda_permission" "allow_eventbridge_extraction" {
  for_each = var.extraction_lambdas

  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.extraction_lambdas[each.key].function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.extraction_schedule[each.key].arn
}

# S3 Event Notifications para trigger das Lambdas de Transformação
resource "aws_s3_bucket_notification" "raw_data_notification" {
  bucket = aws_s3_bucket.raw_data.id

  dynamic "lambda_function" {
    for_each = var.transformation_lambdas
    content {
      lambda_function_arn = aws_lambda_function.transformation_lambdas[lambda_function.key].arn
      events             = ["s3:ObjectCreated:*"]
      filter_prefix      = "data/${lambda_function.key}/"
      filter_suffix      = ".json"
    }
  }

  depends_on = [aws_lambda_permission.allow_s3_transformation]
}

# Permissões para S3 invocar as Lambdas de Transformação
resource "aws_lambda_permission" "allow_s3_transformation" {
  for_each = var.transformation_lambdas

  statement_id  = "AllowExecutionFromS3Bucket"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.transformation_lambdas[each.key].function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.raw_data.arn
}