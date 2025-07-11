resource "aws_lambda_layer_version" "minimal_dependencies_layer" {
    s3_bucket = aws_s3_bucket.football_tracker_datalake.bucket
    s3_key    = aws_s3_object.minimal_layer_file.key
    layer_name = "minimal_dependencies_layer"
    compatible_runtimes = ["python3.11"]

    depends_on = [
        aws_s3_bucket.football_tracker_datalake,
        aws_s3_object.minimal_layer_file
    ]

    lifecycle {
        create_before_destroy = true
    }
}
# Usar esse resource como base para criar as 4 funções Lambdas de extração
# 1. Extract competition details
# 2. Extract match details
# 3. Extract team details
# 4. Extract Standings details

resource "aws_lambda_function" "football_tracker_extractors" {
  for_each = local.lambda_functions

  function_name = each.value.function_name
  role          = aws_iam_role.lambda_role.arn
  handler       = each.value.handler
  runtime       = "python3.11"
  filename      = each.value.filename
  source_code_hash = filebase64sha256(each.value.filename)
  
  timeout       = 30 
  memory_size   = 128

  layers = [
    aws_lambda_layer_version.minimal_dependencies_layer.arn
  ]

  environment {
    variables = {
      BUCKET_NAME = var.bucket_name
    }
  }

  tags = local.tags
  
  depends_on = [
    aws_iam_role.lambda_role,
    aws_iam_role_policy_attachment.lambda_policy_attach,
    aws_iam_role_policy_attachment.lambda_cloudwatch_policy_attach,
    aws_lambda_layer_version.minimal_dependencies_layer
  ]
}

# resource "aws_lambda_function" "futebol_tracker_extractors_lambda" {
#   function_name = "futebol_tracker_extractores_lambda"
#   role          = aws_iam_role.lambda_role.arn
#   handler       = "lambda_function.lambda_handler"
#   runtime       = "python3.11"
#   filename      = "${path.module}/lambdas/extract_competition_details_lambda/payload_files.zip"
#   source_code_hash = filebase64sha256("${path.module}/lambdas/extract_competition_details_lambda/payload_files.zip")
  
#   # Aumentar timeout e memória
#   timeout = 30  
#   memory_size = 256
  
#   layers = [
#     aws_lambda_layer_version.minimal_dependencies_layer.arn
#   ]

#   environment {
#     variables = {
#       BUCKET_NAME = var.bucket_name
#     }
#   }

#   tags = local.tags
  
#   depends_on = [
#     aws_iam_role.lambda_role,
#     aws_iam_role_policy_attachment.lambda_policy_attach,
#     aws_iam_role_policy_attachment.lambda_cloudwatch_policy_attach,
#     aws_lambda_layer_version.minimal_dependencies_layer
#   ]

#   lifecycle {
#     create_before_destroy = true
    
#     precondition {
#       condition     = fileexists("${path.module}/lambdas/extract_competition_details_lambda/payload_files.zip")
#       error_message = "O arquivo payload_files.zip não existe. A função Lambda não pode ser criada."
#     }
#   }
# }