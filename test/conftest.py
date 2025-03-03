import pytest
import pandas as pd


@pytest.fixture(scope="module")
def input_data_design():
    data = {
        "design_id": [1, 2, 3],
        "created_at": [
            "2022-11-03 14:20:49.962000",
            "2022-11-03 14:20:49.962000",
            "2022-11-03 14:20:49.962000",
        ],
        "last_updated": [
            "2022-11-03 14:20:49.962000",
            "2022-11-03 14:20:49.962000",
            "2022-11-03 14:20:49.962000",
        ],
        "design_name": ["design1", "design2", "design3"],
        "file_location": ["folder/next", "folder2/next2", "folder3/next3"],
        "file_name": ["image.png", "image2.png", "image2.png"],
    }
    return pd.DataFrame(data=data)


@pytest.fixture(scope="module")
def output_data_design():
    data = {
        "design_id": [1, 2, 3],
        "design_name": ["design1", "design2", "design3"],
        "file_location": ["folder/next", "folder2/next2", "folder3/next3"],
        "file_name": ["image.png", "image2.png", "image2.png"],
    }
    return pd.DataFrame(data=data)


@pytest.fixture(scope="module")
def input_data_currency():
    data = {
        "currency_id": [1, 2, 3],
        "created_at": [
            "2022-11-03 14:20:49.962000",
            "2022-11-03 14:20:49.962000",
            "2022-11-03 14:20:49.962000",
        ],
        "last_updated": [
            "2022-11-03 14:20:49.962000",
            "2022-11-03 14:20:49.962000",
            "2022-11-03 14:20:49.962000",
        ],
        "currency_code": ["GBP", "EUR", "USD"],
    }
    return pd.DataFrame(data=data)


@pytest.fixture(scope="module")
def output_data_currency():
    data = {
        "currency_id": [1, 2, 3],
        "currency_code": ["GBP", "EUR", "USD"],
        "currency_name": ["Pound sterling", "Euro", "United States dollar"],
    }
    return pd.DataFrame(data=data)


@pytest.fixture(scope="module")
def input_data_staff():
    data = {
        "staff_id": [1, 2, 3],
        "created_at": [
            "2022-11-03 14:20:49.962000",
            "2022-11-03 14:20:49.962000",
            "2022-11-03 14:20:49.962000",
        ],
        "last_updated": [
            "2022-11-03 14:20:49.962000",
            "2022-11-03 14:20:49.962000",
            "2022-11-03 14:20:49.962000",
        ],
        "first_name": ["Tom", "Sam", "John"],
        "last_name": ["Jones", "Wilde", "Smith"],
        "department_id": [1, 2, 3],
        "email_address": ["tom@totebags.com", "sam@totebags.com", "john@totebags.com"],
    }
    return pd.DataFrame(data=data)


@pytest.fixture(scope="module")
def input_data_department():
    data = {
        "department_id": [1, 2, 3],
        "created_at": [
            "2022-11-03 14:20:49.962000",
            "2022-11-03 14:20:49.962000",
            "2022-11-03 14:20:49.962000",
        ],
        "last_updated": [
            "2022-11-03 14:20:49.962000",
            "2022-11-03 14:20:49.962000",
            "2022-11-03 14:20:49.962000",
        ],
        "department_name": ["Sales", "Tech", "Marketing"],
        "location": ["Manchester", "London", "Leeds"],
        "manager": ["Paul C.", "Eli S.", "Danika R."],
    }
    return pd.DataFrame(data=data)


@pytest.fixture(scope="module")
def output_data_staff():
    data = {
        "staff_id": [1, 2, 3],
        "first_name": ["Tom", "Sam", "John"],
        "last_name": ["Jones", "Wilde", "Smith"],
        "email_address": ["tom@totebags.com", "sam@totebags.com", "john@totebags.com"],
        "department_name": ["Sales", "Tech", "Marketing"],
        "location": ["Manchester", "London", "Leeds"],
    }
    return pd.DataFrame(data=data)


@pytest.fixture(scope="module")
def input_data_address():
    data = {
        "address_id": [1, 2, 3],
        "created_at": [
            "2022-11-03 14:20:49.962000",
            "2022-11-03 14:20:49.962000",
            "2022-11-03 14:20:49.962000",
        ],
        "last_updated": [
            "2022-11-03 14:20:49.962000",
            "2022-11-03 14:20:49.962000",
            "2022-11-03 14:20:49.962000",
        ],
        "address_line_1": ["3 Church Lane", "10 Nelson Road", "4 Wilton Avenue"],
        "address_line_2": ["Putney", "Camden", "Kew"],
        "district": ["Lambeth", "Merton", "Richmond"],
        "city": ["Manchester", "London", "Leeds"],
        "postal_code": ["GU1 342", "TW3 827", "YE4 978"],
        "phone": ["078853686554", "07576455456", "07846556544"],
    }
    return pd.DataFrame(data=data)


@pytest.fixture(scope="module")
def output_data_location():
    data = {
        "address_id": [1, 2, 3],
        "address_line_1": ["3 Church Lane", "10 Nelson Road", "4 Wilton Avenue"],
        "address_line_2": ["Putney", "Camden", "Kew"],
        "district": ["Lambeth", "Merton", "Richmond"],
        "city": ["Manchester", "London", "Leeds"],
        "postal_code": ["GU1 342", "TW3 827", "YE4 978"],
        "phone": ["078853686554", "07576455456", "07846556544"],
    }
    return pd.DataFrame(data=data)


@pytest.fixture(scope="module")
def input_data_counterparty():
    data = {
        "counterparty_id": [1, 2, 3],
        "created_at": [
            "2022-11-03 14:20:49.962000",
            "2022-11-03 14:20:49.962000",
            "2022-11-03 14:20:49.962000",
        ],
        "last_updated": [
            "2022-11-03 14:20:49.962000",
            "2022-11-03 14:20:49.962000",
            "2022-11-03 14:20:49.962000",
        ],
        "counterparty_legal_name": ["Paul C.", "Eli S.", "Danika R."],
        "legal_address_id": [1, 2, 3],
        "commercial_contact": ["Argos", "WH Smiths", "Homebase"],
        "delivery_contact": ["Warehouse", "Logistics", "Supply Chains"],
    }
    return pd.DataFrame(data=data)


@pytest.fixture(scope="module")
def output_data_counterparty():
    data = {
        "counterparty_id": [1, 2, 3],
        "counterparty_legal_name": ["Paul C.", "Eli S.", "Danika R."],
        "counterparty_address_line_1": [
            "3 Church Lane",
            "10 Nelson Road",
            "4 Wilton Avenue",
        ],
        "counterparty_address_line_2": ["Putney", "Camden", "Kew"],
        "counterparty_district": ["Lambeth", "Merton", "Richmond"],
        "counterparty_city": ["Manchester", "London", "Leeds"],
        "counterparty_postal_code": ["GU1 342", "TW3 827", "YE4 978"],
        "counterparty_phone": ["078853686554", "07576455456", "07846556544"],
    }
    return pd.DataFrame(data=data)


@pytest.fixture(scope="module")
def output_data_date():
    data = {
        "year": [2025, 2025, 2025],
        "month": [3, 3, 3],
        "day": [3, 4, 5],
        "day_of_week": [0, 1, 2],
        "day_name": ["Monday", "Tuesday", "Wednesday"],
        "month_name": ["March", "March", "March"],
        "quarter": [1, 1, 1],
    }
    df_date = pd.DataFrame(data=data)
    df_date.index.name = "date_id"
    return df_date


# sales_order_id last updated date and time


@pytest.fixture(scope="module")
def input_data_sales_order():
    data = {
        "sales_order_id": [1, 2, 3],
        "created_at": [
            "2022-11-03 14:20:49.962000",
            "2022-11-03 14:20:49.962000",
            "2022-11-03 14:20:49.962000",
        ],
        "last_updated": [
            "2022-11-03 14:20:49.962000",
            "2022-11-03 14:20:49.962000",
            "2022-11-03 14:20:49.962000",
        ],
        "design_id": [1, 2, 3],
        "sales_staff_id": [1, 2, 3],
        "counterparty_id": [1, 2, 3],
        "units_sold": [12345,53422134, 9873234567],
        "unit_price": [12.34, 5.32, 9.99],
        "currency_id": [1, 2, 3],
        "agreed_delivery_date": ["2025-01-18", "4032-01-08", "2024-12-22"],
        "agreed_payment_date": ["2025-01-18", "4032-01-08", "2024-12-22"],
        "agreed_delivery_location_id": [2345, 2, 5],
    }
    df_sales_order = pd.DataFrame(data=data)
    return df_sales_order


@pytest.fixture(scope="module")
def output_data_sales_order():
    data = {
        "sales_order_id": [1, 2, 3],
        "design_id": [1, 2, 3],
        "sales_staff_id": [1, 2, 3],
        "counterparty_id": [1, 2, 3],
        "units_sold": [12345,53422134, 9873234567],
        "unit_price": [12.34, 5.32, 9.99],
        "currency_id": [1, 2, 3],
        "agreed_delivery_date": ["2025-01-18", "4032-01-08", "2024-12-22"],
        "agreed_payment_date": ["2025-01-18", "4032-01-08", "2024-12-22"],
        "agreed_delivery_location_id": [2345, 2, 5],
        "created_date": ['2022-11-03', "2022-11-03", "2022-11-03"],
        "created_time": ["14:20:49.962000", "14:20:49.962000", "14:20:49.962000"],
        "last_updated_date": ["2022-11-03", "2022-11-03", "2022-11-03"],
        "last_updated_time": ["14:20:49.962000", "14:20:49.962000", "14:20:49.962000"],
    }
    output_df_sales_order = pd.DataFrame(data=data)
    output_df_sales_order["created_date"] = pd.to_datetime(output_df_sales_order['created_date']).dt.date
    output_df_sales_order["created_time"] = pd.to_datetime(output_df_sales_order['created_time']).dt.time
    output_df_sales_order["last_updated_date"] = pd.to_datetime(output_df_sales_order['last_updated_date']).dt.date
    output_df_sales_order["last_updated_time"] = pd.to_datetime(output_df_sales_order['last_updated_time']).dt.time
    return output_df_sales_order
