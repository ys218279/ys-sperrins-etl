from utilities.test_secrets_manager import entry, password_retrieval
import pytest
import boto3

def input_args():
    yield "Missile_Launch_Codes"
    yield "bidenj"
    yield "Pa55word"
    yield "Missile_Launch_Codes"
    yield "bidenj"
    yield "Pa55word"
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








def test_password_retrieval_retrieves_id_and_save_credentials_to_file():
    client = boto3.client('secretsmanager')
    result = password_retrieval(client)
    file_name = 'secrets.txt'
    assert result == f'secrets stored in {file_name}' 

def test_password_retrieval_shows_error_message_if_id_not_exist():
    client = boto3.client('secretsmanager')
    result = password_retrieval(client)
    
    assert result == 'Secret not found' 