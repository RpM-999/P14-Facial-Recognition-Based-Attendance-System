

import streamlit as st
from UTILS.navigation import go_to
from BACKEND.department_OP import get_all_departments, update_department

def update_department_info_page():

    if not st.session_state.get("logged_in"):
        st.warning("You must be logged in to view this page.")
        if st.button("Go to Login"):
            go_to("Admin_login")
            st.rerun()
        return

    st.title("Update Department Information")

    departments_list = get_all_departments()

    if not departments_list:
        st.warning("No departments found. Please add a department first.")
        if st.button("⬅️ Back to Admin Menu"):
            go_to("Admin_option")
            st.rerun()
        return

    # --- 3. Create Selectbox to choose department ---
    # The 'format_func' shows the pretty name in the box,
    # but 'selected_dept' will contain the *entire dictionary* for that department.
    selected_dept = st.selectbox(
        "Select Department to Update",
        options=departments_list,
        format_func=lambda dept: f"{dept['dep_id']} - {dept['dep_name']}"
    )

    if not selected_dept:
        st.stop()

    st.markdown("---")
    st.subheader(f"Updating: {selected_dept['dep_name']}")

    # --- 4. Create the Edit Form ---
    with st.form("update_department_form"):

        st.text_input("Department ID (dep_id)", value=selected_dept['dep_id'], disabled=True)
        
        # These fields can be edited
        new_dep_name = st.text_input("Department Name", value=selected_dept['dep_name'])
        new_dep_hod = st.text_input("Head of Department (HOD)", value=selected_dept['dep_hod'])
        new_dep_hod_mail = st.text_input("HOD's Email", value=selected_dept['dep_hod_mail'])

        submitted = st.form_submit_button("Save Changes")

        if submitted:
            # --- 5. Save Changes ---
            if not all([new_dep_name, new_dep_hod, new_dep_hod_mail]):
                st.warning("Please fill out all fields.")
            else:
                try:

                    update_department(dep_id=selected_dept['dep_id'], dep_name=new_dep_name,dep_hod=new_dep_hod,dep_hod_mail=new_dep_hod_mail)
                    
                    st.success("✅ Department updated successfully!")
                    # We add a rerun here to clear the old state and reload the new data
                    st.rerun() 
                    
                except Exception as e:
                    st.error(f"An error occurred: {e}")

    # --- Back Button ---
    if st.button("⬅️ Back to Admin Menu"):
        go_to("Admin_option")
        st.rerun()