import pytest
from moto import mock_aws
import boto3
import os
import json
from freezegun import freeze_time
from unittest.mock import patch

with patch.dict(os.environ, {"S3_BUCKET_NAME_INGESTION": "test_bucket_ingestion", "S3_BUCKET_NAME_PROCESSED": "test_bucket_processed"}):
    from src.src_transform.transform_lambda import lambda_handler

class DummyContext:
    pass


@pytest.fixture(scope="function")
def lambda_event():
    return {'department': False,
            'transaction': False,
            'payment': False,
            'design': 'design/2025-03-03/131223.json',
            'address': 'address/2025-03-01/071556.json',
            'staff': False,
            'counterparty': False,
            'currency': False,
            'sales_order': False}


@freeze_time("2024-04-01 12:00")
def test_handler_writes_objects_to_s3(lambda_event, 
                                      s3_client, 
                                      create_bucket, 
                                      create_object_design, 
                                      bucket_name, 
                                      object_key_design, 
                                      bucket_name_processed, 
                                      create_bucket_processed,
                                      create_object):
    with mock_aws():
        context = DummyContext()
        lambda_handler(lambda_event, context)
        bucket_data = s3_client.list_objects_v2(Bucket="test_bucket_processed")
        assert bucket_data['KeyCount'] == 3
        assert bucket_data["Contents"][0]["Key"] == 'dim_date/2024-04-01/120000.json'
        assert bucket_data["Contents"][1]["Key"] == 'dim_design/2024-04-01/120000.json'
        assert bucket_data["Contents"][2]["Key"] == 'dim_location/2024-04-01/120000.json'

