import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

# st. set_page_config(layout="wide")
st.set_page_config(layout="centered")

data = pd.read_csv('BBT_Income.csv')
data['Date'] = pd.to_datetime(data['Date'], dayfirst=True)
data['Date'] = data['Date'].dt.date

st.title('Main Page')
# st.header('Income management')
'more info here'

'''
*todos*

-- income in Kenya shillings
-- exchange rate

a button to indicate if you want to edit the values

a button to submit

a button to add more content, and a form to fill to add

how to we handle data keys so that the user change change them

how can we handle deletes
'''

fig = px.bar(data, x='Asset', y='Income', color='Income_Type', barmode="group")

col1, col2 = st.columns(2)


# months={
#     1: 'January',
#     2: 'February',
#     3: 'March',
#     4: 'April',
#     5: 'May',
#     6: 'June',
#     7: 'July',
#     8: 'August',
#     9: 'September': 9,
#     10: 'October': 10,
#     11: 'November': 11,
#     12: 'December': 12
# }
def get_year_month_data(input_df):
    input_df['Date'] = pd.to_datetime(input_df['Date'])
    input_df['Year'] = input_df['Date'].dt.year
    input_df['Month'] = input_df['Date'].dt.month
    input_df['Month_Name'] = input_df['Date'].dt.month_name()
    input_df['Month_Name'] = input_df['Month_Name'].str[:3]
    input_df['Trip_Cycle'] = input_df['Trip_Cycle'].str[:3]
    input_df['Month-Year2'] = input_df['Month'].astype(str) + '-' + input_df['Year'].astype(str)
    input_df['Month-Year'] = input_df['Month_Name'].astype(str) + '-' + input_df['Year'].astype(str)
    input_df['Cycle'] = input_df['Trip_Cycle'].astype(str) + '-' + input_df['Year'].astype(str)
    # input_df['Cycle-Month-Year'] = input_df['Month'].astype(str) + '-' + input_df['Year'].astype(str)
    input_df = input_df.sort_values(by=['Date'])
    return input_df
    # year_month_data['Date'].dt.month

year_month_data = get_year_month_data(data)

fig2 = px.bar(year_month_data, x='Cycle', y='Income', color='Income_Type')


fig_pie_chart = px.pie(year_month_data, values='Income', names='Income_Type')
fig_pie_chart2 = px.pie(year_month_data, values='Income', names='Asset')

st.write(year_month_data)

col2.write(fig2)
col2.write(fig_pie_chart)
col1.write(fig)
col1.write(fig_pie_chart2)


