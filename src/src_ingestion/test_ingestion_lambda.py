from unittest.mock import patch
import boto3
from moto import mock_aws
import pytest, json
import os
from datetime import datetime

with patch.dict(os.environ, {"S3_BUCKET_NAME": "test_bucket"}):
    from src.src_ingestion.ingestion_lambda import lambda_handler

@pytest.fixture(autouse=True)
def aws_credentials():
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"

@pytest.fixture(scope="function", autouse=True)
def test_mock_client():
    with mock_aws():
        client = boto3.client('s3')
        client.create_bucket(Bucket='my_test_bucket', 
                             CreateBucketConfiguration={'LocationConstraint': 'eu-west-2'})
        yield client


# def test_filename_is_fetched_correctly_from_s3_bucket(test_mock_client):
#     filename = datetime.now().strftime('%H%M%S')
#     y_m_d=datetime.now().strftime('%Y-%m-%d')
#     input_file = f"staff/{y_m_d}/{filename}.json"
#     test_dict = {"columns" : [1,2,3,4], "data" : ["insert here"]}
#     res_bytes = json.dumps(test_dict).encode('utf-8')
#     test_mock_client.put_object(Body=res_bytes, Bucket='my_test_bucket', Key=input_file)
#     response = lambda_handler(1,1,'my_test_bucket')
#     print("response:",response)
#     assert response["base_time"] == filename


def test_file_writes_to_s3_bucket(test_mock_client):
    input_key = "staff/2025_02_25/110314.json"
    test_dict = {"columns" : [1,2,3,4], "data" : ["insert here"]}
    res_bytes = json.dumps(test_dict).encode('utf-8')
    test_mock_client.put_object(Body=res_bytes, Bucket='my_test_bucket', Key=input_key)
    list_file_name = test_mock_client.list_objects_v2(Bucket='my_test_bucket')
    print(list_file_name)
    assert list_file_name['Contents'][0]['Key'] == input_key

def test_all_tables_writen_to_s3(test_mock_client):
    pass