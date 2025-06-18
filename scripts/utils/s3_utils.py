# utils/s3_utils.py

from datetime import datetime

def gerar_s3_key(base_dir, tabela, formato, data=None):
    """Gera a key para o S3 seguindo a estratégia definida"""
    if data is None:
        data = datetime.utcnow()
    data_str = data.strftime('%Y-%m-%d')
    # hora_str = data.strftime('%Y%m%dT%H%MZ')
    
    key = f"{base_dir}/api_football/{tabela}/dt={data_str}/.{formato}"
    return key
