import requests
import yaml
from datetime import datetime, timedelta

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from config.config_loader import load_config

class FootballDataExtractor:
    def __init__(self, base_url, api_key, config):
        self.api_key = api_key
        self.base_url = base_url
        self.config = config
        self.headers = {'X-Auth-Token': api_key}

    def get_brasileirao_id(self):
        """"
        Obter ID do Brasileirão Série A:
            No JSON você tem um campo code: "BSA" que serve exatamente como identificador 
            único e semântico para essa competição. Ao contrário de id, que é numérico e poderia, 
            em teoria, mudar caso migrem o banco de dados, o código “BSA” tende a ser mais estável 
            e legível.
        """
        competitions_endpoint = self.config['endpoints']['competitions']
        response = requests.get(
            f"{self.base_url}{competitions_endpoint}",
            headers=self.headers
        )
        
        data = response.json()
        competitions = data.get("competitions", [])

        for comp in competitions:
            if comp.get("code", "").upper() == "BSA":
                return comp["id"]
        return None
        
if __name__ == "__main__":
    base_url, api_key, config = load_config()
    extractor = FootballDataExtractor(base_url, api_key, config)
    print(extractor.get_brasileirao_id())

