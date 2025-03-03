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

import os
from datetime import datetime
from pg8000.native import identifier
from connection import connect_to_db, close_db_connection
from pprint import pprint
from utils import list_s3_objects, upload_to_s3, get_s3_client, fetch_latest_update_time_from_s3, fetch_latest_update_time_from_db
import sys
sys.path.append('src/src_ingestion')

BUCKET_NAME = os.environ["S3_BUCKET_NAME"]

# if statement: uses s3_client to 
    # (a) check for any files - if no files, then grab a whole snapshot of the data
    # (b) else take the last file ... and enter the new section of logic below:    
    
    # list_of_files = [response['Contents'][i]['Key'] for i in range(len(response['Contents']))]

# def lambda_handler(event, context, BUCKET_NAME=BUCKET_NAME):
#     conn = connect_to_db()
#     client = get_s3_client()
#     response = list_s3_objects(client, BUCKET_NAME)
#     if 'Contents' not in response:
#         raw_table_list =conn.run("SELECT * from information_schema.tables")
#         table_list = [item[2] for item in raw_table_list if item[1] == 'public'][1:]
#         for table in table_list:
#             raw_data = conn.run(f"SELECT * FROM {identifier(table)}")
#             columns = [col['name'] for col in conn.columns]
#             result = {"columns" : columns, "data" : raw_data}
#             filename = datetime.now().strftime('%H%M%S')
#             upload_to_s3(BUCKET_NAME, table, result)
#         return {"base_time": filename, "new_data": False}

def lambda_handler(event, context, BUCKET_NAME=BUCKET_NAME):
    conn = connect_to_db()
    client = get_s3_client()
    # response = list_s3_objects(client, BUCKET_NAME)
    raw_table_list =conn.run("SELECT * from information_schema.tables")
    table_list = [item[2] for item in raw_table_list if item[1] == 'public'][1:]
    output = {}
    for table in table_list:
        latest_update_s3 = fetch_latest_update_time_from_s3(client, BUCKET_NAME)
        latest_update_db = fetch_latest_update_time_from_db(conn, table)
        if latest_update_db > latest_update_s3:
            latest_update_s3_dt = datetime.strptime(latest_update_s3, "%Y%m%d%H%M%S")
            raw_data = conn.run(f"SELECT * FROM {identifier(table)} WHERE last_updated > :last_update_s3_dt'", latest_update_s3_dt=latest_update_s3_dt)
            columns = [col['name'] for col in conn.columns]
            result = {"columns" : columns, "data" : raw_data}
            filename = datetime.now().strftime('%H%M%S')
            object_name = upload_to_s3(BUCKET_NAME, table, result)
            output[table] = object_name
        else:
            output[table] = False
    return output
    

    # if 'Contents' not in response:
    #     for table in table_list:
    #         raw_data = conn.run(f"SELECT * FROM {table}")
    #         columns = [col['name'] for col in conn.columns]
    #         result = {"columns" : columns, "data" : raw_data}
    #         filename = datetime.now().strftime('%H%M%S')
    #         upload_to_s3(BUCKET_NAME, table, result)
    #     return {"base_time": filename, "new_data": False}
    # else:
    #     for table in table_list:

            
#         try:
#             client = boto3.client('secretsmanager')
#             conn = connect_to_db(client)

#             raw_table_list =conn.run("SELECT * from information_schema.tables")
#             table_list = [item[2] for item in raw_table_list if item[1] == 'public']
#             for table_name in table_list:
#                 if table_name[0] != "_":
#                     raw_data = conn.run(f"SELECT * FROM {identifier(table_name)}")
#                     columns = [col['name'] for col in conn.columns]
#                     result = {"columns" : columns, "data" : raw_data}
#                     filename = datetime.now().strftime('%H%M%S')

#                     with open(f'{filename}.json','w') as f:
#                         filedatain = json.dumps(result, indent=4, sort_keys=True, default=str)
#                         res_bytes = filedatain.encode('utf-8')

#                         try:
#                             y_m_d=datetime.now().strftime('%Y-%m-%d')
#                             object_name=f"{table_name}/{y_m_d}/{filename}.json"
#                             s3_client.put_object(Body=res_bytes, Bucket=BUCKET_NAME, Key=object_name)
#                             return True
#                         except ClientError as e:
#                             return False
#         finally:
#             if conn:
#                 close_db_connection(conn)   
#     else:
#         latest_filename=list_of_files[-1]
#         latest_fetchtime=latest_filename[-22:-5]
        
#         query=""

#         return {"base_time" : latest_fetchtime, "new_data" : False }


# # Still TO DO
# # periodically checks for new and updated data
# # if the column 'last_updated' is newer than the last pull of data,
# # then new data is grabbed/reformatted/written to ingestion bucket

# if __name__ == "__main__":
#     lambda_handler(BUCKET_NAME=BUCKET_NAME)