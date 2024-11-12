from src.utils.get_latest_id import get_latest_id # H&M

from moto import mock_aws
import os
import boto3
import pytest
import json


@pytest.fixture(scope="function")
def aws_credentials():
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"


@pytest.fixture(scope="function")
def s3_client(aws_credentials):
    with mock_aws():
        yield boto3.client("s3")


@pytest.fixture(scope="function")
def test_bucket_with_data(aws_credentials, s3_client):
    test_bucket_name = "test-espresso-bucket"
    test_table_name = "address"
    s3_client.create_bucket(
        Bucket=test_bucket_name,
        CreateBucketConfiguration={
            "LocationConstraint": "eu-west-2",
        },
    )
    latest = {
        "latest_row_id": 1526,
        "timestamp": "2024-11-11T15-03-24",
        "rows_ingested": 35,
    }
    s3_client.put_object(
        Bucket=test_bucket_name,
        Key=f"{test_table_name}/latest.json",
        Body=json.dumps(latest).encode("utf-8"),
    )


class TestGetLatestIdFunction:
    def test_json_data_is_retrieved_from_bucket(
        self,
        aws_credentials,
        s3_client,
        test_bucket_with_data,
    ):
        # result = s3_client.get_object(
        #     Bucket="test-espresso-bucket",
        #     Key="address/latest.json",
        # )
        # latest_ingestion = json.loads(
        #     result["Body"].read().decode('utf-8')
        #     )

        result = get_latest_id(
            "address",
            s3_client,
            "test-espresso-bucket",
        )

        assert result == 1526