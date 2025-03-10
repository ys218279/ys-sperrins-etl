import boto3, json, io, sys, logging
from botocore.exceptions import ClientError
from pg8000.native import Connection, identifier, InterfaceError
import pandas as pd

sys.path.append("src/src_load")

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def retrieval(client, secret_identifier='totesys_data_warehouse_olap'):
    """Return the credentials to the final Data Warehouse as a dictionary.
    
    Required input arguments:
    - client = secrets manager client
    - secret identifier (default = "totesys_data_warehouse_olap")

    Returns:
    - credentials required for connecting to db as dictionary containing key:value pairs

    Errors logged and raised:
    - Resource Not Found
    - Client Errors from AWS side.
    """  
    try:
        response = client.get_secret_value(SecretId=secret_identifier)
        res_str = response["SecretString"]
        res_dict = json.loads(res_str)
        return res_dict
    except client.exceptions.ResourceNotFoundException as err:
        print(err)
        logger.warning("Secret does not exist, %s", str(err))
    except Exception as err:
        print({"ERROR": err, "message": "Error detected and logged!"})
        logger.critical("There has been a critical error when attempting to retrieve secret for Data Warehouse credentials, %s", str(err))

def get_s3_client():
    """Creates s3 client returns client
    
    Return:
    - boto3.client: S3 client object
    """
    try:
        client = boto3.client("s3", region_name="eu-west-2")
        return client
    except ClientError:
        raise ClientError(
            {
                "Error": {
                    "Code": "FailedToConnect",
                    "Message": "failed to connect to s3",
                }
            },
            "GetS3Client",
        )



def get_secrets_manager_client():
    """Creates secrets manager client returns client
    
    Return:
    - boto3.client: secrets manager client object
    """
    try:
        client = boto3.client("secretsmanager", region_name="eu-west-2")
        return client
    except ClientError:
        raise ClientError(
            {
                "Error": {
                    "Code": "FailedToConnect",
                    "Message": "failed to connect to secret manager",
                }
            },
            "GetSecretsManagerClient",
        )


def pd_read_s3_parquet(key, bucket, s3_client):
    """Gets the parquet from s3 bucket, returns dataframe
    
    Keyword arguments:
    - key (str): object name of the parquet
    - bucket_name (str): Name for the processing bucket
    - s3_client (boto3.client): s3 client
    
    Returns:
    - df
    """
    try:
        obj = s3_client.get_object(Bucket=bucket, Key=key)
        df = pd.read_parquet(io.BytesIO(obj['Body'].read()), engine='pyarrow')
        return df
    except Exception as err:
        logger.critical("There has been a critical error when attempting to read the parquet from s3 bucket, %s", str(err))

def connect_to_dw(client):
    """return conn to dw"""
    try:
        credentials = retrieval(client)
        return Connection(
            user=credentials["username"],
            password=credentials["password"],
            database=credentials["database"],
            host=credentials["host"],
        )
    except Exception as err:
        logger.critical("The connection to the Data Warehouse is failing, %s", str(err))

def close_dw_connection(conn):
    """close dw"""
    conn.close()

def load_tables_to_dw(conn, df, table_name, fact_tables):
    """Load dataframe to data warehouse
    
    Keyword arguments:
    - conn (Connection): connection to dw
    - table_name (str): Name for the table
    - fact_tables (list): list of fact tables
    """
    try:
        column_names = get_column_names(conn, table_name)
        on_conflict = table_name not in fact_tables
        update_query = get_insert_query(table_name, column_names, df.index.name, on_conflict=on_conflict)
        for row in df.reset_index().to_dict(orient="records"):
            conn.run(update_query, **row, table_name=table_name)
    except Exception as err:
        logger.critical("Unable to load table, %s, to Data Warehouse, %s", str(table_name),  str(err))



def get_insert_query(table_name, column_names, conflict_column, on_conflict):
    """Given table name and column names of the table return the conditional query
    
    Keyword arguments:
    - table_name (str): name of the table
    - column_names (list): column names of the table
    - on_conflict (bool): fact table or not
    
    Returns:
    - query (string)
    """
    column_names = column_names[1:] if not on_conflict else column_names
    placeholders = ", ".join([f":{column_name}" for column_name in column_names])
    column_names_with_identifier = [f"{identifier(column_name)}" for column_name in column_names]
    columns = ", ".join(column_names_with_identifier)
    update_set = ", ".join([f"{col} = EXCLUDED.{col}" for col in column_names[1:]])
    query = f"""INSERT INTO {table_name} ({columns})
    VALUES ({placeholders})"""
    if not on_conflict:
        return f"{query};"
    return f"""{query}
    ON CONFLICT ({identifier(conflict_column)})
    DO UPDATE SET {update_set};
    """

def get_column_names(conn, table_name):
    """Given table name return a list of column names
    
    Keyword arguments:
    - conn (Connection): connection to dw
    - table_name (str): name of the table
    
    Returns:
    - column_names (list)
    """
    query = """
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = :table_name;
    """
    result = conn.run(query, table_name=table_name)
    return [row[0] for row in result]


def delete_all_from_dw():
    """delete all contents in dw but will keep the table structure (column names)"""
    conn = connect_to_dw()
    tables = ['fact_sales_order', 'dim_date', 'dim_staff', 'dim_counterparty', 'dim_location', 'dim_currency', 'dim_design']
    for table in tables:
        query = f"DELETE FROM {identifier(table)};"
        conn.run(query)

if __name__ == "__main__":
    delete_all_from_dw()
