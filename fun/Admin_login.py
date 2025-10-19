import streamlit as st
from utils.navigation import go_to
from database.admin_OP import admin_verification 
from supabase import create_client ,Client


url = st.secrets["supabase"]["url"]
anon_key = st.secrets["supabase"]["anon_key"]

supabase :Client = create_client(url, anon_key)

def login():
    
    st.title("🔐 Admin Panel")
    
    with st.form("admin_login_form"):
        email = st.text_input("Enter Admin Email")
        password = st.text_input("Enter Admin Password", type="password")
        
        col1, col2 = st.columns(2)

        with col1:
            login_button = st.form_submit_button("Login", use_container_width=True)
        
        with col2:
            home_button = st.form_submit_button("Back to Home", use_container_width=True)
            
        if login_button:
            is_admin , message = admin_verification(email,password,supabase)
            
            if is_admin:
                st.session_state.logged_in = True
                st.session_state.admin_email = message
                st.success(f"✅ Login successful! Welcome")
                st.rerun()
            else:
                st.warning(f"❌ {message}")         
                
        if home_button:
            go_to("Home")           
'''
        if login_button:
            if admin_verification(email, password):
                st.session_state.logged_in = True
                st.session_state.admin_email = email
                # On successful login, go to the admin options page
                go_to("Admin_option")
            else:
                st.warning("❌ Invalid name or password")
  '''      
   


