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

def load_tables_to_dw(conn, df, table_name, fact_tables, dim_tables):
    # engine = create_engine('postgresql://username:password@localhost:5432/postgres')
    engine = generate_conn_dw_engine()
    if table_name in fact_tables:
        df.to_sql(table_name, con=engine, if_exists='append',index=False)
    elif table_name in dim_tables:
        check_empty_table = conn.run(f'SELECT * FROM {identifier(table_name)};')
        if not check_empty_table:
            df.to_sql(table_name, con=engine, if_exists='append',index=False)
        column_names = get_column_names(conn, table_name)
        update_query = get_update_query(table_name, column_names)
        rows = [row for row in df.itertuples(index=False, name=None)]
        for row in rows:
            conn.run(update_query, row)


def get_update_query(table_name, column_names):
    conflict_column = column_names[0]  
    placeholders = ", ".join(["%s"] * len(column_names))
    columns = ", ".join(column_names)
    update_set = ", ".join([f"{col} = EXCLUDED.{col}" for col in column_names[1:]])
    query = f"""
    INSERT INTO {identifier(table_name)} ({identifier(columns)})
    VALUES ({identifier(placeholders)})
    ON CONFLICT ({identifier(conflict_column)})
    DO UPDATE SET {identifier(update_set)}
    """
    return query

def get_column_names(conn, table_name: str) -> List[str]:
    query = f"""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = :table
    """
    result = conn.run(query, table=table_name)
    return [row[0] for row in result]

def delete_all_from_dw():
    conn = connect_to_dw()
    tables = ['dim_date', 'dim_staff', 'dim_counterparty', 'dim_location', 'dim_currency', 'dim_design', 'fact_sales_order']
    for table in tables:
        query = f"DELETE FROM {identifier(table)};"
        conn.run(query)

# if __name__ == "__main__":
    # data = {'currency_id':[1, 2], 'currency_code':[1, 2], "currency_name": [1, 2]}
    # df = pd.DataFrame(data)
    # engine = generate_conn_dw_engine()
    # df.to_sql('dim_currency', con=engine, if_exists='append',index=False)
    # delete_all_from_dw()



