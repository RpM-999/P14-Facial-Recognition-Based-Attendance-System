import streamlit as st
from UI import Home, Admin_login, Admin_option, Add_new_department ,Update_department_info 
from UI import Add_new_student ,Update_student_info , Remove_student , Give_attendance
from UI import Attendance_list
from UI import Add_admin , Remove_admin

if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

#----------------------------------------------------------------- LANDING PAGE -----------------------------------------------


page = st.session_state.current_page

if page == "Home":
    Home.show()

elif page == "Admin_login":
    Admin_login.login_page() 

elif page == "Admin_option":
    if st.session_state.logged_in:
        Admin_option.admin_options_page()
    else:
        st.warning(" Please log in to access the Admin Panel.")
        Admin_login.login_page()


#------------------------------------------------------------------------------------------- ADMIN/ DEPARTMENT ------------------------------------


elif page == "Add_new_department":
    
    if st.session_state.logged_in:
        Add_new_department.Add_new_department_page()
    else:
        st.warning(" Please log in to access this page.")
        Admin_login.login_page()
        
elif page == "Update_department_info":
    if st.session_state.logged_in:
       Update_department_info.update_department_info_page()
    else:
        st.warning(" Please log in to access this page.")
        Admin_login.login_page()
        
        
#------------------------------------------------------------------------------------------ ADMIN/STUDENT ---------------------------------------------------
        
        
elif page == "Add_new_student":
    if st.session_state.logged_in:
       Add_new_student.add_new_students()
    else:
        st.warning(" Please log in to access this page.")
        Admin_login.login_page()
        
        
elif page == "Update_student_info":
    if st.session_state.logged_in:
       Update_student_info.update_student()
    else:
        st.warning(" Please log in to access this page.")
        Admin_login.login_page()
        
elif page == "Remove_student":
    if st.session_state.logged_in:
       Remove_student.remove_student()
    else:
        st.warning(" Please log in to access this page.")
        Admin_login.login_page()
        
    
    #------------------------------------------------------------------------------------- GIVE ATTENDENCE ------------------------------------------
    
elif page == "Give_attendance":
    Give_attendance.give_attendence()
        
        
#-------------------------------------------------- ADMIN/ATTENDANCE ---------------------------------



elif page == "Attendence_list":
    if st.session_state.logged_in:
       Attendance_list.attendance_list()
    else:
        st.warning(" Please log in to access this page.")
        Admin_login.login_page()
        

#---------------------------------------------------- ADMIN/ADMIN------------------------------------

elif page == "Add_admin":
    if st.session_state.logged_in:
        Add_admin.add_admin()
    else:
        st.warning(" Please log in to access this page.")
        Admin_login.login_page()
        
        
        
elif page == "Remove_admin":
    if st.session_state.logged_in:
        Remove_admin.remove_admin()
    else:
        st.warning(" Please log in to access this page.")
        Admin_login.login_page()




#-----------------------------------------------------------------------------------------------------













# --- Add other pages below using the same pattern ---
# Example for a future student page:
# elif page == "add_new_student":
#     if st.session_state.logged_in:
#         add_new_student.show()
#     else:
#         st.warning("🔒 Please log in to access this page.")
#         Admin_login.login()


