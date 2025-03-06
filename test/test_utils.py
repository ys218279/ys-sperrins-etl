from src.src_ingestion.utils import (
    get_s3_client,
    get_secrets_manager_client,
    upload_to_s3,
    fetch_latest_update_time_from_s3,
    fetch_latest_update_time_from_db,
    retrieval,
)

from src.src_load.utils import (
    load_retrieval
)

import boto3
import unittest
from unittest.mock import patch, Mock
from moto import mock_aws
import json
from botocore.exceptions import ClientError
import io
import logging
import datetime
from pg8000.native import Connection

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
    # yield "abc"
    



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

    @patch("builtins.input")
    def test_retrieval_successful_return_dict(self, mock_input):
        with mock_aws():
            client = boto3.client("secretsmanager", region_name="eu-west-2")
            with patch("sys.stdout", new=io.StringIO()) as fake_out:
                entry(client)
                res = retrieval(client)
                mock_input.input_args = ["de_2024_12_02"]
                assert res == {
                    "username": "test",
                    "password": "test",
                    "host": "test",
                    "database": "test",
                    "port": "test",
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


def entry(client,secret_identifier = "de_2024_12_02"):
    """will only be used once to create the initial TEST secret"""
    if "SecretsManager" in str(type(client)):
        # secret_identifier = "de_2024_12_02"
        get_username = "test"
        get_password = "test"
        get_host = "test"
        get_database = "test"
        get_port = "test"
        secret_value = {
            "username": get_username,
            "password": get_password,
            "host": get_host,
            "database": get_database,
            "port": get_port,
        }
        secret_string = json.dumps(secret_value)
        try:
            client.create_secret(Name=secret_identifier, SecretString=secret_string)
            print("Secret saved.")
        except client.exceptions.ResourceExistsException as e:
            print("Secret already exists!")
        except Exception as err:
            print({"ERROR": err, "message": "Fail to connect to aws secret manager!"})
    else:
        print("invalid client type used for secret manager! plz contact developer!")

class TestLoadLambdaRetrieval:
    @patch("builtins.input", side_effect=input_args())
    def test_load_retrieval_successfully_gets_a_secret(self, mock_input):
        mock_input.input_args = ["fake_db"]
        with mock_aws():
            client = boto3.client("secretsmanager", region_name="eu-west-2")
            entry(client,secret_identifier="totesys_data_warehouse_olap")
            res = load_retrieval(client)
            assert res is not None

    @patch("builtins.input")
    def test_load_retrieval_successful_return_dict(self,mock_input):
        with mock_aws():
            client = boto3.client("secretsmanager", region_name="eu-west-2")
            with patch("sys.stdout", new=io.StringIO()):
                entry(client,secret_identifier="totesys_data_warehouse_olap")
                res = load_retrieval(client)
                mock_input.input_args = ["fake_tote_dw"]
                assert res == {
                    "username": "test",
                    "password": "test",
                    "host": "test",
                    "database": "test",
                    "port": "test",
                }

    @patch("builtins.input")
    def test_load_retrieval_secret_doesnot_exist(self, mock_input):
        with mock_aws():
            client = boto3.client("secretsmanager", region_name="eu-west-2")
            with patch("sys.stdout", new=io.StringIO()) as fake_out:
                load_retrieval(client)
                result = fake_out.getvalue()
                assert (
                    "An error occurred (ResourceNotFoundException) when calling the GetSecretValue operation"
                    in result
                )
