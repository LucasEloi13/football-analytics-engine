import os
import sys
from datetime import datetime
from config.config_loader import load_config
from scripts.extract.competition_details_extractor import CompetitionDetailsExtractor
from scripts.utils.s3_utils import gerar_s3_key
from scripts.load.S3Uploader import S3Uploader
import logging

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
        import json
        with open("tests/teste_upload_s3.json", "r") as f:
            data = json.load(f)

        # data_extractor = CompetitionDetailsExtractor(config)
        # data = data_extractor.get_competition_details()
        # logger.info("Extração de dados realizada com sucesso.")
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

    # try:
    #     key = gerar_s3_key('raw', 'competition_details', datetime.utcnow())
    #     print(f"Chave com data explícita: {key}")
    # except Exception as e:
    #     print(f"Erro com data explícita: {e}")

if __name__ == "__main__":
    # Executar localmente para testes
    event = {}
    context = None  # Contexto pode ser None para testes locais
    response = lambda_handler(event, context)
    print(response)  # Exibir a resposta para verificar o resultado da execução