import pandas as pd
import json


def get_latest_id(table: str, client, bucket_name: str) -> dict:
    """gets latest row ingested for the given table

    Args:
        table (str): name of the table to query
        client: boto3 client
        bucket_name (str): name of the bucket where the data is stored

    Returns:
        row_id (int): the latest row of the table previously ingested
    """
    result = client.get_object(
        Bucket=bucket_name,
        Key=f"{table}/latest.json",
    )
    latest_ingestion = json.loads(
        result["Body"].read().decode('utf-8')
        )
    return latest_ingestion["latest_row_id"]

def get_table_data(table: str, row_id: int, connection) -> pd.DataFrame:
    """extracts data for the given table name for all rows with id > row id

    Args:
        table (str): name of the table to query.
        row_id (int): row from which to collect data (exclusive)
        connection: ??????

    Returns:
        df (dataframe): a pandas dataframe containing the new data

    Raises:
    """
    pass


def write_table_data(table: str, data: pd.DataFrame, client, bucket_name: str) -> dict:
    """writes table data to the given bucket in json lines format, including a 'latest.json'

    Args:
        table (str): name of the table data to store.
        data (dataframe): data to store
        client: boto3 client
        bucket_name: name of bucket in which to store the data

    Returns:
        result (dict): a dictionary reporting the result of the call e.g.
            {
            "success": True,
            "message": "35 lines of data successfully written to 'address' table,
            }

    Raises:
    """
    pass
