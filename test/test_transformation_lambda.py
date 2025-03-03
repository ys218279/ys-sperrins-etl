import pytest
from moto import mock_aws
import boto3
import os
import json
from unittest.mock import patch

with patch.dict(os.environ, {"S3_BUCKET_NAME_INGESTION": "test_bucket_ingestion", "S3_BUCKET_NAME_PROCESSED": "test_bucket_processed"}):
    from src.src_ingestion.ingestion_lambda import lambda_handler

@pytest.fixture(scope='function', autouse=True)
def aws_credentials():
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
