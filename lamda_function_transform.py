import os
import sys
from datetime import datetime
from config.config_loader import load_config
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# Um JSON terá contido várias entidades (tables), portanto, um JSON pode 
# derivar mais de uma tabela/parquet.
extract_to_transform_tables_correspondence = {
    'competition_details': ['area', 'competition', 'season'],
    'matches': 'matches',
    'standings': 'standings',
    'teams': ['coach', 'player', 'team']
}

def lambda_handler(event, context):
    try:
        config = load_config()
        logger.info("Configuração carregada com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao carregar configuração dentro do handler: {e}")

    
