resource "aws_lambda_function" "football-extract-competitions" {
    function_name = "football-extract-competitions"
    handler = "lambda_function.lambda_handler"
    role = ""
    runtime = "python3.8"    
}