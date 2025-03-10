from src.src_load.load_utils import pd_read_s3_parquet, get_insert_query, retrieval
import io
import boto3
import unittest
from unittest.mock import patch, Mock
from moto import mock_aws
import pytest
import pandas as pd
from io import BytesIO
import json

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

def entry(client,secret_identifier = "de_2024_12_02"):
    """Use to create the initial TEST secret"""
    if "SecretsManager" in str(type(client)):
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
    def test_retrieval_successfully_gets_a_secret(self, mock_input):
        mock_input.input_args = ["fake_db"]
        with mock_aws():
            client = boto3.client("secretsmanager", region_name="eu-west-2")
            entry(client,secret_identifier="totesys_data_warehouse_olap")
            res = retrieval(client)
            assert res is not None

    @patch("builtins.input")
    def test_retrieval_successful_return_dict(self,mock_input):
        with mock_aws():
            client = boto3.client("secretsmanager", region_name="eu-west-2")
            with patch("sys.stdout", new=io.StringIO()):
                entry(client,secret_identifier="totesys_data_warehouse_olap")
                res = retrieval(client)
                mock_input.input_args = ["fake_tote_dw"]
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
                
    
class TestPdReadParquett:
    def test_pd_read_s3_parquet(self):
        with mock_aws():
            s3_client = boto3.client('s3', region_name='eu-west-2')
            s3_client.create_bucket(
                    Bucket="test-bucket",
                    CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
                )
            bucket_name = "test-bucket"
            test_data = {
                    "calories": [420, 380, 390],
                    "duration": [50, 40, 45]
                    }
            df = pd.DataFrame(test_data)
            output_buffer = BytesIO()
            df.to_parquet(output_buffer)
            body = output_buffer.getvalue()
            s3_client.put_object(Bucket=bucket_name, Key='test_data_parquet', Body=body)
            res_df = pd_read_s3_parquet('test_data_parquet', bucket_name, s3_client)
            pd.testing.assert_frame_equal(res_df, df)

class TestGetInsertQuery:
    def test_get_insert_query_not_on_conflict(self):
        table_name = "dim_currency"
        column_names = ["currency_id", "currency_code", "currency_name"]
        on_conflict = True
        res = get_insert_query(table_name, column_names, "currency_id", on_conflict)
        print(res)
        expected = """INSERT INTO dim_currency (currency_id, currency_code, currency_name)
    VALUES (:currency_id, :currency_code, :currency_name)
    ON CONFLICT (currency_id)
    DO UPDATE SET currency_code = EXCLUDED.currency_code, currency_name = EXCLUDED.currency_name;
    """
        assert res == expected

    def test_get_insert_query_not_on_conflict(self):
        table_name = "fact_sales"
        column_names = [
            "sales_record_id", "sales_order_id", "created_date", "created_time",
            "last_updated_date", "last_updated_time", "sales_staff_id", "counterparty_id",
            "units_sold", "unit_price", "currency_id", "design_id",
            "agreed_payment_date", "agreed_delivery_date", "agreed_delivery_location_id"
        ]
        on_conflict = False
        res = get_insert_query(table_name, column_names, "sales_record_id", on_conflict)
        expected = (
            "INSERT INTO fact_sales (sales_order_id, created_date, created_time, last_updated_date, last_updated_time, sales_staff_id, counterparty_id, units_sold, unit_price, currency_id, design_id, agreed_payment_date, agreed_delivery_date, agreed_delivery_location_id)\n"
            "    VALUES (:sales_order_id, :created_date, :created_time, :last_updated_date, :last_updated_time, :sales_staff_id, :counterparty_id, :units_sold, :unit_price, :currency_id, :design_id, :agreed_payment_date, :agreed_delivery_date, :agreed_delivery_location_id);"
        )
        assert res.strip() == expected.strip()



