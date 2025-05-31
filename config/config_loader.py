import os
import yaml
from dotenv import load_dotenv

def load_config():
    load_dotenv()
    api_key = os.getenv("FOOTBALL_DATA_API_KEY")
    with open("/workspaces/futebol-tracker/config/config.yaml") as f:
        config_yaml = yaml.safe_load(f)
    return api_key, config_yaml


if __name__ == "__main__":
    api_key, config = load_config()
    print("API Key:", api_key)
    print("Config:", config)
    # Exemplo de uso
    # api_key, config = load_config()
    # print(api_key)
    # print(config)  # Imprime o conteúdo do arquivo config.yaml