data "archive_file" "football-extract-competitions_artefact" {
    type = "zip"
    source_file = "${path.module}/lambda/football-extract-competitions.py"
    output_path = "${path.module}/lambda/football-extract-competitions.zip"
  
}

resource "aws_lambda_function" "football-extract-competitions" {
    function_name = "football-extract-competitions"
    handler = "lambda_function.lambda_handler"
    role = aws_iam_role.football-api-role.arn
    runtime = "python3.11"    
}