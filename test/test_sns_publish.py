from moto import mock_aws
from src.src_ingestion.sns_publish import sns_publish
import boto3
import pytest
import os


# Seting up AWS test suite


@pytest.fixture(scope="module")
def aws_credentials():
    """Mocked AWS Credentials for moto."""

    os.environ["AWS_ACCESS_KEY_ID"] = "testing"

    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"

    os.environ["AWS_SECURITY_TOKEN"] = "testing"

    os.environ["AWS_SESSION_TOKEN"] = "testing"

    os.environ["AWS_DEFAULT_REGION"] = "us-west-2"


# Mocking the sns client


@pytest.fixture(scope="function")
def mock_sns_client(aws_credentials):

    with mock_aws():

        yield boto3.client("sns", region_name="eu-west-2")


# Setup for creating mock SNS topic and email subscription


@pytest.fixture(scope="function")
def mock_sns_setup(mock_sns_client):

    response = mock_sns_client.create_topic(Name="Lambda_ingestion_topic")

    topic_arn = response["TopicArn"]

    mock_sns_client.subscribe(
        TopicArn=topic_arn, Protocol="email", Endpoint="test_example@something.com"
    )

    return mock_sns_client


# Unit test for sns_publish checking excecution of email being sent


def test_sns_publish_status_code(mock_sns_setup):

    mock_sns_client = mock_sns_setup

    result = sns_publish(mock_sns_client, "This is for testing")

    assert result["ResponseMetadata"]["HTTPStatusCode"] == 200
