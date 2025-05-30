import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import boto3
import json
import os
from botocore.exceptions import ClientError
import logging

logger = logging.getLogger("futebol_tracker")

class S3Uploader: 
    def __init__(self, bucket_name, endpoint_url, access_key, secret_key, region_name='us-east-1'):
        self.bucket_name = bucket_name
        self.s3 = boto3.client(
            's3',
            endpoint_url=endpoint_url,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region_name
        )
        logger.info("S3Uploader inicializado para bucket: %s", bucket_name)
    
    def upload_json(self, data, key):
        """Envia um dicionário JSON para o bucket com o prefixo (key) especificado"""
        try:
            json_data = json.dumps(data, ensure_ascii=False).encode('utf-8')
            self.s3.put_object(Bucket=self.bucket_name, Key=key, Body=json_data)
            logger.info("Arquivo JSON enviado com sucesso para %s/%s", self.bucket_name, key)
        except ClientError as e:
            logger.error("Erro ao enviar JSON para o S3: %s", e)
            raise e
    
    def upload_file(self, file_path, key):
        """Envia um arquivo local para o bucket"""
        try:
            self.s3.upload_file(file_path, self.bucket_name, key)
            logger.info("Arquivo %s enviado com sucesso para %s/%s", file_path, self.bucket_name, key)
        except ClientError as e:
            logger.error("Erro ao enviar arquivo para o S3: %s", e)
            raise e