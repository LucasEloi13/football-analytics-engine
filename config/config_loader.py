import os
import yaml
from dotenv import load_dotenv, dotenv_values

def load_config():
    config = {}

    env_vars = dotenv_values(".env")
    config.update(env_vars)

    with open("config/config.yaml") as f:
        config_yaml = yaml.safe_load(f)
    env_vars = dotenv_values(".env")
    
    config = {**config_yaml, **env_vars}
    return config