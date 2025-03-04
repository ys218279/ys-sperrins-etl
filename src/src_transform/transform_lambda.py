import boto3
import json
import os
from io import StringIO
from botocore.exceptions import ClientError
from datetime import datetime
import sys
sys.path.append('src/src_transform')
from transform_utils import get_s3_client, get_s3_object, convert_s3_obj_to_df, convert_df_to_s3_obj
from transform_pandas import create_dim_design_table, create_dim_currency_table, create_dim_staff_table, create_dim_location_table, create_dim_counterparty_table, create_dim_date_table, create_fact_sales_order_table

INGESTION_BUCKET_NAME = os.environ["S3_BUCKET_NAME_INGESTION"]
PROCESSED_BUCKET_NAME = os.environ["S3_BUCKET_NAME_PROCESSED"]


def lambda_handler(event,context):
    """Main handler - This transforms the data from the ingestion s3 bucket, into the
                    required schema for the Data Warehouse, before converting back to JSON
                    and putting in processed s3 bucket.
      Args:
            Event: {'department': 'department/2025-03-03/131224.json',
                    'transaction': 'transaction/2025-03-03/131223.json',
                     'payment': False ...}
                        event is a dictionary that is passed in by StateMachine payload 
                        with table names as keys, and object keys as values (False if no new table).
            Context: supplied by AWS
        
        Returns:
        dictionary e.g. {'dim_staff': 'dim_staff/2025-03-03/131224.json',
                         'dim_currency': 'dim_currency/2025-03-03/131223.json',
                          'dim_staff' : False ...}
        }"""
    
    data_tables = ['dim_design', 'dim_currency', 'dim_staff', 'dim_location', 'dim_counterparty', 'dim_date', 'fact_sales_order']
    output_event = {'dim_design': False, 'dim_currency': False, 'dim_staff': False, 'dim_location': False, 'dim_counterparty': False, 'dim_date': False, 'fact_sales_order': False}
    y_m_d = datetime.now().strftime('%Y-%m-%d')
    filename = datetime.now().strftime('%H%M%S')
    
    
    for table in data_tables:
        s3_client = get_s3_client()
        if table == 'dim_design' and event['design']:
            obj_key_ingest = event['design']
            s3_object = get_s3_object(s3_client, INGESTION_BUCKET_NAME, obj_key_ingest)
            df = convert_s3_obj_to_df(s3_object)
            df_transformed = create_dim_design_table(df)
            obj_key_processed = f"{table}/{y_m_d}/{filename}.json"
            output_event[table] = obj_key_processed
            convert_df_to_s3_obj(s3_client, df_transformed, PROCESSED_BUCKET_NAME, obj_key_processed)
        if table == 'dim_currency' and event['currency']:
            obj_key_ingest = event['currency']
            s3_object = get_s3_object(s3_client, INGESTION_BUCKET_NAME, obj_key_ingest)
            df = convert_s3_obj_to_df(s3_object)
            df_transformed = create_dim_currency_table(df)
            obj_key_processed = f"{table}/{y_m_d}/{filename}.json"
            output_event[table] = obj_key_processed
            convert_df_to_s3_obj(s3_client, df_transformed, PROCESSED_BUCKET_NAME, obj_key_processed)
        if table == 'dim_staff' and event['staff'] and event['department']:
            obj_key_ingest1 = event['staff']
            obj_key_ingest2 = event['department']
            s3_object1 = get_s3_object(s3_client, INGESTION_BUCKET_NAME, obj_key_ingest1)
            s3_object2 = get_s3_object(s3_client, INGESTION_BUCKET_NAME, obj_key_ingest2)
            df1 = convert_s3_obj_to_df(s3_object1)
            df2 = convert_s3_obj_to_df(s3_object2)
            df_transformed = create_dim_staff_table(df1, df2)
            obj_key_processed = f"{table}/{y_m_d}/{filename}.json"
            output_event[table] = obj_key_processed
            convert_df_to_s3_obj(s3_client, df_transformed, PROCESSED_BUCKET_NAME, obj_key_processed)
        if table == 'dim_location' and event['address']:
            obj_key_ingest = event['address']
            s3_object = get_s3_object(s3_client, INGESTION_BUCKET_NAME, obj_key_ingest)
            df = convert_s3_obj_to_df(s3_object)
            df_transformed = create_dim_location_table(df)
            obj_key_processed = f"{table}/{y_m_d}/{filename}.json"
            output_event[table] = obj_key_processed
            convert_df_to_s3_obj(s3_client, df_transformed, PROCESSED_BUCKET_NAME, obj_key_processed)
        if table == 'dim_counterparty' and event['address'] and event['counterparty']:
            obj_key_ingest1 = event['address']
            obj_key_ingest2 = event['counterparty']
            s3_object1 = get_s3_object(s3_client, INGESTION_BUCKET_NAME, obj_key_ingest1)
            s3_object2 = get_s3_object(s3_client, INGESTION_BUCKET_NAME, obj_key_ingest2)
            df1 = convert_s3_obj_to_df(s3_object1)
            df2 = convert_s3_obj_to_df(s3_object2)
            df_transformed = create_dim_counterparty_table(df1, df2)
            obj_key_processed = f"{table}/{y_m_d}/{filename}.json"
            output_event[table] = obj_key_processed
            convert_df_to_s3_obj(s3_client, df_transformed, PROCESSED_BUCKET_NAME, obj_key_processed)
        if table == 'fact_sales_order' and event['sales_order']:
            obj_key_ingest = event['sales_order']
            s3_object = get_s3_object(s3_client, INGESTION_BUCKET_NAME, obj_key_ingest)
            df = convert_s3_obj_to_df(s3_object)
            df_transformed = create_fact_sales_order_table(df)
            obj_key_processed = f"{table}/{y_m_d}/{filename}.json"
            output_event[table] = obj_key_processed
            convert_df_to_s3_obj(s3_client, df_transformed, PROCESSED_BUCKET_NAME, obj_key_processed)
        if table == 'dim_date':
            df_transformed = create_dim_date_table()
            obj_key_processed = f"{table}/{y_m_d}/{filename}.json"
            output_event[table] = obj_key_processed
            convert_df_to_s3_obj(s3_client, df_transformed, PROCESSED_BUCKET_NAME, obj_key_processed)

    return output_event
    


            
