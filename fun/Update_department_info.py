import streamlit as st
from utils.navigation import go_to


def update_department():


    if not st.session_state.get("logged_in"):
        st.warning("You must be logged in to view this page.")
        if st.button("Go to Login"):
            go_to("Admin_login")
        return
    
    st.title("Update Department Info")

    with st.form("update_department_form",clear_on_submit=True)
    
