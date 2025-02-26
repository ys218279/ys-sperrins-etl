# this lambda will initially connect to the db
# then it will read all the data from the specified tables
# the first time it will select all from the tables, with conn.run('query)
# this then need to be reformatted
# then it will be written to the the ingestion s3 bucket
# using datatime year/month/day/timestamp.parquet

# periodically checks for new and updated data
# if the column 'last_updated' is newer than the last pull of data,
# then new data is grabbed/reformatted/written to ingestion bucket

import boto3
import os
from pg8000.native import Connection
from src_ingestion.connection import connect_to_db, close_db_connection

BUCKET_NAME = os.environ["S3_BUCKET_NAME"]


def lambda_handler(event, context):
    pass
