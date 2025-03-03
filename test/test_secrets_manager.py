from src.src_ingestion.secrets_manager import retrieval
import pytest
import boto3
from unittest.mock import patch
from moto import mock_aws
import io
import os
import json


@pytest.fixture(scope="module", autouse=True)
def aws_credentials():
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"


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


class TestRetrieval:

    @patch("builtins.input", side_effect=input_args())
    def test_retrieval_successful_1_secret(self, mock_input):
        with mock_aws():
            client = boto3.client("secretsmanager")
            with patch("sys.stdout", new=io.StringIO()) as fake_out:
                secret_identifier = "de_2024_12_02"
                get_username = input('Please enter your username:')
                get_password = input("Please enter your password:")
                get_host = input("Please enter your host:")
                get_database = input("Please enter your database:")
                get_port = input("Please enter your port:")
                secret_value = {"username": get_username,
                                "password": get_password,
                                "host": get_host,
                                "database": get_database,
                                "port": get_port}
                secret_string = json.dumps(secret_value)
                client.create_secret(Name=secret_identifier, SecretString=secret_string)
                retrieval(client)
                mock_input.input_args = ["de_2024_12_02"]
                result = fake_out.getvalue()
                assert "Secrets returned as dictionary" in result

    @patch("builtins.input", side_effect=input_args())
    def test_retrieval_successful_return_dict(self, mock_input):
        with mock_aws():
            client = boto3.client("secretsmanager")
            with patch("sys.stdout", new=io.StringIO()) as fake_out:
                secret_identifier = "de_2024_12_02"
                get_username = input('Please enter your username:')
                get_password = input("Please enter your password:")
                get_host = input("Please enter your host:")
                get_database = input("Please enter your database:")
                get_port = input("Please enter your port:")
                secret_value = {"username": get_username,
                                "password": get_password,
                                "host": get_host,
                                "database": get_database,
                                "port": get_port}
                secret_string = json.dumps(secret_value)
                client.create_secret(Name=secret_identifier, SecretString=secret_string)
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
            client = boto3.client("secretsmanager")
            with patch("sys.stdout", new=io.StringIO()) as fake_out:
                retrieval(client)
                result = fake_out.getvalue()
                assert (
                    "An error occurred (ResourceNotFoundException) when calling the GetSecretValue operation"
                    in result
                )
