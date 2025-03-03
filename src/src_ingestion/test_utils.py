from src.src_ingestion.utils import get_s3_client, get_secrets_manager_client, list_s3_objects, upload_to_s3, fetch_latest_update_time_from_s3, fetch_latest_update_time_from_db
import pytest
import boto3
from unittest.mock import patch
from moto import mock_aws
import io
import os
from src.src_ingestion.connection import connect_to_db, close_db_connection
import json

@pytest.fixture(scope="module", autouse=True)
def aws_credentials():
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"

class TestUploadS3:
    def test_upload_to_s3(self):
        with mock_aws():
            client = boto3.client('s3', region_name="eu-west-2")
            client.create_bucket(Bucket="test-bucket", CreateBucketConfiguration={"LocationConstraint": "eu-west-2"})
            bucket_name = "test-bucket"
            table = "table"
            result = {"key": "value"}
            object_name = upload_to_s3(bucket_name, table, result)
            # Verify the object was uploaded
            response = client.list_objects_v2(Bucket=bucket_name)
            assert "Contents" in response
            keys = [obj["Key"] for obj in response["Contents"]]
            assert object_name in keys
            # Verify the content
            s3_object = client.get_object(Bucket=bucket_name, Key=object_name)
            content = json.loads(s3_object["Body"].read().decode("utf-8"))
            assert content == result

class TestFetchLatestUpdateS3:
    def test_fetch_latest_update_time_from_s3(self):
        with mock_aws():
            client = boto3.client('s3', region_name="eu-west-2")
            bucket_name = "test-bucket"
            client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={"LocationConstraint": "eu-west-2"})
            objects = ['table/20250301174108', 'table/20250302140516', 'table/20250103131459']
            for i in objects:
                client.put_object(Bucket=bucket_name, Key=i, Body="test")
            assert fetch_latest_update_time_from_s3(client, bucket_name, 'table') == 20250302140516

    def test_fetch_latest_upload_when_s3_is_empty(self):
        with mock_aws():
            client = boto3.client('s3', region_name="eu-west-2")
            bucket_name = "test-bucket"
            client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={"LocationConstraint": "eu-west-2"})
            assert fetch_latest_update_time_from_s3(client, bucket_name, 'table') == 20000101000001

# @pytest.fixture()
# def db():
#     db = connect_to_db()
#     yield db
#     close_db_connection(db)

# class TestFetchLastUpdateDB:
#     #this test cannot connect to aws, duno why
#     def test_fetch_latest_update_time_from_db(self):
#         conn = connect_to_db()
#         table = 'address'
#         res = fetch_latest_update_time_from_db(table, conn)
#         assert res == 20221103142049



