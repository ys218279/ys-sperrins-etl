import boto3
from botocore.exceptions import ClientError
import json
from datetime import datetime
from pg8000.native import Connection, identifier
import sys
import pyarrow.parquet as pa
import pandas as pd
import io
from typing import List
import sys
from sqlalchemy import create_engine

sys.path.append("src/src_load")

def retrieval(client, secret_identifier='de_2024_12_02_dw'):
    """return the credentials to the totesys db in a dictionary"""
    if "SecretsManager" in str(type(client)):
        try:
            response = client.get_secret_value(SecretId=secret_identifier)
            res_str = response["SecretString"]
            res_dict = json.loads(res_str)
            return res_dict
        except client.exceptions.ResourceNotFoundException as err:
            print(err)
        except Exception as err:
            print({"ERROR": err, "massage": "Fail to connect to aws secret manager!"})
    else:
        print("invalid client type used for secret manager! plz contact developer!")

def get_s3_client():
    """return a client to connect to s3"""
    try:
        client = boto3.client("s3", region_name="eu-west-2")
        return client
    except ClientError:
        raise ClientError(
            {
                "Error": {
                    "Code": "FailedToConnect",
                    "Message": "failed to connect to s3",
                }
            },
            "GetS3Client",
        )


def get_secrets_manager_client():
    """return a client to connect to secret manager"""
    try:
        client = boto3.client("secretsmanager", region_name="eu-west-2")
        return client
    except ClientError:
        raise ClientError(
            {
                "Error": {
                    "Code": "FailedToConnect",
                    "Message": "failed to connect to secret manager",
                }
            },
            "GetSecretsManagerClient",
        )


def pd_read_s3_parquet(key, bucket, s3_client):
    obj = s3_client.get_object(Bucket=bucket, Key=key)
    df = pd.read_parquet(io.BytesIO(obj['Body'].read()), engine='pyarrow')
    return df

def connect_to_dw(secret_identifier='de_2024_12_02_dw'):
    """return conn to dw"""
    client = get_secrets_manager_client()
    credentials = retrieval(client, secret_identifier=secret_identifier)
    return Connection(
        user=credentials["username"],
        password=credentials["password"],
        database=credentials["dbname"],
        host=credentials["host"],
    )

def generate_conn_dw_engine():
    client = get_secrets_manager_client()
    credentials = retrieval(client)
    engine = create_engine(f'postgresql://{credentials["username"]}:{credentials["password"]}@{credentials["host"]}:5432/{credentials["dbname"]}')
    return engine

def close_dw_connection(conn):
    """close dw"""
    conn.close()

def load_tables_to_dw(conn, df, table_name, fact_tables):
    column_names = get_column_names(conn, table_name)
    on_conflict = table_name not in fact_tables
    update_query = get_insert_query(table_name, column_names, on_conflict=on_conflict)
    for row in df.reset_index().to_dict(orient="records"):
        conn.run(update_query, **row, table_name=table_name)

def get_insert_query(table_name: str, column_names: List[str], on_conflict: bool) -> str:
    conflict_column = column_names[0]  
    placeholders = ", ".join([f":{column_name}" for column_name in column_names])
    columns = ", ".join(column_names)
    update_set = ", ".join([f"{col} = EXCLUDED.{col}" for col in column_names[1:]])
    query = f"""
    INSERT INTO {table_name} ({columns})
    VALUES ({placeholders})"""
    if not on_conflict:
        return f"{query};"
    return f"""{query}
    ON CONFLICT ({conflict_column})
    DO UPDATE SET {update_set};
    """


def get_column_names(conn, table_name: str) -> List[str]:
    query = f"""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = :table_name;
    """
    result = conn.run(query, table_name=table_name)
    return [row[0] for row in result]


def delete_all_from_dw():
    conn = connect_to_dw()
    tables = ['dim_date', 'dim_staff', 'dim_counterparty', 'dim_location', 'dim_currency', 'dim_design', 'fact_sales_order']
    for table in tables:
        query = f"DELETE FROM {identifier(table)};"
        conn.run(query)

if __name__ == "__main__":
    conn = connect_to_dw()
    fact_tables =  ['fact_sales_order']
    data = {'currency_id':[1, 2], 'currency_code':["/dsa1@", "dsa/2"], "currency_name": [1, 2]}
    df = pd.DataFrame(data).set_index('currency_id')
    load_tables_to_dw(conn, df, 'dim_currency', fact_tables)
    updated_data = {'currency_id':[1, 2], 'currency_code':[2, 5], "currency_name": [1, 5]}
    df_updated = pd.DataFrame(updated_data).set_index('currency_id')
    print(df_updated)
    load_tables_to_dw(conn, df_updated, "dim_currency", fact_tables)
    delete_all_from_dw()
