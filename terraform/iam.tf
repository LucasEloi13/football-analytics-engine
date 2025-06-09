data "aws_iam_policy_document" "lambda_assume_role_policy" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "lambda_role" {
  name = "lambda-lambdaRole-waf"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role_policy.json
}

data "aws_iam_policy_document" "lambda_access_s3" {
  statement {
    effect  = "Allow"
    actions = [
        "s3:PutObject",
        "s3:GetObject",
        "s3:ListBucket",
        "s3:CreateBucket",
        "s3:DeleteObject"
    ]
    resources = [
        "arn:aws:s3:::${var.bucket_name}",
        "arn:aws:s3:::${var.bucket_name}/*"
    ]
  }
}

resource "aws_iam_policy" "lambda_access_s3" {
  name   = "lambda_access_s3"
  policy = data.aws_iam_policy_document.lambda_access_s3.json
}

data "aws_iam_policy_document" "lambda_access_cloudwatch" {
  statement {
    effect  = "Allow"
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]
    resources = ["arn:aws:logs:*:*:*"]
  }
}

resource "aws_iam_policy" "lambda_access_cloudwatch" {
  name   = "lambda_access_cloudwatch"
  policy = data.aws_iam_policy_document.lambda_access_cloudwatch.json
}

resource "aws_iam_role_policy_attachment" "lambda_policy_attach" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.lambda_access_s3.arn
}

resource "aws_iam_role_policy_attachment" "lambda_cloudwatch_policy_attach" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.lambda_access_cloudwatch.arn
}