import streamlit as st

st. set_page_config(layout="wide")

# import uti

# from .. import

import utils.data_connection_utils as data_connect
# import ..utils.data_connection_utils as data_connect
from utils.state_management import set_state
import plotly.express as px
# import plotly.graph_objects as go



div1, div2 = st.columns([1, 4])

set_state('revenue_df', data_connect.get_revenue_data())
set_state('expense_df', data_connect.get_expense_data())
set_state('asset_df', data_connect.get_asset_data())
set_state('table_view', 'Revenue')


set_state('prepared_revenue_df', data_connect.get_year_month_data(st.session_state.revenue_df, 'Trip_Cycle'))
set_state('prepared_expense_df', data_connect.get_year_month_data(st.session_state.expense_df, 'Cycle'))


def handle_table_view_change():
    if st.session_state.table_view == "Revenue":
        st.session_state.table_view = "Expenses"
    else:
        st.session_state.table_view = "Revenue"


# metrics
total_revenue = st.session_state.prepared_revenue_df['Income'].sum()
total_expense = st.session_state.prepared_expense_df['Cost'].sum()
# st.write(total_revenue)

col1, col2, col3 = div2.columns(3)

col1.metric('Total Revenue', f'{total_revenue:,}')
col2.metric('Total Expense', f'{total_expense:,}')
col3.metric('Total Profit', f'{total_revenue - total_expense:,}')

# create visuals
fig_asset_revenue = px.bar(
    st.session_state.prepared_revenue_df,
    x='Asset',
    y='Income',
    color='Income_Type',
    # barmode="group"
)

fig_revenue = px.bar(
    st.session_state.prepared_revenue_df,
    x='Cycle_Month_Year',
    y='Income',
    color='Income_Type'
)

# st.dataframe(st.session_state.prepared_expense_df)

relevant_expense_data = st.session_state.prepared_expense_df.loc[st.session_state.prepared_expense_df['Billed_From_Revenue'] == 'Yes']
relevant_expense_data['Expense_Type'] = relevant_expense_data['Expense_Type'].fillna('N/A')

fig_asset_expense = px.bar(
    relevant_expense_data,
    x='Asset',
    y='Cost',
    color='Cost',
    # barmode="group"
)

fig_expenses = px.bar(
    relevant_expense_data.sort_values(by=['Date'], ascending=True),
    x='Cycle_Month_Year',
    y='Cost',
    color='Expense_Type',
    barmode='stack',
)

cumulative_revenue = st.session_state.prepared_revenue_df
group_df = cumulative_revenue.sort_values(by=['Date'], ascending=False)
group_df = group_df.groupby('Cycle_Month_Year').sum('Income').reset_index()


# st.dataframe(group_df)
# group_df = group_df.sort_values('Cycle_Month_Year')
group_df['Cumulative_Income'] = group_df['Income'].cumsum()
# st.dataframe(group_df)

data_used_here = st.session_state.prepared_revenue_df[['Date', 'Cycle_Month_Year', 'Income']]
# fig_revenue_cumulative2 = data_used_here.join(
#         # data_used_here[['Cycle_Month_Year', 'Income']].groupby("Cycle_Month_Year", as_index=False).cumsum(), rsuffix="_cumsum"
#         data_used_here['Income'].cumsum(), rsuffix="_cumsum"
#     )

fig_revenue_cumulative = px.line(
    st.session_state.prepared_revenue_df.join(
        st.session_state.prepared_revenue_df['Income'].cumsum(), rsuffix="_cumsum"
    ),
    y="Income_cumsum",
    x="Cycle_Month_Year",
    # color="Income_cumsum"
)









# graphs

col1, col2 = div2.columns(2)

col1.write(fig_revenue)
col1.write(fig_asset_revenue)
col2.write(fig_expenses)
col2.write(fig_asset_expense)
div2.write(fig_revenue_cumulative)


view_table = div2.radio(
    "## Select table to view",
    ["Revenue", "Expenses"],
    # captions = ["Data regarding income", "", "Never stop learning."]
    horizontal=True,
    on_change=handle_table_view_change()
    )

div2.write(st.session_state.table_view)

if view_table == "Revenue":
    div2.write('*Revenue Table*')
    div2.dataframe(
        st.session_state.prepared_revenue_df,
        selection_mode="multi-row"
    )
elif view_table == "Expenses":
    div2.write('*Expenses Table*')
    div2.dataframe(st.session_state.prepared_expense_df)


# div1
unique_assets = st.session_state.asset_df['Asset_ID'].unique().tolist()
div2.write(unique_assets)
options = div1.multiselect(
    "Select Assets",
    [*unique_assets])

# st.write(st.session_state)
