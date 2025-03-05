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
from datetime import datetime
from pg8000.native import identifier
from src_load.load_utils import (
    upload_to_s3,
    retrieval,
    get_s3_client,
    fetch_latest_update_time_from_s3,
    fetch_latest_update_time_from_db,
    connect_to_db,
    close_db_connection,
    pd_read_s3_multiple_parquets,
    pd_read_s3_parquet,
    load_tables_to_dw
)
import sys

sys.path.append("src/src_load")

BUCKET_NAME = os.environ["S3_BUCKET_NAME"]



def lambda_handler(event, context, BUCKET_NAME=BUCKET_NAME):
    if event:
        s3_client = get_s3_client()
        fact_table =  ['fact_sales_order']
        for table_name, s3_key in event.items():
            if s3_key:
                df = pd_read_s3_parquet(s3_key, BUCKET_NAME, s3_client)
                load_tables_to_dw(df, table_name, fact_table)


      
            
      

