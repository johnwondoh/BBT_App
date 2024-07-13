import streamlit as st
from datetime import datetime


def income_columns_configuration():
    column_configuration = {
        "is_widget": "Widget ?",
        "Date": st.column_config.DatetimeColumn(
            "Date",
            min_value=datetime(2023, 6, 1),
            max_value=datetime(2025, 1, 1),
            format="D MMM YYYY",
            # format="D MMM YYYY, h:mm a",
            step=60,
        ),
        "Asset": st.column_config.SelectboxColumn(
            "Asset",
            help="Our current assets",
            # width="medium",
            options=[
                "trk0001",
                "trk0002",
            ],
            required=True,
        ),
        "Trip Cycle": st.column_config.SelectboxColumn(
            "Trip Cycle",
            help="Our monthly trip cycle",
            # width="small",
            options=[
                'January',
                'February',
                'March',
                'April',
                'May',
                'June',
                'July',
                'August',
                'September',
                'October',
                'November',
                'December'
            ],
            required=True,
        ),
        "Income Type": st.column_config.SelectboxColumn(
            "Income Type",
            help="Income type",
            # width="medium",
            options=[
                "Adhoc",
                "Main",
            ],
            required=True,
        ),
        "Income": st.column_config.NumberColumn(
            "Income (in AUD)",
            help="The price of the product in AUD",
            min_value=0,
            # max_value=1000,
            step=1,
            format="$%d",
        ),
        "Reserved Amount": st.column_config.NumberColumn(
            "Reserved Amt (AUD)",
            help="The price of the product in AUD",
            min_value=0,
            # max_value=1000,
            step=1,
            format="$%d",
        )
    }
    return column_configuration
