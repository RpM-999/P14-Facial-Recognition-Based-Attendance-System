import streamlit as st

def go_to(page_name: str):
   
    st.session_state.current_page = page_name
    st.rerun()