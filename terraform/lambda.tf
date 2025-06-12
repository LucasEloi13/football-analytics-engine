# resource "aws_lambda_layer_version" "futebol_tracker_lambda_layer" {
#   filename   = "${path.module}/layers/python.zip"
#   layer_name = "futebol_tracker_lambda_layer"
#   compatible_runtimes = ["python3.9", "python3.10", "python3.11"]
#   source_code_hash = filebase64sha256("${path.module}/layers/python.zip")
# }

resource "aws_lambda_layer_version" "futebol_tracker_lambda_layer1" {
  s3_bucket = aws_s3_bucket.football_tracker_datalake.bucket
  s3_key    = aws_s3_object.layer1-file.key
  layer_name = "futebol_tracker_lambda_layer1"
  compatible_runtimes = ["python3.11"]

  depends_on = [
    aws_s3_bucket.football_tracker_datalake,
    aws_s3_object.layer1-file,
    aws_iam_role.lambda_role
  ]

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_lambda_layer_version" "futebol_tracker_lambda_layer2" {
  s3_bucket = aws_s3_bucket.football_tracker_datalake.bucket
  s3_key    = aws_s3_object.layer2-file.key
  layer_name = "futebol_tracker_lambda_layer2"
  compatible_runtimes = ["python3.11"]

  depends_on = [
    aws_s3_bucket.football_tracker_datalake,
    aws_s3_object.layer2-file,
    aws_iam_role.lambda_role,
    aws_lambda_layer_version.futebol_tracker_lambda_layer1
  ]

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_lambda_function" "futebol_tracker_extractores_lambda" {
  function_name = "futebol_tracker_extractores_lambda"
  role          = aws_iam_role.lambda_role.arn
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.11"
  filename      = "${path.module}/lambdas/extract_competition_details_lambda/payload_files.zip"
  source_code_hash = filebase64sha256("${path.module}/lambdas/extract_competition_details_lambda/payload_files.zip")
  layers        = [
    aws_lambda_layer_version.futebol_tracker_lambda_layer1.arn, 
    aws_lambda_layer_version.futebol_tracker_lambda_layer2.arn
  ]

  environment {
    variables = {
      BUCKET_NAME = var.bucket_name
      S3_BUCKET_NAME = var.bucket_name
    }
  }

  tags = local.tags
  
  depends_on = [
    aws_iam_role.lambda_role,
    aws_iam_role_policy_attachment.lambda_policy_attach,
    aws_iam_role_policy_attachment.lambda_cloudwatch_policy_attach,
    aws_lambda_layer_version.futebol_tracker_lambda_layer1,
    aws_lambda_layer_version.futebol_tracker_lambda_layer2
  ]

  lifecycle {
    create_before_destroy = true
    
    precondition {
      condition     = fileexists("${path.module}/lambdas/extract_competition_details_lambda/payload_files.zip")
      error_message = "O arquivo payload_files.zip não existe. A função Lambda não pode ser criada."
    }
  }
}