import requests
import pandas as pd
import streamlit as st


def get_data(api):
    response = requests.get(api)
    data = response.json()
    reff = pd.json_normalize(data['data'])
    df = pd.DataFrame(data=reff)
    return df


@st.cache_data
def get_revenue_data():
    revenue_api = "https://n39ah9it60.execute-api.us-east-1.amazonaws.com/prd/revenue"
    data = get_data(revenue_api)
    return data


@st.cache_data
def get_asset_data():
    assets_api = "https://n39ah9it60.execute-api.us-east-1.amazonaws.com/prd/assets"
    data = get_data(assets_api)
    return data


@st.cache_data
def get_expense_data():
    expenses_api = "https://n39ah9it60.execute-api.us-east-1.amazonaws.com/prd/expenses"
    data = get_data(expenses_api)
    # print(data.dtypes)
    return data


def get_year_month_data(input_df, cycle_name):
    input_df['Date'] = pd.to_datetime(input_df['Date'])
    input_df['Year'] = input_df['Date'].dt.year
    input_df['Month'] = input_df['Date'].dt.month
    input_df['Month_Name'] = input_df['Date'].dt.month_name()
    input_df['Month_Name'] = input_df['Month_Name'].str[:3]
    input_df[cycle_name] = input_df[cycle_name].str[:3]
    # input_df['Month-Year2'] = input_df['Month'].astype(str) + '-' + input_df['Year'].astype(str)
    input_df['Month-Year'] = input_df['Month_Name'].astype(str) + '-' + input_df['Year'].astype(str)
    input_df['Cycle_Month_Year'] = input_df[cycle_name].astype(str) + '-' + input_df['Year'].astype(str)
    # input_df['Cycle-Month-Year'] = input_df['Month'].astype(str) + '-' + input_df['Year'].astype(str)
    input_df = input_df.sort_values(by=['Date'])
    return input_df


# get_expense_data()
x = get_year_month_data(get_expense_data(), 'Cycle')
print(x)
# df = get_data(get_all_revenue_api, 'revenue')
# print(res.json())

