import requests
import logging

class BaseExtractor:
    def __init__(self, api_key, config):
        self.api_key = api_key
        self.config = config
        self.headers = {'X-Auth-Token': api_key}
        self.logger = logging.getLogger("futebol_tracker")

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

        self.logger.debug("Fazendo requisição para URL: %s", url)
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            self.logger.info("Requisição bem-sucedida para %s", endpoint_name)
            return response.json()
        except Exception as e:
            self.logger.error("Erro na requisição para %s: %s", endpoint_name, e)
            return None
