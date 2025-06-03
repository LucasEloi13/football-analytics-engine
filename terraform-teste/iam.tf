data "aws_iam_policy_document" "football_api_policy" {
    statement {
        actions = [
            "sts:AssumeRole"
        ]
        
        principals {
            type        = "Service"
            identifiers = ["lambda.amazonaws.com"]
        }
    }
}  


resource "aws_iam_role" "football-api-role" {
    name                  = "football-api-role"
    assume_role_policy    = data.aws_iam_policy_document.football_api_policy.json

    tags = local.common_tags

}

