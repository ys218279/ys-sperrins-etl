from src.src_load.load_utils import pd_read_s3_parquet

import boto3
import unittest
from unittest.mock import patch, Mock
from moto import mock_aws
import pytest
import pandas as pd
from io import BytesIO
from pandasql import sqldf


def test_pd_read_s3_parquet():
    with mock_aws():
        s3_client = boto3.client('s3', region_name='eu-west-2')
        s3_client.create_bucket(
                Bucket="test-bucket",
                CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
            )
        bucket_name = "test-bucket"
        test_data = {
                "calories": [420, 380, 390],
                "duration": [50, 40, 45]
                }
        df = pd.DataFrame(test_data)
        output_buffer = BytesIO()
        df.to_parquet(output_buffer)
        body = output_buffer.getvalue()
        s3_client.put_object(Bucket=bucket_name, Key='test_data_parquet', Body=body)
        res_df = pd_read_s3_parquet('test_data_parquet', bucket_name, s3_client)
        pd.testing.assert_frame_equal(res_df, df)

def test_get_column_names():
    pysqldf = lambda q: sqldf(q, globals())
    data = {'currency_id':[1, 2], 'currency_code':[1, 2], "currency_name": [1, 2]}
    df = pd.DataFrame(data)
    # pysqldf("INSERT INTO df ('currency_id', 'currency_code', 'currency_name') VALUES (1,2,3);")
    
    res = pysqldf(query)
    return res