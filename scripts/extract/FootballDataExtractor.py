import requests
import yaml
from datetime import datetime, timedelta

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from config.config_loader import load_config
from logs.logger import setup_logging
import logging

setup_logging()
logger = logging.getLogger("futebol_tracker")

class FootballDataExtractor:
    def __init__(self, base_url, api_key, config):
        self.api_key = api_key
        self.base_url = base_url
        self.config = config
        self.headers = {'X-Auth-Token': api_key}
        logger.info("FootballDataExtractor inicializado.")

    def get_brasileirao_id(self):
        """"
        Obter ID do Brasileirão Série A:
        """
        endpoint = self.config['endpoints']['competitions']
        path = endpoint['path']
        logger.info("Buscando ID do Brasileirão Série A no endpoint %s", path)
        
        try:
            response = requests.get(
                f"{self.base_url}{path}",
                headers=self.headers
            )
            response.raise_for_status()
            data = response.json()
            competitions = data.get("competitions", [])

            for comp in competitions:
                if comp.get("code", "").upper() == "BSA":
                    brasileirao_id = comp["id"]
                    self.config['brasileirao_id'] = brasileirao_id
                    with open("config/config.yaml", "w", encoding='utf-8') as f:
                        yaml.dump(self.config, f, 
                                allow_unicode=True,
                                sort_keys=False,
                                default_flow_style=False)
                    logger.info("ID do Brasileirão encontrado e salvo: %s", brasileirao_id)
                    return brasileirao_id
            logger.warning("ID do Brasileirão Série A não encontrado.")
            return None
        except Exception as e:
            logger.error("Erro ao buscar ID do Brasileirão: %s", e)
            return None
    
    def _make_request(self, endpoint_name, **params):
        """"
        Método genérico para fazer requisições
        """
        if not self.config['brasileirao_id']:
            logger.info("ID do Brasileirão não encontrado no config, buscando...")
            self.get_brasileirao_id()

        # id = self.config['brasileirao_id']
        endpoint = self.config['endpoints'][endpoint_name]
        path = endpoint['path']

        # Substitui placeholders no path (ex: {id})
        path = path.replace('{id}', str(self.config['brasileirao_id']))
        
        url = f"{self.base_url}{path}"

        # Adiciona parâmetros de query se existirem
        if params:
            query = '&'.join([f'{k}={v}' for k, v in params.items()])
            url += f'?{query}'
        
        logger.debug("Fazendo requisição para URL: %s", url)
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            logger.info("Requisição bem-sucedida para %s", endpoint_name)
            return response.json()
        except Exception as e:
            logger.error("Erro na requisição para %s: %s", endpoint_name, e)
            return None

    def get_competition_details(self):
        logger.info("Obtendo detalhes da competição.")
        return self._make_request('competition_details')
    
    def get_standigs(self):
        logger.info("Obtendo tabela de classificação.")
        return self._make_request('standings')
    
    def get_matches(self):
        logger.info("Obtendo partidas.")
        return self._make_request('matches')
    
    def get_teams(self):
        logger.info("Obtendo times.")
        return self._make_request('teams')
    

if __name__ == "__main__":
    base_url, api_key, config = load_config()
    extractor = FootballDataExtractor(base_url, api_key, config)
    extractor.get_competition_details()

