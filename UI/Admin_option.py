import streamlit as st
from UTILS.navigation import go_to


def admin_options_page():
   
    
    # --- Security Check --- Ensure the user is logged in to see this page
    if not st.session_state.get("logged_in"):
        st.warning("You must be logged in to view this page.")
        if st.button("Go to Login"):
            go_to("Admin_login")
        return # Stop execution if not logged in

    # Get the admin's name from session state to personalize the welcome message
    admin_name = st.session_state.get("admin_name", "Admin")

    # --- Sidebar Navigation Menu ---
    with st.sidebar:
        st.title(f"Welcome, {admin_name}")
        st.header("Admin Menu")
        
        # --- Student Management ---
        st.subheader("Student Management")
        if st.button("Register Student", use_container_width=True):
            go_to("add_new_student") 
        if st.button("Remove Student", use_container_width=True):
            go_to("remove_student")
        if st.button("Update Student Info", use_container_width=True):
            go_to("update_student_info")
        
        # --- Department Management ---fun\.py
        st.subheader("Department Management")

        if st.button("Add Department", use_container_width=True):
            # Corrected the page name to be consistent (lowercase)
            go_to("Add_new_department")

        if st.button("Update Department Info", use_container_width=True):
            go_to("Update_department_info")
            
        # ------------------- Admin Management ---
        st.subheader("System Administration")
        if st.button("Add New Admin", use_container_width=True):
            go_to("add_admin")
        if st.button("Remove Admin", use_container_width=True):
            go_to("remove_admin")
        
        st.divider()

        # --- Logout Button ---
        if st.button("Logout", use_container_width=True, type="primary"):
            # Clear relevant session state keys on logout
            st.session_state.logged_in = False
            st.session_state.admin_name = None
            # Redirect to the home page after logout
            go_to("Home") 

    # --- Main Content Area ---
    st.title("Admin Dashboard")
    st.info("Select an option from the sidebar to get started.")
    # Corrected the parameter from use_column_width to use_container_width
    st.image("https://images.unsplash.com/photo-1517048676732-d65bc937f952?q=80&w=2070&auto=format&fit=crop", 
             caption="Welcome to the Admin Control Panel",
             use_container_width=True)

