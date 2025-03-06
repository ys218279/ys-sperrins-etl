from src.src_ingestion.utils import (
    get_s3_client,
    get_secrets_manager_client,
    upload_to_s3,
    fetch_latest_update_time_from_s3,
    fetch_latest_update_time_from_db,
    fetch_snapshot_of_table_from_db,
    entry,
    retrieval,
)
import boto3
import unittest
from unittest.mock import patch, Mock
from moto import mock_aws
import json
from botocore.exceptions import ClientError
import io
import os
import pytest
import datetime

class TestGetS3Client(unittest.TestCase):
    def test_get_s3_client_success(self):
        client = get_s3_client()
        assert "S3" in str(type(boto3.client("s3")))

    @patch("boto3.client")
    def test_get_s3_client_fail(self, mock_boto_client):
        mock_boto_client.side_effect = ClientError(
            {"Error": {"Code": "InternalError", "Message": "Simulated error"}},
            "ListObjects",
        )
        with self.assertRaises(ClientError) as context:
            get_s3_client()
        assert "failed to connect to s3" in str(context.exception)


class TestGetSMClient(unittest.TestCase):
    def test_get_s3_client_success(self):
        client = get_secrets_manager_client()
        assert "SecretsManager" in str(type(boto3.client("secretsmanager", region_name="eu-west-2")))

    @patch("boto3.client")
    def test_get_s3_client_fail(self, mock_boto_client):
        mock_boto_client.side_effect = ClientError(
            {"Error": {"Code": "InternalError", "Message": "Simulated error"}},
            "ListObjects",
        )
        with self.assertRaises(ClientError) as context:
            get_secrets_manager_client()
        assert "failed to connect to secret manager" in str(context.exception)


class TestUploadS3:
    def test_upload_to_s3(self):
        with mock_aws():
            client = boto3.client("s3", region_name="eu-west-2")
            client.create_bucket(
                Bucket="test-bucket",
                CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
            )
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
            client = boto3.client("s3", region_name="eu-west-2")
            bucket_name = "test-bucket"
            client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
            )
            objects = [
                "table/20250301174108.json",
                "table/20250302140516.json",
                "table/20250103131459.json",
            ]
            for i in objects:
                client.put_object(Bucket=bucket_name, Key=i, Body="test")
            assert (
                fetch_latest_update_time_from_s3(client, bucket_name, "table")
                == 20250302140516
            )

class TestFectchLatestUpdateDB:
    def test_fetch_latest_upload_when_s3_is_empty(self):
        mock_conn = Mock()
        mock_conn.run.return_value = [[datetime.datetime(2022, 11, 3, 14, 20, 49, 962000)]]
        result = fetch_latest_update_time_from_db(mock_conn, "mock_table")
        assert result == 20221103142049

def input_args():
    yield "bidenj"
    yield "Pa55word"
    yield "host"
    yield "database"
    yield "port"
    yield "bidenj"
    yield "Pa55word"
    yield "host"
    yield "database"
    yield "port"


def input_args_2():
    yield "bidenj"
    yield "Pa55word"
    yield "host"
    yield "database"
    yield "port"
    yield "abc"


class TestEntry:
    @patch("builtins.input", side_effect=input_args())
    def test_entry_successful(self, mock_input):
        with mock_aws():
            client = boto3.client("secretsmanager", region_name="eu-west-2")
            with patch("sys.stdout", new=io.StringIO()) as fake_out:
                entry(client)
                secret = client.get_secret_value(SecretId="de_2024_12_02")
                assert secret is not None

    @patch("builtins.input", side_effect=input_args())
    def test_entry_fails(self, mock_input):
        with mock_aws():
            client = boto3.client("s3", region_name="eu-west-2")
            with patch("sys.stdout", new=io.StringIO()) as fake_out:
                entry(client)
                result = fake_out.getvalue()
                assert (
                    "invalid client type used for secret manager! plz contact developer!"
                    in result
                )

    @patch("builtins.input", side_effect=input_args())
    def test_entry_successfully_stored(self, mock_input):
        with mock_aws():
            client = boto3.client("secretsmanager", region_name="eu-west-2")
            entry(client)
            response = client.list_secrets()
            assert len(response["SecretList"]) == 1

    @patch("builtins.input", side_effect=input_args())
    def test_secret_already_exists(self, mock_input):
        with mock_aws():
            client = boto3.client("secretsmanager", region_name="eu-west-2")
            entry(client)
            with patch("sys.stdout", new=io.StringIO()) as fake_out:
                entry(client)
                result = fake_out.getvalue()
                assert "Secret already exists!" in result


class TestRetrieval:
    @patch("builtins.input", side_effect=input_args())
    def test_retrieval_successful_1_secret(self, mock_input):
        mock_input.input_args = ["de_2024_12_02"]
        with mock_aws():
            client = boto3.client("secretsmanager", region_name="eu-west-2")
            entry(client)
            res = retrieval(client)
            assert res is not None

    @patch("builtins.input", side_effect=input_args())
    def test_retrieval_successful_return_dict(self, mock_input):
        with mock_aws():
            client = boto3.client("secretsmanager", region_name="eu-west-2")
            with patch("sys.stdout", new=io.StringIO()) as fake_out:
                entry(client)
                res = retrieval(client)
                mock_input.input_args = ["de_2024_12_02"]
                assert res == {
                    "username": "bidenj",
                    "password": "Pa55word",
                    "host": "host",
                    "database": "database",
                    "port": "port",
                }

    @patch("builtins.input")
    def test_retrieval_secret_doesnot_exist(self, mock_input):
        with mock_aws():
            client = boto3.client("secretsmanager", region_name="eu-west-2")
            with patch("sys.stdout", new=io.StringIO()) as fake_out:
                retrieval(client)
                result = fake_out.getvalue()
                assert (
                    "An error occurred (ResourceNotFoundException) when calling the GetSecretValue operation"
                    in result
                )

class TestFetchSnapshotOfWholeTable:
    def test_returns_dictionary_result_with_columns_and_data_keys(self, ):
        mock_conn = Mock()
        mock_conn.run.return_value = [1,"Jeremie","Franey",2,"email"]
        mock_conn.columns = [{"name": "id"},{"name": "first_name"},{"name": "last_name"},{"name": "department_id"},{"name": "email"}]
        result = fetch_snapshot_of_table_from_db(mock_conn, "mock_table")
        assert type(result) == dict
        assert result["columns"]
        assert result["data"]

