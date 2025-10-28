import streamlit as st
from FUNC.navigation import go_to

from BACKEND.department_OP import add_department

def Add_new_department_page():


    if not st.session_state.get("logged_in"):
        st.warning("You must be logged in to view this page.")
        if st.button("Go to Login"):
            go_to("Admin_login")
        return

    st.title("Add a New Department")

    with st.form("add_department_form", clear_on_submit=True):
        st.subheader("Department Details")
        
        d_id = st.text_input("Department ID", placeholder="e.g. cse-101")

        d_name = st.text_input("Department Name", placeholder="e.g., Computer Science")

        d_hod_name = st.text_input("Head of Department (HOD) Name", placeholder="Enter the HOD's full name")

        d_hod_email = st.text_input("HOD's Email Address", placeholder="hod.email@example.com")
       
        submitted = st.form_submit_button("Add Department")


        if submitted:
            # --- Validation ---
            if not all([d_id, d_name, d_hod_name, d_hod_email]):
                st.warning("Please fill out all fields.")
            else:
                try:
                    
                    add_department( dep_id=d_id ,dep_name=d_name,dep_hod=d_hod_name,dep_hod_mail=d_hod_email)
                    st.success(f"✅ Successfully added department: {d_name}")
                    
                except Exception as e:
                    # This will catch potential errors like a duplicate department ID
                    st.error(f"An error occurred: {e}")


    if st.button("⬅️ Back to Admin Menu"):
        go_to("Admin_option")
