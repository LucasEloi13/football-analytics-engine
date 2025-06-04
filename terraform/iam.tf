# Role básica para execução das Lambdas
data "aws_iam_policy_document" "lambda_assume_role" {
  statement {
    effect = "Allow"
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
    actions = ["sts:AssumeRole"]
  }
}

# Role IAM para Lambdas de Extração
resource "aws_iam_role" "lambda_extraction_role" {
  name               = "${var.project_name}-lambda-extraction-role"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json

  tags = merge(var.common_tags, {
    Name = "${var.project_name}-lambda-extraction-role"
    Type = "IAMRole"
  })
}

# Role IAM para Lambdas de Transformação
resource "aws_iam_role" "lambda_transformation_role" {
  name               = "${var.project_name}-lambda-transformation-role"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json

  tags = merge(var.common_tags, {
    Name = "${var.project_name}-lambda-transformation-role"
    Type = "IAMRole"
  })
}

# Policy para acesso básico de execução Lambda
resource "aws_iam_role_policy_attachment" "lambda_extraction_basic_execution" {
  role       = aws_iam_role.lambda_extraction_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy_attachment" "lambda_transformation_basic_execution" {
  role       = aws_iam_role.lambda_transformation_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Policy para Lambdas de Extração (apenas write no S3 raw data)
data "aws_iam_policy_document" "lambda_extraction_s3_policy" {
  statement {
    effect = "Allow"
    actions = [
      "s3:PutObject",
      "s3:PutObjectAcl",
      "s3:GetObjectVersion"
    ]
    resources = [
      "${aws_s3_bucket.raw_data.arn}/*"
    ]
  }

  statement {
    effect = "Allow"
    actions = [
      "s3:ListBucket",
      "s3:GetBucketLocation"
    ]
    resources = [
      aws_s3_bucket.raw_data.arn
    ]
  }
}

resource "aws_iam_policy" "lambda_extraction_s3_policy" {
  name        = "${var.project_name}-lambda-extraction-s3-policy"
  description = "Policy para permitir que Lambdas de extração escrevam no bucket de dados brutos"
  policy      = data.aws_iam_policy_document.lambda_extraction_s3_policy.json

  tags = merge(var.common_tags, {
    Name = "${var.project_name}-lambda-extraction-s3-policy"
    Type = "IAMPolicy"
  })
}

# Policy para Lambdas de Transformação (read do raw data, write no processed data)
data "aws_iam_policy_document" "lambda_transformation_s3_policy" {
  statement {
    effect = "Allow"
    actions = [
      "s3:GetObject",
      "s3:GetObjectVersion"
    ]
    resources = [
      "${aws_s3_bucket.raw_data.arn}/*"
    ]
  }

  statement {
    effect = "Allow"
    actions = [
      "s3:PutObject",
      "s3:PutObjectAcl",
      "s3:GetObjectVersion"
    ]
    resources = [
      "${aws_s3_bucket.processed_data.arn}/*"
    ]
  }

  statement {
    effect = "Allow"
    actions = [
      "s3:ListBucket",
      "s3:GetBucketLocation"
    ]
    resources = [
      aws_s3_bucket.raw_data.arn,
      aws_s3_bucket.processed_data.arn
    ]
  }
}

resource "aws_iam_policy" "lambda_transformation_s3_policy" {
  name        = "${var.project_name}-lambda-transformation-s3-policy"
  description = "Policy para permitir que Lambdas de transformação leiam dados brutos e escrevam dados processados"
  policy      = data.aws_iam_policy_document.lambda_transformation_s3_policy.json

  tags = merge(var.common_tags, {
    Name = "${var.project_name}-lambda-transformation-s3-policy"
    Type = "IAMPolicy"
  })
}

# Anexar policies aos roles
resource "aws_iam_role_policy_attachment" "lambda_extraction_s3" {
  role       = aws_iam_role.lambda_extraction_role.name
  policy_arn = aws_iam_policy.lambda_extraction_s3_policy.arn
}

resource "aws_iam_role_policy_attachment" "lambda_transformation_s3" {
  role       = aws_iam_role.lambda_transformation_role.name
  policy_arn = aws_iam_policy.lambda_transformation_s3_policy.arn
}

# Policy adicional para CloudWatch Logs (caso necessário logs customizados)
data "aws_iam_policy_document" "lambda_cloudwatch_logs_policy" {
  statement {
    effect = "Allow"
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
      "logs:DescribeLogStreams",
      "logs:DescribeLogGroups"
    ]
    resources = [
      "arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:log-group:/aws/lambda/${var.project_name}-*"
    ]
  }
}

resource "aws_iam_policy" "lambda_cloudwatch_logs_policy" {
  name        = "${var.project_name}-lambda-cloudwatch-logs-policy"
  description = "Policy para permitir que Lambdas escrevam logs no CloudWatch"
  policy      = data.aws_iam_policy_document.lambda_cloudwatch_logs_policy.json

  tags = merge(var.common_tags, {
    Name = "${var.project_name}-lambda-cloudwatch-logs-policy"
    Type = "IAMPolicy"
  })
}

# Anexar policy de CloudWatch aos roles
resource "aws_iam_role_policy_attachment" "lambda_extraction_cloudwatch" {
  role       = aws_iam_role.lambda_extraction_role.name
  policy_arn = aws_iam_policy.lambda_cloudwatch_logs_policy.arn
}

resource "aws_iam_role_policy_attachment" "lambda_transformation_cloudwatch" {
  role       = aws_iam_role.lambda_transformation_role.name
  policy_arn = aws_iam_policy.lambda_cloudwatch_logs_policy.arn
}

# Policy para permitir que Lambdas acessem a Layer
data "aws_iam_policy_document" "lambda_layer_policy" {
  statement {
    effect = "Allow"
    actions = [
      "lambda:GetLayerVersion"
    ]
    resources = [
      "arn:aws:lambda:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:layer:${var.project_name}-*"
    ]
  }
}

resource "aws_iam_policy" "lambda_layer_policy" {
  name        = "${var.project_name}-lambda-layer-policy"
  description = "Policy para permitir que Lambdas acessem as layers"
  policy      = data.aws_iam_policy_document.lambda_layer_policy.json

  tags = merge(var.common_tags, {
    Name = "${var.project_name}-lambda-layer-policy"
    Type = "IAMPolicy"
  })
}

# Anexar policy de Layer aos roles
resource "aws_iam_role_policy_attachment" "lambda_extraction_layer" {
  role       = aws_iam_role.lambda_extraction_role.name
  policy_arn = aws_iam_policy.lambda_layer_policy.arn
}

resource "aws_iam_role_policy_attachment" "lambda_transformation_layer" {
  role       = aws_iam_role.lambda_transformation_role.name
  policy_arn = aws_iam_policy.lambda_layer_policy.arn
}