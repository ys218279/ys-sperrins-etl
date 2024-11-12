# Ingestion Lambda Specification

## Overview
This Lambda Function will:
- Ingest data from the Totesys OLTP database when triggered
- Triggering will be orchestrated via a Step Function every 10 mins
- If any of the data collected is in an unexpected format or type an error will be logged to Cloudwatch
- The ingested data will be stored in an S3 bucket. The latest ID ingested for each table will be stored per table as part of the key for the stored data.

S3 keys for ingested data are in the format [table_name]/[latest_row_id]-[timestamp].jsonl

### ingestion-bucket contents
```
prod-ingestion-bucket/address/1491-2024-11-11T14-56-55.jsonl
prod-ingestion-bucket/address/1526-2024-11-11T15-03-24.jsonl
prod-ingestion-bucket/address/latest.json
```

### latest.json contents
```json
{
    "latest_row_id": 1526,
    "timestamp": "2024-11-11T15-03-24",
    "rows_ingested": 35
}
```


## Functions

```python
get_latest_id(table: str, client, bucket_name: str) -> dict:
"""gets latest row ingested for the given table

Args:
    table (str): name of the table to query
    client: boto3 client
    bucket_name (str): name of the bucket where the data is stored

Returns:
    row_id (int): the latest row of the table previously ingested
"""

get_table_data(table: str, row_id: int, connection) -> Dataframe:
"""extracts data for the given table name for all rows with id > row id

Args:
    table (str): name of the table to query.
    row_id (int): row from which to collect data (exclusive)
    connection: ?????? 

Returns:
    df (dataframe): a pandas dataframe containing the new data

Raises:
"""

write_table_data(table: str, data: Dataframe, client, bucket_name: str) -> dict:
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
```

## Output Format
Options for output format considered were:
- csv
- json lines - decided to go with this!
- parquet
- sql files

## Logging
The loading of each table will be logged to cloudwatch with details. Any errors will also be logged to cloudwatch.