import streamlit as st
from UTILS.navigation import go_to

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
            # Corrected the page name to be consistent (lowercase)
            go_to("Add_new_department")

        if st.button("Update Department Info", use_container_width=True):
            go_to("Update_department_info")
            
        st.divider()


#------------------------------ Attendence Management ------------------------------------


    
        st.subheader("Attendence Management")
    
        if st.button("Attendance List",use_container_width=True):
            go_to("Attendence_list")
    
        st.toggle("Monthly Upload",value=True
              )
        
        st.divider()
            
            
# -------------------------- Admin Management ---------------------------------------------


        st.subheader("System Administration")
        if st.button("Add New Admin", use_container_width=True):
            go_to("add_admin")
        if st.button("Remove Admin", use_container_width=True):
            go_to("remove_admin")
        
        st.divider()

# ----------------------------------------- Logout Button ---------------------------------------


        if st.button("Logout", use_container_width=True, type="primary"):
            # Clear relevant session state keys on logout
            st.session_state.logged_in = False
            st.session_state.admin_name = None
            # Redirect to the home page after logout
            go_to("Home") 
            
            
            

    # --------------------------------------- Main Content Area ---------------------------------
    
    
    
    
    st.title("Admin Panel")
    st.info("Select an option from the sidebar to get started.")
    # Corrected the parameter from use_column_width to use_container_width
    st.image(
        "IMAGES/img.png",
        caption="Welcome to the Admin Control Panel",
        width='stretch' 
    )


