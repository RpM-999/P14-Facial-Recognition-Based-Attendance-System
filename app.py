import streamlit as st
# Import all your page modules
from UI import Home, Admin_login, Admin_option, Add_new_department ,Update_department_info 
from UI import Add_new_student
# --------------------- Session State Initialization ---
# -------------Initialize the current_page if it doesn't exist

if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

# Initialize the logged_in status if it doesn't exist

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- Router Logic ---
# Get the current page from the session state
page = st.session_state.current_page

# Based on the current page, call the appropriate function
if page == "Home":
    Home.show()

elif page == "Admin_login":
    # Using the .login() function as specified
    Admin_login.login_page() 

elif page == "Admin_option":
    if st.session_state.logged_in:
        Admin_option.admin_options_page()
    else:
        st.warning("🔒 Please log in to access the Admin Panel.")
        Admin_login.login_page()

elif page == "Add_new_department":
    
    if st.session_state.logged_in:
        Add_new_department.Add_new_department_page()
    else:
        st.warning("🔒 Please log in to access this page.")
        Admin_login.login_page()
        
        
        
elif page == "Update_department_info":
    if st.session_state.logged_in:
       Update_department_info.update_department_info_page()
    else:
        st.warning("🔒 Please log in to access this page.")
        Admin_login.login_page()
        
elif page == "Add_new_student":
    if st.session_state.logged_in:
       Add_new_student.add_new_students()
    else:
        st.warning("🔒 Please log in to access this page.")
        Admin_login.login_page()

# --- Add other pages below using the same pattern ---
# Example for a future student page:
# elif page == "add_new_student":
#     if st.session_state.logged_in:
#         add_new_student.show()
#     else:
#         st.warning("🔒 Please log in to access this page.")
#         Admin_login.login()


