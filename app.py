import streamlit as st
# Import all your page modules
from fun import Home, Admin_login, Admin_option, Add_new_department

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
    Admin_login.login() 

elif page == "Admin_option":
    # This block handles the security check before showing the admin options
    if st.session_state.logged_in:
        Admin_option.admin_options()
    else:
        st.warning("🔒 Please log in to access the Admin Panel.")
        # If not logged in, show the login page instead
        Admin_login.login()

elif page == "Add_new_department":
    
    if st.session_state.logged_in:
        Add_new_department.Add_new_department()
    else:
        st.warning("🔒 Please log in to access this page.")
        Admin_login.login()

# --- Add other pages below using the same pattern ---
# Example for a future student page:
# elif page == "add_new_student":
#     if st.session_state.logged_in:
#         add_new_student.show()
#     else:
#         st.warning("🔒 Please log in to access this page.")
#         Admin_login.login()

