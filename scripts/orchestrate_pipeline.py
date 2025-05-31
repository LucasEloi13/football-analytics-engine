from io import BytesIO
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from config.config_loader import load_config
from logs.logger import setup_logging
import logging
import os
from dotenv import load_dotenv
from datetime import datetime

from scripts.extract.FootballDataExtractor import FootballDataExtractor
from scripts.load.S3Uploader import S3Uploader
from scripts.extract.S3Downloader import S3Downloader
from scripts.transform.match_transformer import MatchTransformer  # exemplo
from scripts.utils.s3_utils import gerar_s3_key

import pandas as pd
import pyarrow

setup_logging()
logger = logging.getLogger("orchestrate_pipeline")

# Carrega .env
load_dotenv()

# Configurações S3
s3_endpoint_url = os.getenv('S3_DATALAKE_ENDPOINT_URL')
s3_aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
s3_aws_secret_access_key = os.getenv('AWS_SECRET_ACESS_KEY')
bucket = 'data-lake'

# Carrega config API
api_key, config = load_config()

# Instancia componentes
extractor = FootballDataExtractor(api_key, config)
uploader = S3Uploader(bucket, s3_endpoint_url, s3_aws_access_key_id, s3_aws_secret_access_key)
downloader = S3Downloader(bucket, s3_endpoint_url, s3_aws_access_key_id, s3_aws_secret_access_key)

def orquestrar_tabela(tabela, extractor_func, transformer_cls):
    """Orquestra o fluxo completo para uma tabela"""
    logger.info(f"Iniciando orquestração para tabela: {tabela}")

    data_exec = datetime.utcnow()

    # 1. Extração
    logger.info("Extraindo dados brutos...")
    data = extractor_func()
    
    # 2. Upload raw
    raw_key = gerar_s3_key('raw', tabela, data_exec, 'json')
    uploader.upload_json(data, raw_key)
    logger.info(f"Upload JSON raw concluído: {raw_key}")

    # 3. Recuperar do S3
    data_baixado = downloader.download_json(raw_key)
    logger.info(f"Download JSON raw realizado: {raw_key}")

    # 4. Transformar
    transformer = transformer_cls(data_baixado)
    df = transformer.transform()
    logger.info(f"Transformação concluída para tabela: {tabela}")

    # 5. Salvar como parquet
    parquet_buffer = BytesIO()
    df.to_parquet(parquet_buffer, index=False, engine='pyarrow')  # Especifica o engine pyarrow

    # 6. Upload processed
    processed_key = gerar_s3_key('processed', tabela, data_exec, 'parquet')
    uploader.upload_parquet(parquet_buffer.getvalue(), processed_key)
    logger.info(f"Upload Parquet processed concluído: {processed_key}")

if __name__ == "__main__":
    # Exemplo com 'matches'
    orquestrar_tabela(
        tabela='matches',
        extractor_func=extractor.get_matches,
        transformer_cls=MatchTransformer
    )

    # Para outras tabelas, repetir:
    # orquestrar_tabela('teams', extractor.get_teams, TeamTransformer)
