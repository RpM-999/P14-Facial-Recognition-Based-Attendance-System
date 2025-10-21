

import streamlit as st
from supabase import create_client, Client

if "supabase" in st.session_state:
    supabase = st.session_state.supabase
else:
    try:
        url = st.secrets["supabase"]["url"]
        anon_key = st.secrets["supabase"]["anon_key"]
        
        supabase: Client = create_client(url, anon_key)
        
        # Store the connection in session state
        st.session_state.supabase = supabase
        
    except Exception as e:
        st.error(f"Error connecting to Supabase: {e}")
        st.stop()
        
