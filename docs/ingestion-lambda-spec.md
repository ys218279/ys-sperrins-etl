# Ingestion Lambda Specification

## Overview
This Lambda Function will:
- Ingest data from the Totesys OLTP database when triggered
- Triggering will be orchestrated via a Step Function every 10 mins
- If any of the data collected is in an unexpected format or type an error will be logged to Cloudwatch
- The ingested data will be stored in an S3 bucket. The latest ID ingested for each table will be stored per table as part of the key for the stored data.


### ingestion-bucket contents
```
ingestion-bucket/address/1526-2024-11-11T15-03-24.sql
ingestion-bucket/address/latest.json
```

### latest.json contents
```json
{
    "latest-row": 1526,
    "timestamp": "2024-11-11T15-03-24",
    "rows-ingested": 35
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

get_table_data(table: str, row_id: int, connection) -> ????:
"""extracts data for the given table name for all rows with id > row id

Args:
    table (str): name of the table to query.
    row_id (int): row from which to collect data (exclusive)
    connection: ?????? 

Returns:
    ?????

Raises:
    ?????
"""

write_table_data(table: str, data: ????, client, bucket_name: str) -> dict:
"""writes table data to the given bucket, including a 'latest.json'

Args:
    table (str): name of the table data to store.
    data (???): data to store
    client: boto3 client
    bucket_name: name of bucket in which to store the data

Returns:
    result (dict): a dictionary reporting the result of the call e.g.
        {
        "success": True,
        "message": "35 lines of data successfully written to 'address' table,
        }

Raises:
    ?????
"""

```

## Output Format
Options for output format considered were:
- csv
- json lines
- parquet
- sql files
The first two would store a lot of the data in strings and may lose integrity when converting types. Parquet is more suited for analytics. We have decided to proceed with saving the ingested data as raw SQL.