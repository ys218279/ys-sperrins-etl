from src.src_load.load_utils import pd_read_s3_parquet, get_insert_query

import boto3
import unittest
from unittest.mock import patch, Mock
from moto import mock_aws
import pytest
import pandas as pd
from io import BytesIO

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
        res = get_insert_query(table_name, column_names, on_conflict)
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
        res = get_insert_query(table_name, column_names, on_conflict)
        expected = (
            "INSERT INTO fact_sales (sales_record_id, sales_order_id, created_date, created_time, last_updated_date, last_updated_time, sales_staff_id, counterparty_id, units_sold, unit_price, currency_id, design_id, agreed_payment_date, agreed_delivery_date, agreed_delivery_location_id)\n"
            "    VALUES (:sales_record_id, :sales_order_id, :created_date, :created_time, :last_updated_date, :last_updated_time, :sales_staff_id, :counterparty_id, :units_sold, :unit_price, :currency_id, :design_id, :agreed_payment_date, :agreed_delivery_date, :agreed_delivery_location_id);"
        )
        assert res.strip() == expected.strip()



