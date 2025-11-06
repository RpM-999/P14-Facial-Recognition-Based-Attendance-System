import streamlit as st
from FUNC.navigation import go_to

def show():
    st.title("🏫 Welcome to Student Attendance Management System")
    st.write("Please select an option:")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Admin Login"):
            go_to("Admin_login")         #------------------------------------------>> ONLY FOR ADMIN 
            
    with col2:
        if st.button("Give Attendance"):
            go_to("Give_attendance")      #------------------------------------------->> STUDENTS CAN GIVE ATTENDENCE
            
            
            
''''          
    with col2:
        if st.button("Department"):
            st.info("page coming soon")  #------------------------------------------->> DEPARTMENT
            
'''         
    