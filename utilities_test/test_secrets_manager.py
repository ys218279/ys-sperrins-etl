from utilities.secrets_manager import entry, retrieval
import pytest
import boto3
from unittest.mock import patch
from moto import mock_aws
import io

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

class TestUtilsEntry:
    @patch("builtins.input", side_effect=input_args())
    def test_entry_successful(self, mock_input):
        with mock_aws():
            client = boto3.client("secretsmanager")
            with patch("sys.stdout", new=io.StringIO()) as fake_out:
                entry(client)
                result = fake_out.getvalue()
                assert "Secret saved." in result

    @patch("builtins.input", side_effect=input_args())
    def test_entry_fails(self, mock_input):
        with mock_aws():
            client = boto3.client("s3")
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
            client = boto3.client("secretsmanager")
            entry(client)
            response = client.list_secrets()
            assert len(response["SecretList"]) == 1

    @patch("builtins.input", side_effect=input_args())
    def test_secret_already_exists(self, mock_input):
        with mock_aws():
            client = boto3.client("secretsmanager")
            entry(client)
            with patch("sys.stdout", new=io.StringIO()) as fake_out:
                entry(client)
                result = fake_out.getvalue()
                assert "Secret already exists!" in result


class TestRetrieval:

    @patch("builtins.input", side_effect=input_args())
    def test_retrieval_successful_1_secret(self, mock_input):
        with mock_aws():
            client = boto3.client("secretsmanager")
            with patch("sys.stdout", new=io.StringIO()) as fake_out:
                entry(client)
                retrieval(client)
                mock_input.input_args = ["de_2024_12_02"]
                result = fake_out.getvalue()
                assert "Secrets returned as dictionary" in result

    @patch("builtins.input", side_effect=input_args())
    def test_retrieval_successful_return_dict(self, mock_input):
        with mock_aws():
            client = boto3.client("secretsmanager")
            with patch("sys.stdout", new=io.StringIO()) as fake_out:
                entry(client)
                res = retrieval(client)
                mock_input.input_args = ["de_2024_12_02"]
                assert res == {"username": 'bidenj',
                        "password": 'Pa55word',
                        "host": 'host',
                        "database": 'database',
                        "get_port": 'port'}


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
