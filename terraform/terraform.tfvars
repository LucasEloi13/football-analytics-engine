aws_region            = "us-east-2"            # <--- Altere a região
s3_bucket_name        = "futebol-tracker-bucket-728573093558"     # <--- Altere o nome do bucket
lambda_function_name  = "soccer-data-lambda"    # <--- Nome da função Lambda
lambda_handler        = "lambda_function.lambda_handler" # <--- Altere se mudar o arquivo/handler
lambda_runtime        = "python3.11"            # <--- Runtime desejado
lambda_role_name      = "lambda-s3-access-role" # <--- Nome da role IAM

