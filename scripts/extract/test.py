import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from config.config_loader import load_config

base_url, api_key, config = load_config()

brasileirao_id = config['brasileirao_id']

if not config['brasileirao_id']:
    config['brasileirao_id'] = 2013
