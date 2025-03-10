from moto import mock_aws
from unittest.mock import patch
import logging, pytest, os

class DummyContext:
    pass

with patch.dict(os.environ, {"S3_BUCKET_NAME_PROCESSED": "test_bucket_processed"}):
    from src.src_load.load_lambda import lambda_handler


@pytest.fixture(scope="function")
def lambda_event():
    return {"dim_design": "dim_design/2025-03-06/224349.parquet",
            "dim_currency": False,
            "dim_staff": "dim_staff/2025-03-06/224349.parquet",
            "dim_location": "dim_location/2025-03-06/224349.parquet",
            "dim_counterparty": "dim_counterparty/2025-03-06/224349.parquet",
            "dim_date": "dim_date/2025-03-06/224349.parquet",
            "fact_sales_order": "fact_sales_order/2025-03-06/224349.parquet"
        }

@patch('src.src_load.load_lambda.get_s3_client')
def test_logging_for_lambda_handler(s3_client,lambda_event, create_bucket_processed, bucket_name_processed, caplog):
    with mock_aws():
        s3_client.return_value=0
        context = DummyContext()
        with caplog.at_level(logging.INFO):
            lambda_handler(lambda_event,context, BUCKET_NAME=bucket_name_processed)
            assert "Unexpected Exception" in caplog.text
