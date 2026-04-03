import streamlit as st
from FUNC.navigation import go_to


def admin_options_page():
   
    
    
    if not st.session_state.get("logged_in"):
        st.warning("You must be logged in to view this page.")
        if st.button("Go to Login"):
            go_to("Admin_login")
        return 
    
    

    admin_name = st.session_state.get("admin_name", "Admin")

    # --- Sidebar Navigation Menu ---
    with st.sidebar:
        st.title(f"Welcome {admin_name}")
        st.header("Admin Menu",)
        
        
        
# ------------------------------- Student Management ----------------------------------


        st.subheader("Student Management")
        
        if st.button("Register Student", use_container_width=True):
            go_to("Add_new_student") 
            
        if st.button("Remove Student", use_container_width=True):
            go_to("Remove_student")
            
        if st.button("Update Student Info", use_container_width=True):
            go_to("Update_student_info")
            
        st.divider()
        
        
# ----------------------------- Department Management -------------------------------------

        st.subheader("Department Management")

        if st.button("Add Department", use_container_width=True):
            go_to("Add_new_department")

        if st.button("Update Department Info", use_container_width=True):
            go_to("Update_department_info")
            
        st.divider()


#------------------------------ Attendence Management ------------------------------------


    
        st.subheader("Attendence Management")
    
        if st.button("Attendance List",use_container_width=True):
            go_to("Attendence_list")
    
        #st.toggle("Monthly Upload",value=True
        # )
        
        st.divider()
            


# ---------------------------------------------------- Databricks Job Management -------------------------------------

        st.subheader("Databricks Job Management")

# ---job------------- Student ----------------

        if st.button("Upload Student Data", use_container_width=True,key="student_btn"):
            st.session_state.job_type = "student"
            go_to("Job_monitor")

# ---job------------- Department ----------------

        if st.button("Upload Department Data", use_container_width=True,key="department_btn"):
            st.session_state.job_type = "department"
            go_to("Job_monitor")


# ---------------- Attendance ----------------


        if st.button("Upload Attendance Data", use_container_width=True,key="attendance_btn"):
            st.session_state.job_type = "attendance"
            go_to("Job_monitor")



# ---------------- Full Pipeline ----------------

        if st.button("Upload All Data", use_container_width=True,key="full_btn"):
            st.session_state.job_type = "full"
            go_to("Job_monitor")


        st.divider()

# --------------------------------------- Admin Management ---------------------------------------


    

# ----------------------------------------- Logout Button ---------------------------------------


        if st.button("Logout", use_container_width=True, type="primary"):
            # Clear relevant session state keys on logout
            st.session_state.logged_in = False
            st.session_state.admin_name = None

            # ----------------------Redirect to the home page after logout---------------------------

            go_to("Home") 
            
            
            

    # --------------------------------------- Main Content Area ---------------------------------
    
    
    
    
    st.title("Admin Panel")
    st.info("Select an option from the sidebar to get started.")
    st.image(
        "IMAGES/admin panel image.png",
        caption="Welcome to the Admin Control Panel",
        width='stretch'

    )


