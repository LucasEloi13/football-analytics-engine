resource "aws_s3_bucket" "football_tracker_datalake"{
    bucket = var.bucket_name
    tags=local.tags
}

resource "aws_s3_object" "layer1-file" {
    bucket = aws_s3_bucket.football_tracker_datalake.bucket
    key    = "dependencies/aws_dependencies/python.zip"
    source = "${path.module}/layers/aws_dependencies/python.zip"
    etag   = filemd5("${path.module}/layers/aws_dependencies/python.zip")
    tags   = local.tags
    
    depends_on = [aws_s3_bucket.football_tracker_datalake]

    lifecycle {
        precondition {
            condition     = fileexists("${path.module}/layers/aws_dependencies/python.zip")
            error_message = "Arquivo aws_dependencies/python.zip não encontrado. Execute o script de criação dos layers primeiro."
        }
    }
}

resource "aws_s3_object" "layer2-file" {
    bucket = aws_s3_bucket.football_tracker_datalake.bucket
    key    = "dependencies/data_processing_dependencies/python.zip"
    source = "${path.module}/layers/data_processing_dependencies/python.zip"
    etag   = filemd5("${path.module}/layers/data_processing_dependencies/python.zip")
    tags   = local.tags
    
    depends_on = [
        aws_s3_bucket.football_tracker_datalake,
        aws_s3_object.layer1-file
    ]

    lifecycle {
        precondition {
            condition     = fileexists("${path.module}/layers/data_processing_dependencies/python.zip")
            error_message = "Arquivo data_processing_dependencies/python.zip não encontrado. Execute o script de criação dos layers primeiro."
        }
    }
}