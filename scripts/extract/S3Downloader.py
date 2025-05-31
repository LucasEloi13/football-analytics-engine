import boto3
import json
from io import BytesIO

from botocore.exceptions import ClientError

class S3Downloader:
    def __init__(self, bucket_name, endpoint_url, access_key, secret_key, region_name='us-east-1'):
        self.bucket_name = bucket_name
        self.s3 = boto3.client('s3',
                               endpoint_url=endpoint_url,
                               aws_access_key_id=access_key,
                               aws_secret_access_key=secret_key,
                               region_name=region_name)        

    def download_json(self, key):
        """Baixa arquivo JSON do S3 e retorna como dict"""
        response = self.s3.get_object(Bucket=self.bucket_name, Key=key)
        content = response['Body'].read().decode('utf-8')
        return json.loads(content)
