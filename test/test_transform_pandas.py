import pytest
import pandas as pd
from src.src_transform.transform_pandas import create_dim_design_table, create_dim_currency_table, create_dim_staff_table, create_dim_location_table, create_dim_counterparty_table, create_dim_date_table


def test_create_dim_design_creates_correct_schema(input_data_design, output_data_design):
    dim_design_data = create_dim_design_table(input_data_design)
    pd.testing.assert_frame_equal(dim_design_data, output_data_design)
    
def test_create_dim_currency_creates_correct_schema(input_data_currency, output_data_currency):
    dim_currency_data = create_dim_currency_table(input_data_currency)
    pd.testing.assert_frame_equal(dim_currency_data, output_data_currency)

def test_create_dim_staff_creates_correct_schema(input_data_staff, input_data_department, output_data_staff):
    dim_staff_data = create_dim_staff_table(input_data_staff, input_data_department)
    pd.testing.assert_frame_equal(dim_staff_data, output_data_staff)

def test_create_dim_location_creates_correct_schema(input_data_address, output_data_location):
    dim_location_data = create_dim_location_table(input_data_address)
    pd.testing.assert_frame_equal(dim_location_data, output_data_location)

def test_create_dim_counterparty_creates_correct_schema(input_data_address, input_data_counterparty, output_data_counterparty):
    dim_counterparty_data = create_dim_counterparty_table(input_data_address, input_data_counterparty)
    pd.testing.assert_frame_equal(dim_counterparty_data, output_data_counterparty)

def test_create_dim_date_creates_correct_schema(output_data_date):
    dim_date_data = create_dim_date_table(start='2025/03/03', end='2025/03/05')
    pd.testing.assert_frame_equal(dim_date_data, output_data_date, check_dtype=False)