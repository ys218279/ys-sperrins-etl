import boto3
from botocore.exceptions import ClientError
import json
from datetime import datetime
from pg8000.native import identifier

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

def list_s3_objects(client, bucket_name):
    return client.list_objects_v2(Bucket=bucket_name)

def upload_to_s3(bucket_name, table, result):
    tmp_file_path = f'/tmp/{table}.json'
    with open(tmp_file_path, 'w') as f:
        filedatain = json.dumps(result, indent=4, sort_keys=True, default=str)
        res_bytes = filedatain.encode('utf-8')
    s3_client = get_s3_client()
    y_m_d = datetime.now().strftime('%Y%m%d')
    filename = datetime.now().strftime('%H%M%S')
    object_name = f"{table}/{y_m_d}{filename}"
    s3_client.put_object(Body=res_bytes, Bucket=bucket_name, Key=object_name)
    return object_name

#if the max of last updated from db is diff from the max 
def fetch_latest_update_time_from_s3(client, bucket_name, table_name):
    """fetch the latest time of the file being loaded to s3 bucket and return the latest upload time as int."""
    response = client.list_objects_v2(Bucket=bucket_name, Prefix=table_name + '/')
    raw_all_updates = response.get('Contents', [])
    if raw_all_updates:
        all_tables = [update['Key'].split('/')[0] for update in raw_all_updates]
        if table_name not in all_tables:
            return 20000101000001
        all_updates = [update['Key'].split('/')[-1] for update in raw_all_updates]
        last_update = max(list(map(int, all_updates)))
        return last_update
    return 20000101000001
    
def fetch_latest_update_time_from_db(conn, table_name):
    """fetch the latest update of the table in db and return the latest update time as int."""
    query = f'SELECT last_updated FROM {identifier(table_name)} ORDER BY last_updated DESC LIMIT 1;'
    raw_last_updated = conn.run(query)
    last_updated_dt = raw_last_updated[0][0]
    formatted_res = int(last_updated_dt.strftime('%Y%m%d%H%M%S'))
    return formatted_res


#strp

    



