import os
from load_utils import (
    get_s3_client,
    get_secrets_manager_client,
    connect_to_dw,
    close_dw_connection,
    pd_read_s3_parquet,
    load_tables_to_dw
)
import sys

sys.path.append("src/src_load")

BUCKET_NAME = os.environ["S3_BUCKET_NAME_PROCESSED"]


def lambda_handler(event, context, BUCKET_NAME=BUCKET_NAME):
    """Main handler - This loads the data from the processed s3 bucket, into the
                    required schema for the Data Warehouse
      Args:
            Event: {
                    "dim_design": "dim_design/2025-03-06/224349.parquet",
                    "dim_currency": False
                    "dim_staff": "dim_staff/2025-03-06/224349.parquet",
                    "dim_location": "dim_location/2025-03-06/224349.parquet",
                    "dim_counterparty": "dim_counterparty/2025-03-06/224349.parquet",
                    "dim_date": "dim_date/2025-03-06/224349.parquet",
                    "fact_sales_order": "fact_sales_order/2025-03-06/224349.parquet"
                    }   
                        event is a dictionary that is passed in by StateMachine payload 
                        with table names as keys, and object keys as values (False if no new table).
            Context: supplied by AWS
    """
    client_secret_manager = get_secrets_manager_client()
    s3_client = get_s3_client()
    conn = connect_to_dw(client_secret_manager)
    fact_table =  ['fact_sales_order']
    for table_name, s3_key in event.items():
        if s3_key:
            df = pd_read_s3_parquet(s3_key, BUCKET_NAME, s3_client)
            load_tables_to_dw(conn, df, table_name, fact_table)
    close_dw_connection(conn)