import streamlit as st
from UTILS.navigation import go_to

def show():
    st.title("🏫 Welcome to Attendance System")
    st.write("Please select an option:")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Admin Login"):
            go_to("Admin_login")
    with col2:
        if st.button("Give Attendance"):
            st.info("Attendance page coming soon")