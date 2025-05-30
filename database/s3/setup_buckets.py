import boto3
 
import os
from dotenv import load_dotenv

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from logs.logger import setup_logging
import logging

# Configura o sistema de logging reutilizável
setup_logging()
logger = logging.getLogger("futebol_tracker")

# Carrega variáveis do .env
load_dotenv()


s3_endpoint_url = os.getenv('S3_DATALAKE_ENDPOINT_URL')
s3_aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
s3_aws_secret_access_key = os.getenv('AWS_SECRET_ACESS_KEY')

logger.info("Conectando ao S3 endpoint: %s", s3_endpoint_url)

s3 = boto3.client('s3',
                  endpoint_url=s3_endpoint_url,
                  aws_access_key_id=s3_aws_access_key_id,
                  aws_secret_access_key=s3_aws_secret_access_key,
                  region_name='us-east-1')

# Criar bucket
bucket_name = 'data-lake'

try:
    logger.info("Criando bucket: %s", bucket_name)
    s3.create_bucket(Bucket=bucket_name)
    logger.info("Bucket criado com sucesso.")
except Exception as e:
    logger.error("Erro ao criar bucket: %s", e)

