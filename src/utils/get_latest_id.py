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
