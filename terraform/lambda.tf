resource "aws_lambda_layer_version" "futebol_tracker_lambda_layer" {
  filename   = "${path.module}/layers/python.zip"
  layer_name = "futebol_tracker_lambda_layer"
  compatible_runtimes = ["python3.9", "python3.10", "python3.11"]
  source_code_hash = filebase64sha256("${path.module}/layers/python.zip")
}

resource "aws_lambda_function" "futebol_tracker_extractores_lambda" {
  function_name = "futebol_tracker_extractores_lambda"
  role          = aws_iam_role.lambda_role.arn
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.11"
  filename      = "${path.module}/lambdas/extract_competition_details_lambda/payload_files.zip"
  source_code_hash = filebase64sha256("${path.module}/lambdas/extract_competition_details_lambda/payload_files.zip")
  layers        = [aws_lambda_layer_version.futebol_tracker_lambda_layer.arn]

  environment {
    variables = {
      BUCKET_NAME = var.bucket_name
    }
  }

  tags = local.tags
  
}