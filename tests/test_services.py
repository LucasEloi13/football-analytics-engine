import psycopg2
import boto3
from botocore.exceptions import NoCredentialsError
import os

def test_postgres():
    print("Testando conexão com PostgreSQL...")
    try:
        conn = psycopg2.connect(
            dbname="soccer_data",
            user="user",
            password="pass",
            host="postgres",
            port="5432"
        )
        cur = conn.cursor()
        cur.execute("SELECT version();")
        db_version = cur.fetchone()
        print("PostgreSQL conectado. Versão:", db_version)
        cur.close()
        conn.close()
    except Exception as e:
        print("Erro ao conectar no PostgreSQL:", e)

def test_minio():
    print("\nTestando conexão com MinIO (S3)...")
    try:
        s3 = boto3.client(
            's3',
            endpoint_url='http://minio:9000',
            aws_access_key_id='minioadmin',
            aws_secret_access_key='minioadmin',
            region_name='us-east-1'
        )
        
        bucket_name = "test-bucket"
        file_name = "test_file.txt"
        file_content = "Hello, MinIO!"
        
        # Criar bucket
        try:
            s3.create_bucket(Bucket=bucket_name)
            print(f"Bucket '{bucket_name}' criado.")
        except s3.exceptions.BucketAlreadyOwnedByYou:
            print(f"Bucket '{bucket_name}' já existe.")

        # Criar arquivo temporário
        with open(file_name, "w") as f:
            f.write(file_content)
        
        # Upload do arquivo
        s3.upload_file(file_name, bucket_name, file_name)
        print(f"Arquivo '{file_name}' enviado para MinIO.")

        # Download para verificar
        s3.download_file(bucket_name, file_name, f"downloaded_{file_name}")
        print(f"Arquivo '{file_name}' baixado de MinIO como 'downloaded_{file_name}'.")

        # Limpeza
        os.remove(file_name)
        os.remove(f"downloaded_{file_name}")

    except NoCredentialsError:
        print("Credenciais inválidas para MinIO.")
    except Exception as e:
        print("Erro ao conectar no MinIO:", e)

if __name__ == "__main__":
    test_postgres()
    test_minio()
