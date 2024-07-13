import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
# from pydantic import BaseModel
# from pydantic_settings import BaseModel # NEW
# import streamlit_pydantic as sp

import utils.configurations as configs
from utils.state_management import set_state

st. set_page_config(layout="wide")


def handle_delete_selected_income_data():
    st.session_state['delete_selected_income_data'] = True


def confirm_delete_selected_income_data(new_data):
    st.session_state.data = new_data
    st.session_state['delete_selected_income_data'] = False


def revert_delete_selected_income_data():
    st.session_state['delete_selected_income_data'] = False


def handle_open_income_entry():
    st.session_state.open_income_entry = True


def handle_add_income_entry():
    st.session_state.create_income_entry = True


div1, div2 = st.columns([1, 3])

options = div1.multiselect(
    "What are your favorite colors",
    ["Green", "Yellow", "Red", "Blue"],
    ["Yellow", "Red"])

data = pd.read_csv('BBT_Income.csv')
data['Date'] = pd.to_datetime(data['Date'], dayfirst=True)
data['Date'] = data['Date'].dt.date
data['Select'] = False

set_state('data', data)
set_state('delete_selected_income_data', False)
set_state('open_income_entry', False)
set_state('create_income_entry', False)
# set_state('confirm_del_for_select_income_data', False)





div2.title('Income management')
# st.header('Income management')
div2.write('more info here')

div2.write('''
*todos*

a button to indicate if you want to edit the values

a button to submit

a button to add more content, and a form to fill to add

how to we handle data keys so that the user change change them

how can we handle deletes
'''
)

# -------------------------------------------

# -------------------------------------------

# col1, col2 = div2.columns(2)


d = div2.data_editor(
    # div2.session_state.data,
    st.session_state.data,
    column_config=configs.income_columns_configuration(),
)


create = div2.button('Add new income item', type="secondary", on_click=handle_open_income_entry)
delete = div2.button('Deleted Selected Item', type="primary", on_click=handle_delete_selected_income_data)

if st.session_state.delete_selected_income_data:
    selected_items = d.loc[d['Select']]
    unselected_items = d.loc[~d['Select']]
    # unselected_income_items = d.loc[d['Select'] == False]
    if not selected_items.empty:
        div2.write('_Are you sure you want to delete the following rows?_')
        div2.dataframe(selected_items)
        button_pos1, button_pos2 = div2.columns(2)
        button_pos1.button(
            'No',
            use_container_width=True,
            on_click=revert_delete_selected_income_data
        )
        button_pos2.button(
            'Yes',
            use_container_width=True,
            on_click=confirm_delete_selected_income_data(unselected_items)
        )
    else:
        div2.write('Please select rows to delete first')
        st.session_state.delete_selected_income_data = False





# st_btn_group(
#     buttons=[{"label": "Button 1", "value": "1"}, {"label": "Button 2", "value": "2"}],
# )


# selected_income_items = d

# div2.dataframe(selected_income_items)
st.write(delete)
# div2.write(create)

# show_form = False
#
# if create:
#     show_form = create
# add_new_row = False
if st.session_state.open_income_entry:
    with div2.container(border=True):
        form_col1, form_col2 = div2.columns(2)

        div2.write("Inside the form")
        date_recorded = form_col1.date_input("Date received", value=None)
        asset = form_col2.selectbox(
            'Select appropriate asset',
            ('trk0001', 'trk0002'),
            index=None,
            placeholder='select asset'
        )
        trip_cycle = form_col1.selectbox(
            'Select trip cycle',
            (
                'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
                'September', 'October', 'November', 'December'
             ),
            index=None,
            placeholder='select trip cycle'
        )
        income_type = form_col2.selectbox(
            'Select income type',
            ('Adhoc', 'Main'),
            index=None,
            placeholder='select trip cycle'
        )
        income = form_col1.number_input("Amount", value=None, placeholder="amount (AUD")
        reserved = form_col2.number_input("Reserved", value=None, placeholder="amount (AUD")

        txt = div2.text_area(
            "Comments", "",)
        add_new_row = div2.button('Create Entry')


# if add_new_row:
#     st.write(date_recorded)

with st.sidebar:
    with st.echo():
        st.write("This code will be printed to the sidebar.")

    with st.spinner("Loading..."):
        # time.sleep(5)
        st.success("Done!")

div2.dataframe(d)

st.session_state




