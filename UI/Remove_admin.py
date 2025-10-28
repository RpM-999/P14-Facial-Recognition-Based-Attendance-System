import streamlit as st 
from FUNC.navigation import go_to

def remove_admin():
    st.info("This page will available soon")
    
    st.markdown("---")
    if st.button("⬅️ Back to Admin Menu", key="back_admin_btn"):
        go_to("Admin_option")
        st.rerun()