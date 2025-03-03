import pandas as pd
import boto3
import json


def create_dim_design_table(df_design):
    df_dim_design = df_design.drop(columns=['created_at','last_updated'])
    return df_dim_design

def create_dim_currency_table(df_currency):
    df_dim_currency = df_currency.drop(columns=['created_at','last_updated'])
    currency_dictionary = {'GBP': 'Pound sterling', 'EUR': 'Euro', 'USD': 'United States dollar'}
    df_dim_currency['currency_name'] = df_dim_currency['currency_code'].map(currency_dictionary)
    return df_dim_currency

def create_dim_staff_table(df_staff, df_department):
    df_staff_mod = df_staff.drop(columns=['created_at','last_updated'])
    df_department_mod = df_department.drop(columns=['created_at','last_updated', 'manager'])
    df_dim_staff = pd.merge(df_staff_mod, df_department_mod, left_on='department_id', right_on='department_id', how='left').drop(columns=['department_id'])
    return df_dim_staff

def create_dim_location_table(df_address):
    df_dim_location = df_address.drop(columns=['created_at','last_updated'])
    return df_dim_location

def create_dim_counterparty_table(df_address, df_counterparty):
    df_address_mod = df_address.drop(columns=['created_at','last_updated'])
    df_counterparty_mod = df_counterparty.drop(columns=['created_at','last_updated', 'commercial_contact', 'delivery_contact'])
    df_dim_counterparty = pd.merge(df_counterparty_mod, df_address_mod, left_on='legal_address_id', right_on='address_id', how='left').drop(columns=['address_id', 'legal_address_id'])
    df_dim_counterparty_mod = df_dim_counterparty.rename(columns={'address_line_1': 'counterparty_address_line_1', 
                                                      'address_line_2': 'counterparty_address_line_2',
                                                      'district': 'counterparty_district',
                                                      'city': 'counterparty_city',
                                                      'postal_code': 'counterparty_postal_code',
                                                      'phone': 'counterparty_phone'})
    return df_dim_counterparty_mod

def create_dim_date_table(start='2000/01/01', end='2050/12/31'):
    '''
    Create Dimension Date in Pandas
    
    :return df_date : DataFrame
    '''
    # Construct DIM Date Dataframe
    df_date = pd.DataFrame({"Date": pd.date_range(start=f'{start}', end=f'{end}', freq='D')})
    df_date.index.name = 'date_id'
    df_date["year"] = df_date.Date.dt.year
    df_date["month"] = df_date.Date.dt.month
    df_date["day"] = df_date.Date.dt.day
    df_date["day_of_week"] = df_date.Date.dt.dayofweek 
    df_date["day_name"] = df_date.Date.dt.day_name()
    df_date["month_name"] = df_date.Date.dt.month_name()
    df_date["quarter"] = df_date.Date.dt.quarter
    df_date_mod = df_date.drop(columns=['Date'])
    return df_date_mod

def create_fact_sales_table():
    pass