locals{
    tags = {
        Name = "football-tracker-project"
        Environment = "Dev"
        Managedby = "Terraform"
    }

    lambda_functions = {
        extract_competition_details = {
            function_name = "futebol_tracker_extract_competition_details_lambda"
            handler       = "lambda_function.lambda_handler"
            filename      = "${path.module}/lambdas/extract_competition_details_lambda/payload_files.zip"
        }
        extract_match_details = {
            function_name = "futebol_tracker_extract_matches_lambda"
            handler       = "lambda_function.lambda_handler"
            filename      = "${path.module}/lambdas/extract_matches_ambda/payload_files.zip"
        }
        extract_team_details = {
            function_name = "futebol_tracker_extract_teams_lambda"
            handler       = "lambda_function.lambda_handler"
            filename      = "${path.module}/lambdas/extract_teams_lambda/payload_files.zip"
        }
        extract_standings_details = {
            function_name = "futebol_tracker_extract_standings_lambda"
            handler       = "lambda_function.lambda_handler"
            filename      = "${path.module}/lambdas/extract_standings_lambda/payload_files.zip"
        }
    }
}