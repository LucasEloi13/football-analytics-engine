resource "aws_s3_bucket" "football_tracker_datalake"{
    bucket = var.bucket_name
    tags=local.tags
}