from moto import mock_aws
from utilities.error_logging import cloudwatch,sns
from botocore.exceptions import ClientError
import boto3
import pytest
import os,logger

@pytest.fixture(scope="module")
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-west-2"

@pytest.fixture(scope="function")
def mock_cloudwatch_client(aws_credentials):
    with mock_aws():
        yield boto3.client("cloudwatch", region_name="us-west-2")

@pytest.fixture(scope="function")
def mock_cloudwatchlogs_client(aws_credentials):
    with mock_aws():
        yield boto3.client("logs", region_name="us-west-2")

#mock aws 
#create a mock lambda that creates a simple response 
# write cloud watch script and test
# try execute it see if it appears anywhere is cloud watch

def lambda_handler(event, context):
    logger.setLevel(logging.DEBUG)
    logger.debug("This is a sample DEBUG message.. !!")
    logger.error("This is a sample ERROR message.... !!")
    logger.info("This is a sample INFO message.. !!")
    logger.critical("This is a sample 5xx error message.. !!")

def test_cloudwatch(aws_credentials,mock_cloudwatch_client):
    pass