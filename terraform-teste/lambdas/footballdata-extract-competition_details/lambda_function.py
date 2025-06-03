import os
import sys

from config.config_loader import load_config
from logs.logger import setup_logging
from scripts.competition_details_extractor import CompetitionDetailsExtractor


def lambda_handler(event, context):

    try:
        api_key, config = load_config()
    except Exception as e:
        print(f"Erro ao carregar configuração dentro do handler: {e}")
        # Decida como lidar com isso: retornar um erro, usar defaults, etc.
        return {
            'statusCode': 500,
            'body': f'Erro de configuração: {str(e)}'
        }

    try:
        competition_extractor = CompetitionDetailsExtractor(api_key, config)
        competition_details = competition_extractor.get_competition_details()

        print(f"Competition Details: {competition_details}")

        # O Lambda espera um retorno serializável em JSON.
        # Adapte o retorno conforme necessário.
        return {
            'statusCode': 200,
            'body': {
                'message': "Competition details extracted successfully!",
                'details': competition_details  # Certifique-se que competition_details é serializável
            }
        }

    except Exception as e:
        print(f"Erro durante a execução da extração: {e}")
        # Logar o traceback completo para CloudWatch é uma boa prática
        import traceback
        print(traceback.format_exc())
        return {
            'statusCode': 500,
            'body': f'Erro interno no servidor: {str(e)}'
        }