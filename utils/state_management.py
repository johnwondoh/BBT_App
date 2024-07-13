import streamlit as st


def set_state(state_name, state_value):
    if state_name not in st.session_state:
        # st.session_state[state_name] = state_value
        st.session_state[state_name] = state_value




