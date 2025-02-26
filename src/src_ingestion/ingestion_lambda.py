'''
Doc Strings for this Ingestion Lambda

This lambda will SELECT data from the ToteSys Database and:
    - loads the data in to a dictionary with two keys:
        "columns" : <list of table headers>
        "data" : <contains raw data as a list of lists. Each list is one row of the table.>
    - transforms the data to json format and encodes it in bytes
    - uploads that file-like object to the s3 bucket using the following format:
        - table_name/year-month-day/timestamp(HHMMSS).json
    - finally this lambda will close the db conn.

Important Notes: 
    - Any data in a datetime format when extracted from ToteSys is coverted in to a string format.
    - Any data fields that had None have been converted to 'null' values.
    - The S3 Bucket Name will need to be passed in as an argument otherwise it will default to the ENVIRONMENT VARIABLE.

'''


import boto3
from botocore.exceptions import ClientError
import os
import json
from datetime import datetime
from pg8000.native import identifier
from src.src_ingestion.connection import connect_to_db, close_db_connection

BUCKET_NAME = os.environ["S3_BUCKET_NAME"]

def lambda_handler(event, context, BUCKET_NAME=BUCKET_NAME):
    conn = None
    
    # if statement: uses s3_client to 
    # (a) check for any files - if no files, then grab a whole snapshot of the data
    # (b) else take the last file ... and enter the new section of logic below:    
    s3_client = boto3.client('s3')
    response = s3_client.list_objects_v2(Bucket=BUCKET_NAME)
    list_of_files = [response['Contents'][i]['Key'] for i in range(len(response['Contents']))]
    
    if list_of_files == None:

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
                    filename = datetime.now().strftime('%H%M%S')

                    with open(f'{filename}.json','w') as f:
                        filedatain = json.dumps(result, indent=4, sort_keys=True, default=str)
                        res_bytes = filedatain.encode('utf-8')

                        try:
                            y_m_d=datetime.now().strftime('%Y-%m-%d')
                            object_name=f"{table_name}/{y_m_d}/{filename}.json"
                            s3_client.put_object(Body=res_bytes, Bucket=BUCKET_NAME, Key=object_name)
                            return True
                        except ClientError as e:
                            return False
        finally:
            if conn:
                close_db_connection(conn)   
    else:
        latest_filename=list_of_files[-1]
        latest_fetchtime=latest_filename[-22:-5]
        
        query=""

        return {"base_time" : latest_fetchtime, "new_data" : False }




# Still TO DO
# periodically checks for new and updated data
# if the column 'last_updated' is newer than the last pull of data,
# then new data is grabbed/reformatted/written to ingestion bucket
    #       - use name to save times of last fetch
    #       - compare "last_updated" column in each table to see if any values are greater than the last fetch

