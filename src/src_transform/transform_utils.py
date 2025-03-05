import pandas as pd
import boto3
import json
from io import BytesIO
from botocore.exceptions import ClientError


def get_s3_client():
    try:
        client = boto3.client('s3')
        return client
    except ClientError as e:
        raise RuntimeError("failed to connect to s3, error message as {e}") from e


def get_s3_object(client, bucket, key):
    s3_obj = client.get_object(Bucket=bucket, Key=key)
    s3_obj_bytes = s3_obj["Body"].read()
    s3_obj_dict = json.loads(s3_obj_bytes.decode('utf-8'))
    return s3_obj_dict

def convert_s3_obj_to_df(s3_obj_dict):
    data = s3_obj_dict["data"]
    columns = s3_obj_dict['columns']
    df = pd.DataFrame(data,columns=columns)
    return df

def convert_df_to_s3_obj(client, df, bucket, key):
    output_buffer = BytesIO()
    df.to_parquet(output_buffer)
    body = output_buffer.getvalue()
    client.put_object(Bucket=bucket, Key=key, Body=body)





