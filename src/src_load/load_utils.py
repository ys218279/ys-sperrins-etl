import io
import boto3
from botocore.exceptions import ClientError
import pandas as pd
# from sqlalchemy import create_engine



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

def connect_to_dw():
    pass

def transfer_from_parquet_to_df(object_name, client, bucket_name): 
    obj = client.get_object(Bucket=bucket_name, Key=object_name)
    df = pd.read_parquet(io.BytesIO(obj['Body'].read()), engine='pyarrow')
    return df

def load_to_dw(df, table_name, fact_table):
    conn = connect_to_dw()
    if table_name == fact_table:
        df.to_sql(table_name, con=conn, if_exists='append', index=False)
    else:
        df.to_sql(table_name, con=conn, if_exists='replace', index=False)

    # engine = create_engine('postgresql://your_username:your_password@localhost:5432/your_database')