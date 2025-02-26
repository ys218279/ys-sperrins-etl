'''
Doc Strings for this Ingestion Lambda

This lambda will SELECT data from the ToteSys Database and:
    - loads the data in to a dictionary with two keys:
        "columns" : <list of table headers>
        "data" : <contains raw data as a list of lists. Each list is one row of the table.>
    - transforms the data to json format and dumps it in a local file
    - uploads that file to the s3 bucket using the following format:
        - table_name/year-month-day/timestamp(HHMMSS).json
    - finally this lambda will delete the local file in the root dir and close the db conn.

Important Notes: 
    - Any data in a datetime format when extracted from ToteSys is coverted in to a string format.
    - Any data fields that had None have been converted to 'null' values.

'''


import boto3
from botocore.exceptions import ClientError
import os
import json
from datetime import datetime
from pg8000.native import identifier
from src.src_ingestion.connection import connect_to_db, close_db_connection

BUCKET_NAME = os.environ["S3_BUCKET_NAME"]

def lambda_handler(event, context):
    conn = None
    try:
        client = boto3.client('secretsmanager')
        conn = connect_to_db(client)

        raw_table_list =conn.run("SELECT * from information_schema.tables")
        table_list = [item[2] for item in raw_table_list if item[1] == 'public']
        for table_name in table_list:
            if table_name[0] != "_":
                raw_data = conn.run(f"SELECT * FROM {identifier(table_name)}")
                columns = [col['name'] for col in conn.columns]
                result = {"columns" : columns, "data" : raw_data}
                print(raw_data[0])
                filename = datetime.now().strftime('%H%M%S')

                with open(f'{filename}.json','w') as f:
                    filedatain = json.dumps(result, indent=4, sort_keys=True, default=str)
                    f.write(filedatain)

                    s3_client = boto3.client('s3')
                    try:
                        y_m_d=datetime.now().strftime('%Y-%m-%d')
                        object_name=f"{table_name}/{y_m_d}/{filename}.json"
                        print(object_name)
                        response = s3_client.upload_file(f'{filename}.json', BUCKET_NAME, object_name)
                        return True      
                    except ClientError as e:

                        print("\n \n\n")
                        print("table_name>>>>", e)
                        return False
                    finally:
                        dir=os.getcwd()
                        print(dir)
                        os.remove(f"{dir}/{filename}.json")
    finally:
        if conn:
            close_db_connection(conn)

# Still TO DO
# periodically checks for new and updated data
# if the column 'last_updated' is newer than the last pull of data,
# then new data is grabbed/reformatted/written to ingestion bucket
