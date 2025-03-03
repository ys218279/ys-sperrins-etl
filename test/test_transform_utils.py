import pytest
from moto import mock_aws
import boto3
import os
import json
from src.src_transform.transform_utils import get_s3_object, convert_s3_obj_to_df, convert_df_to_s3_obj


@pytest.fixture(scope='function', autouse=True)
def aws_credentials():
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

@pytest.fixture()
def s3_client():
    with mock_aws():
        yield boto3.client('s3', region_name="eu-west-2")

@pytest.fixture()
def bucket_name():
    return 'test_bucket'

@pytest.fixture
def create_bucket(s3_client, bucket_name):
    s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint':'eu-west-2'})

@pytest.fixture()
def object_key():
    return 'address/2025-03-01/071556.json'

@pytest.fixture()
def object_body():
    return {
    "columns": [
        "department_id",
        "department_name",
        "location",
        "manager",
        "created_at",
        "last_updated"
    ],
    "data": [
        [
            1,
            "Sales",
            "Manchester",
            "Richard Roma",
            "2022-11-03 14:20:49.962000",
            "2022-11-03 14:20:49.962000"
        ],
        [
            2,
            "Purchasing",
            "Manchester",
            "Naomi Lapaglia",
            "2022-11-03 14:20:49.962000",
            "2022-11-03 14:20:49.962000"
        ],
        [
            3,
            "Production",
            "Leeds",
            "Chester Ming",
            "2022-11-03 14:20:49.962000",
            "2022-11-03 14:20:49.962000"
        ] 
    ]
    }

@pytest.fixture
def create_object(s3_client, bucket_name, object_key, object_body):
    obj_json = json.dumps(object_body, indent=4, sort_keys=True, default=str)
    obj_bytes = obj_json.encode('utf-8')
    s3_client.put_object(Bucket=bucket_name, Key=object_key, Body=obj_bytes)

class TestGetS3Object:

    def test_get_s3_object_can_access_files_as_dict(self, s3_client, create_bucket, create_object, bucket_name, object_key):
        with mock_aws():
            response = get_s3_object(s3_client, bucket_name, object_key)
            assert isinstance(response, dict)
            assert "columns" in response
            assert "data" in response

    def test_get_s3_object_creates_dict_with_correct_schema(self, s3_client, create_bucket, create_object, bucket_name, object_key):
        with mock_aws():
            response = get_s3_object(s3_client, bucket_name, object_key)
            assert "department_id" in response["columns"]
            assert len(response["columns"]) is 6
            assert "Sales" in response["data"][0]
            assert len(response["data"][0]) is 6
            assert isinstance(response["data"][0][0], int)



class TestConvertS3ToDF:
    
    def test_convert_s3_obj_to_df_can_create_df(self, s3_client, bucket_name, object_key, create_bucket, create_object):
        with mock_aws():
            s3_obj = get_s3_object(s3_client, bucket_name, object_key)
            response = convert_s3_obj_to_df(s3_obj)
            assert isinstance(response, object)
            assert len(response) is 3
            assert "department_id" in response
            assert "department_name" in response
            assert "location" in response
            assert "manager" in response

            
class TestConvertDFToS3:

    def test_convert_df_to_s3_object(self, s3_client, bucket_name, object_key, create_bucket, create_object):
        with mock_aws():
            s3_obj = get_s3_object(s3_client, bucket_name, object_key)
            df = convert_s3_obj_to_df(s3_obj)
            convert_df_to_s3_obj(s3_client, df, bucket_name, object_key)
            listing = s3_client.list_objects_v2(Bucket=bucket_name)
            assert len(listing["Contents"]) == 1
            assert listing["Contents"][0]["Key"] == object_key