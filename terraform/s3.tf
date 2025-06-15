resource "aws_s3_bucket" "football_tracker_datalake"{
    bucket = var.bucket_name
    tags=local.tags
}

resource "aws_s3_object" "minimal_layer_file" {
    bucket = aws_s3_bucket.football_tracker_datalake.bucket
    key    = "dependencies/layers/minimal_python.zip"
    source = "${path.module}/layers/minimal_dependencies/python.zip"
    etag   = filemd5("${path.module}/layers/minimal_dependencies/python.zip")
    tags   = local.tags
    
    depends_on = [aws_s3_bucket.football_tracker_datalake]

    lifecycle {
        precondition {
            condition     = fileexists("${path.module}/layers/minimal_dependencies/python.zip")
            error_message = "Arquivo minimal_dependencies/python.zip não encontrado. Execute o script de criação da layer primeiro."
        }
    }
}
