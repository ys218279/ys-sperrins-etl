import pandas as pd
import boto3
import json


def create_dim_design_table(df_des):
    """Converts source df table to target df table schema
    
    Keyword arguments:
    - df_des (panda df obj): The table in dataframe format - source
    
    Returns:
    - df_dim_design (panda df obj): The table in dataframe format - target
    """
    df_design = df_des.copy().set_index('design_id')
    df_dim_design = df_design.drop(columns=['created_at','last_updated'])
    return df_dim_design

def create_dim_currency_table(df_cur):
    """Converts source df table to target df table schema
    
    Keyword arguments:
    - df_cur (panda df obj): The table in dataframe format - source
    
    Returns:
    - df_dim_currency (panda df obj): The table in dataframe format - target
    """
    df_currency = df_cur.copy().set_index('currency_id')
    df_dim_currency = df_currency.drop(columns=['created_at','last_updated'])
    currency_dictionary = {'GBP': 'Pound sterling', 'EUR': 'Euro', 'USD': 'United States dollar'}
    df_dim_currency['currency_name'] = df_dim_currency['currency_code'].map(currency_dictionary)
    return df_dim_currency

def create_dim_staff_table(df_sta, df_dep):
    """Converts two source df table to one target df table schema
    
    Keyword arguments:
    - df_sta (panda df obj): The table in dataframe format - source
    - df_dep (panda df obj): The table in dataframe format - source
    
    Returns:
    - df_dim_staff (panda df obj): The table in dataframe format - target
    """
    df_staff = df_sta.copy()
    df_department = df_dep.copy()
    df_staff_mod = df_staff.drop(columns=['created_at','last_updated'])
    df_department_mod = df_department.drop(columns=['created_at','last_updated', 'manager'])
    df_dim_staff = pd.merge(df_staff_mod, df_department_mod, left_on='department_id', right_on='department_id', how='left').drop(columns=['department_id'])
    df_dim_staff = df_dim_staff.set_index('staff_id')
    return df_dim_staff

def create_dim_location_table(df_addr):
    """Converts source df table to target df table schema
    
    Keyword arguments:
    - df_addr (panda df obj): The table in dataframe format - source
    
    Returns:
    - df_dim_location_mod_2 (panda df obj): The table in dataframe format - target
    """
    df_address = df_addr.copy()
    df_dim_location = df_address.drop(columns=['created_at','last_updated'])
    df_dim_location_mod = df_dim_location.rename(columns={'address_id':'location_id'})
    df_dim_location_mod_2 = df_dim_location_mod.set_index('location_id')
    return df_dim_location_mod_2

def create_dim_counterparty_table(df_addr, df_cp):
    """Converts two source df table to one target df table schema
    
    Keyword arguments:
    - df_addr (panda df obj): The table in dataframe format - source
    - df_cp (panda df obj): The table in dataframe format - source
    
    Returns:
    - df_dim_counterparty_mod_2 (panda df obj): The table in dataframe format - target
    """
    df_address = df_addr.copy()
    df_counterparty = df_cp.copy()
    df_address_mod = df_address.drop(columns=['created_at','last_updated'])
    df_counterparty_mod = df_counterparty.drop(columns=['created_at','last_updated', 'commercial_contact', 'delivery_contact'])
    df_dim_counterparty = pd.merge(df_counterparty_mod, df_address_mod, left_on='legal_address_id', right_on='address_id', how='left').drop(columns=['address_id', 'legal_address_id'])
    df_dim_counterparty_mod = df_dim_counterparty.rename(columns={'address_line_1': 'counterparty_address_line_1', 
                                                      'address_line_2': 'counterparty_address_line_2',
                                                      'district': 'counterparty_district',
                                                      'city': 'counterparty_city',
                                                      'postal_code': 'counterparty_postal_code',
                                                      'country' : 'counterparty_country',
                                                      'phone': 'counterparty_phone'})
    df_dim_counterparty_mod_2 = df_dim_counterparty_mod.set_index('counterparty_id')
    return df_dim_counterparty_mod_2

def create_dim_date_table(start='2019/01/01', end='2030/12/31'):
    '''
    Creates Dimension Date in Pandas

    Keyword arguments:
    - start (str): The start date in string format
    - end (str): The end date in string format
    
    Returns:
    - df_date_mod_2 (panda df obj): The table in dataframe format - target
    '''
    # Construct DIM Date Dataframe
    df_date = pd.DataFrame({"Date": pd.date_range(start=f'{start}', end=f'{end}')})
    df_date["year"] = df_date.Date.dt.year
    df_date["month"] = df_date.Date.dt.month
    df_date["day"] = df_date.Date.dt.day
    df_date["day_of_week"] = df_date.Date.dt.dayofweek 
    df_date["day_name"] = df_date.Date.dt.day_name()
    df_date["month_name"] = df_date.Date.dt.month_name()
    df_date["quarter"] = df_date.Date.dt.quarter
    df_date_mod = df_date.rename(columns={'Date':'date_id'})
    df_date_mod["date_id"] = pd.to_datetime(df_date_mod["date_id"]).dt.strftime('%Y-%m-%d')
    df_date_mod_2 = df_date_mod.set_index('date_id')
    return df_date_mod_2

def create_fact_sales_order_table(df_sales):
    """Converts source df table to target df table schema
    
    Keyword arguments:
    - df_sales (panda df obj): The table in dataframe format - source
    
    Returns:
    - df_fact_sales_order (panda df obj): The table in dataframe format - target
    """
    df_sales_order = df_sales.copy()
    df_sales_order["created_date"] = pd.to_datetime(df_sales_order["created_at"], format='ISO8601').dt.strftime('%Y-%m-%d')
    df_sales_order["created_time"] = pd.to_datetime(df_sales_order["created_at"], format='ISO8601').dt.strftime('%H:%M:%S.%f')
    df_sales_order["last_updated_date"] = pd.to_datetime(df_sales_order["last_updated"], format='ISO8601').dt.strftime('%Y-%m-%d')
    df_sales_order["last_updated_time"] = pd.to_datetime(df_sales_order["last_updated"], format='ISO8601').dt.strftime('%H:%M:%S.%f')
    df_fact_sales_order = df_sales_order.drop(columns=['created_at','last_updated']).set_index('sales_order_id')
    return df_fact_sales_order


