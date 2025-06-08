import boto3
from config.config_loader import load_config

configs = load_config()
s3_bucket_name = configs.get('S3_BUCKET_NAME')
s3 = boto3.client(
    's3',
    endpoint_url=configs.get('S3_DATALAKE_ENDPOINT_URL'),
    aws_access_key_id=configs.get('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=configs.get('AWS_SECRET_ACCESS_KEY'),
    region_name='us-east-1'  # Usar 'us-east-1' como padrão
)

response = s3.list_objects_v2(Bucket=s3_bucket_name)

if 'Contents' in response:
    for obj in response['Contents']:
        print(obj['Key'])
else:
    print("Bucket vazio ou não encontrado.")