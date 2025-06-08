# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import boto3
import json
import os
from botocore.exceptions import ClientError
import logging

class S3Uploader: 
    def __init__(self, config):
        self.bucket_name = config.get("S3_BUCKET_NAME")
        self.s3_endpoint_url = config.get("S3_DATALAKE_ENDPOINT_URL")
        self.aws_access_key_id = config.get("AWS_ACCESS_KEY_ID")
        self.aws_secret_access_key = config.get("AWS_SECRET_ACCESS_KEY")
        # self.config = config

        try:
            logging.info("Inicializando S3Uploader com bucket: %s", self.bucket_name)
            self.s3 = boto3.client(
                's3',
                endpoint_url=self.s3_endpoint_url,
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                region_name='us-east-1'  # Usar 'us-east-1' como padrão
            )
            logging.info("S3Uploader inicializado para bucket: %s", self.bucket_name)
        except Exception as e:
            logging.error("Erro ao inicializar S3Uploader: %s", e)
            raise e
    def upload_json(self, data, key):
        """Envia um dicionário JSON para o bucket com o prefixo (key) especificado"""
        try:
            logging.info("Enviando JSON para o S3: %s/%s", self.bucket_name, key)
            ## criar bucket se não existir
            self.create_bucket()

            json_data = json.dumps(data, ensure_ascii=False).encode('utf-8')
            self.s3.put_object(Bucket=self.bucket_name, Key=key, Body=json_data)
            logging.info("Arquivo JSON enviado com sucesso para %s/%s", self.bucket_name, key)
        except ClientError as e:
            logging.error("Erro ao enviar JSON para o S3: %s", e)
            raise e
        
    def upload_parquet(self, parquet_bytes, key):
        """
        Envia um arquivo Parquet (em bytes) para o bucket com o prefixo (key) especificado.
        parquet_bytes: resultado de BytesIO().getvalue()
        key: caminho/arquivo no bucket (ex: processed/matches/arquivo.parquet)
        """
        try:
            logging.info("Enviando Parquet para o S3: %s/%s", self.bucket_name, key)
            ## criar bucket se não existir
            self.create_bucket()

            self.s3.put_object(Bucket=self.bucket_name, Key=key, Body=parquet_bytes)
            logging.info("Arquivo Parquet enviado com sucesso para %s/%s", self.bucket_name, key)
        except ClientError as e:
            logging.error("Erro ao enviar Parquet para o S3: %s", e)
            raise e
    
    def upload_file(self, file_path, key):
        """Envia um arquivo local para o bucket"""
        try:
            logging.info("Enviando arquivo %s para o S3: %s/%s", file_path, self.bucket_name, key)
            ## criar bucket se não existir
            self.create_bucket()
            
            self.s3.upload_file(file_path, self.bucket_name, key)
            logging.info("Arquivo %s enviado com sucesso para %s/%s", file_path, self.bucket_name, key)
        except ClientError as e:
            logging.error("Erro ao enviar arquivo para o S3: %s", e)
            raise e


    def create_bucket(self):
        """Cria o bucket S3 se não existir"""
        try:
            self.s3.create_bucket(Bucket=self.bucket_name)
            logging.info("Bucket %s criado com sucesso", self.bucket_name)
        except ClientError as e:
            if e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
                logging.info("Bucket %s já existe e é de sua propriedade", self.bucket_name)
            else:
                logging.error("Erro ao criar bucket: %s", e)
                raise e