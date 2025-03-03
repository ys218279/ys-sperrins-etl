# import pandas as pd
import boto3
import json
import os
from io import StringIO
from botocore.exceptions import ClientError
# import sys
# sys.path.append('src/src_transform')
from transform_utils import get_s3_object, convert_s3_obj_to_df, convert_df_to_s3_obj
from transform_pandas import create_dim_design_table, create_dim_currency_table, create_dim_staff_table, create_dim_location_table, create_dim_counterparty_table, create_dim_date_table, create_fact_sales_table

INGESTION_BUCKET_NAME = os.environ["S3_BUCKET_NAME_INGESTION"]
PROCESSED_BUCKET_NAME = os.environ["S3_BUCKET_NAME_PROCESSED"]


def lambda_handler(event,context):
    pass

