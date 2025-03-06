#pseudo:
#create util file:
    # connection to db
    # get files from s3 bucket processed zone
    # read data from parque files and insert into dw
#lambda invoke utils functions
#for facts we retrieve all files, for dim retrieve only the latest file.
#test utils functions

import os
import boto3
from load_utils import (
    get_s3_client,
    connect_to_dw,
    close_dw_connection,
    pd_read_s3_parquet,
    load_tables_to_dw
)
import sys

sys.path.append("src/src_load")

BUCKET_NAME = os.environ["S3_BUCKET_NAME_PROCESSED"]


def lambda_handler(event, context, BUCKET_NAME=BUCKET_NAME):
    if event:
        conn = connect_to_dw()
        s3_client = get_s3_client()
        fact_table =  ['fact_sales_order']
        dim_table = ['dim_date', 'dim_staff', 'dim_counterparty', 'dim_location', 'dim_currency', 'dim_design']
        for table_name, s3_key in event.items():
            if s3_key:
                df = pd_read_s3_parquet(s3_key, BUCKET_NAME, s3_client)
                load_tables_to_dw(conn, df, table_name, fact_table, dim_table)
        close_dw_connection(conn)

      
            
      

