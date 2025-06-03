import os
import yaml
from dotenv import load_dotenv

def load_config():
    load_dotenv()
    api_key = os.getenv("FOOTBALL_DATA_API_KEY")
    with open("config/config.yaml") as f:
        config_yaml = yaml.safe_load(f)
    return api_key, config_yaml