

import os
from datetime import datetime
from pg8000.native import identifier
from connection import connect_to_db, close_db_connection
from utils import upload_to_s3, get_s3_client, fetch_latest_update_time_from_s3, fetch_latest_update_time_from_db


BUCKET_NAME = os.environ["S3_BUCKET_NAME"]

def lambda_handler(event, context, BUCKET_NAME=BUCKET_NAME):
    '''Ingestion Lambda to put the latest data from ToteSys in the ingestion_zone_S3 bucket. 

    Required Input Arguments:
    BUCKET_NAME = The S3 Bucket Name that the handler will write to. 
        - Defaults to the available ENVIRONMENT VARIABLE: "S3_BUCKET_NAME".

    Returned Output:
    Output dictionary with 11 key-value pairs:
        - Each Key is the name of the Table being ingested from ToteSys DB.
        - Each Value is either:
            (a) the filepath to the latest object that was written to s3 during the last fetch.
            (b) False: if no new file was uploaded during the last fetch.
    
    This lambda will SELECT data from the ToteSys Database and:
    For each table in the database, it will:
        - load the data in to a dictionary with two keys:
            "columns" : <list of table headers>
            "data" : <contains raw data as a list of lists. Each list is one row of the table.>
        - opens a temporary file in lambda's /tmp dir and dumps the data there in json format
        - uploads that file object to the s3 bucket using the following format:
            - table_name/year-month-day-timestamp.json (i.e. YYYYMMDDHHMMSS.json)
        - finally this lambda will close the db conn.

    Important Notes: 
        - Any data in a datetime format when extracted from ToteSys is coverted in to a integer format.
        - Within the uploaded file: any data fields that had None have been converted to 'null' values.
    '''
    
    conn = connect_to_db()
    client = get_s3_client()
    raw_table_list =conn.run("SELECT * from information_schema.tables")
    table_list = [item[2] for item in raw_table_list if item[1] == 'public'][1:]
    output = {}
    for table in table_list:
        latest_update_s3 = fetch_latest_update_time_from_s3(client, BUCKET_NAME, table)
        latest_update_db = fetch_latest_update_time_from_db(conn, table)
        if latest_update_db > latest_update_s3:
            latest_update_s3_dt = datetime.strptime(str(latest_update_s3), "%Y%m%d%H%M%S")
            raw_data = conn.run(f"SELECT * FROM {identifier(table)} WHERE last_updated > :latest_update_s3_dt", latest_update_s3_dt=latest_update_s3_dt)
            columns = [col['name'] for col in conn.columns]
            result = {"columns" : columns, "data" : raw_data}
            filename = datetime.now().strftime('%H%M%S')
            object_name = upload_to_s3(BUCKET_NAME, table, result)
            output[table] = object_name
        else:
            output[table] = False
    close_db_connection(conn)
    return output

# if __name__ == "__main__":
#     import sys
#     sys.path.append('src/src_ingestion')