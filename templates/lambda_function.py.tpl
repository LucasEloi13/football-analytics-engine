import os
import sys
import logging

from config.config_loader import load_config
from scripts.extract.{{extractor_file_name}} import {{extractor_class}}

from datetime import datetime
from scripts.utils.s3_utils import gerar_s3_key
from scripts.load.S3Uploader import S3Uploader

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


def lambda_handler(event, context):

    try:
        config = load_config()
        logger.info("Configuração carregada com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao carregar configuração dentro do handler: {e}")

    try:
        data_extractor = CompetitionDetailsExtractor(config)
        data = data_extractor.get_competition_details()
        logger.info("Extração de dados realizada com sucesso.")
    except Exception as e:
        logger.error(f"Erro durante a execução da extração: {e}")

    try:
        s3_bucket_key = gerar_s3_key('raw', 'competition_details', datetime.utcnow())
        logger.info(f"Chave S3 gerada: {s3_bucket_key}")
        uploader = S3Uploader(config)
        uploader.upload_json(data, s3_bucket_key)
        logger.info("Upload para o S3 realizado com sucesso.")
    except Exception as e:
        logger.error(f"Erro: {e}")
