import pandas as pd
import pytest
import boto3
from moto import mock_aws
from src.src_load.utils

test_data = pd.DataFrame({'id': [1, 2, 3], 'value': ['a', 'b', 'c']})

@pytest.fixture
def mock_s3_client():
    """Fixture to create and return a mocked S3 client."""
    with mock_aws():
        s3 = boto3.client("s3", region_name="us-east-1")
        bucket_name = "test-bucket"
        s3.create_bucket(Bucket=bucket_name)
        return s3, bucket_name

def test_transfer_from_parquet_to_df(mock_s3_client):
    """Test function to check if Parquet data is correctly loaded into DataFrame."""
    s3, bucket_name = mock_s3_client

    # Create an in-memory Parquet file
    parquet_buffer = io.BytesIO()
    test_data.to_parquet(parquet_buffer, engine="pyarrow")
    parquet_buffer.seek(0)

    # Upload to the mocked S3 bucket
    object_name = "test.parquet"
    s3.put_object(Bucket=bucket_name, Key=object_name, Body=parquet_buffer.getvalue())

    # Call the function under test
    df = transfer_from_parquet_to_df(object_name, s3, bucket_name)

    # Assertions
    pd.testing.assert_frame_equal(df, test_data)