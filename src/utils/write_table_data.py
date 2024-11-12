import pandas as pd

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