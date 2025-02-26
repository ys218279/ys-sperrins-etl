
# this lambda will initially connect to the db
# then it will read all the data from the specified tables 
# the first time it will select all from each tables, with conn.run('query)
# this then need to be reformatted 
# then it will be written to the the ingestion s3 bucket
# using datatime year/month/day/fetch_hour_min/<table_name>_timestamp.parquet
    # OR table_name/year/month/day/timestamp.parquet

# periodically checks for new and updated data
# if the column 'last_updated' is newer than the last pull of data,
# then new data is grabbed/reformatted/written to ingestion bucket

import boto3
import os
from pg8000.native import identifier
from src.src_ingestion.connection import connect_to_db, close_db_connection

# BUCKET_NAME = os.environ["S3_BUCKET_NAME"]

def lambda_handler(event, context):
    conn = connect_to_db()
    raw_table_list =conn.run("SELECT * from information_schema.tables")
    table_list = [item[2] for item in raw_table_list if item[1] == 'public']    
    for table_name in table_list:
        raw_data = conn.run(f"SELECT * FROM {identifier(table_name)}")
        # implement formatting here.
