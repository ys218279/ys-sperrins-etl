import boto3
from botocore.exceptions import ClientError
import json
from datetime import datetime

def get_s3_client():
    try:
        client = boto3.client('s3')
        return client
    except ClientError as e:
        raise RuntimeError("failed to connect to s3, error message as {e}") from e
    
def get_secrets_manager_client():
    try:
        client = boto3.client("secretsmanager")
        return client
    except ClientError as e:
        raise RuntimeError(f"failed to connect to secret manager, error message as {e}") from e

def list_s3_objects(bucket_name):
    s3_client = get_s3_client()
    return s3_client.list_objects_v2(Bucket=bucket_name)

def upload_to_s3(bucket_name, table, result):
    tmp_file_path = f'/tmp/{table}.json'
    with open(tmp_file_path, 'w') as f:
        filedatain = json.dumps(result, indent=4, sort_keys=True, default=str)
        res_bytes = filedatain.encode('utf-8')
    s3_client = get_s3_client()
    y_m_d = datetime.now().strftime('%Y-%m-%d')
    filename = datetime.now().strftime('%H%M%S')
    object_name = f"{table}/{y_m_d}/{filename}.json"
    s3_client.put_object(Body=res_bytes, Bucket=bucket_name, Key=object_name)


