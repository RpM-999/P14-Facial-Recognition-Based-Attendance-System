import streamlit as st
from FUNC.navigation import go_to

def show():
    st.title(" Admin Access Management Portal ")
    st.write("Admin Authentication Required")
    
    col1, col2 ,col3 = st.columns(3)
    with col2:
        if st.button("Admin Login"):
            go_to("Admin_login")         #------------------------------------------>> ONLY FOR ADMIN 
    '''        
    with col2:
        if st.button("Give Attendance"):
            go_to("Give_attendance")      #------------------------------------------->> STUDENTS CAN GIVE ATTENDENCE
    '''         
            
            
''''          
    with col2:
        if st.button("Department"):
            st.info("page coming soon")  #------------------------------------------->> DEPARTMENT
            
'''         
    