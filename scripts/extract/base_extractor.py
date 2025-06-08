import requests
import logging

class BaseExtractor:
    def __init__(self, config):
        # self.api_key = api_key
        self.config = config
        self.headers = {'X-Auth-Token': self.config['FOOTBALL_DATA_API_KEY']}
        
    def make_request(self, endpoint_name, **params):
        """
        Método genérico para fazer requisições.
        """
        endpoint = self.config['endpoints'][endpoint_name]
        path = endpoint['path'].replace('{id}', str(self.config['brasileirao_id']))
        url = f"{self.config['base_url']}{path}"

        if params:
            query = '&'.join([f'{k}={v}' for k, v in params.items()])
            url += f'?{query}'

        logging.debug("Fazendo requisição para URL: %s", url)
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            logging.info("Requisição bem-sucedida para %s", endpoint_name)
            return response.json()
        except Exception as e:
            logging.error("Erro na requisição para %s: %s", endpoint_name, e)
            return None
