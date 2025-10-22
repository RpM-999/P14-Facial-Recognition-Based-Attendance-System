import streamlit as st
# Import all your page modules
from UI import Home, Admin_login, Admin_option, Add_new_department ,Update_department_info 
from UI import Add_new_student ,Update_student_info , Remove_student

if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

#----------------------------------------------------------------------------------------


page = st.session_state.current_page

if page == "Home":
    Home.show()

elif page == "Admin_login":
    Admin_login.login_page() 

elif page == "Admin_option":
    if st.session_state.logged_in:
        Admin_option.admin_options_page()
    else:
        st.warning("🔒 Please log in to access the Admin Panel.")
        Admin_login.login_page()


#-------------------------------------------------------------------------------------------


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
        
        
#------------------------------------------------------------------------------------------
        
        
elif page == "Add_new_student":
    if st.session_state.logged_in:
       Add_new_student.add_new_students()
    else:
        st.warning("🔒 Please log in to access this page.")
        Admin_login.login_page()
        
        
elif page == "Update_student_info":
    if st.session_state.logged_in:
       Update_student_info.update_student()
    else:
        st.warning("🔒 Please log in to access this page.")
        Admin_login.login_page()
        
elif page == "Remove_student":
    if st.session_state.logged_in:
       Remove_student.remove_student()
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


