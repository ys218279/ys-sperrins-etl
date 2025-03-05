from load_utils import get_s3_client, transfer_from_parquet_to_df, load_to_dw
import os

BUCKET_NAME = os.environ["S3_BUCKET_NAME"]

def lambda_handler(event, context, BUCKET_NAME=BUCKET_NAME):
    if event:
        s3_client = get_s3_client()
        fact_table = 'fact_sales_orders'
        for table_name, s3_key in event.items():
            if s3_key:
                df = transfer_from_parquet_to_df(s3_key, s3_client, BUCKET_NAME)
                load_to_dw(df, table_name, fact_table)


