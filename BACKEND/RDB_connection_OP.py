import streamlit as st
from supabase import create_client, Client

if "supabase" in st.session_state:
    supabase = st.session_state.supabase
else:
    try:
        url = st.secrets["supabase_api"]["url"]
        anon_key = st.secrets["supabase_api"]["anon_key"]
        
        supabase: Client = create_client(url, anon_key)
        
        # ------------------------ STORE SESSION STATE ----------------------------------------

        st.session_state.supabase = supabase
        
    except Exception as e:
        st.error(f"Error connecting to Supabase: {e}")
        st.stop()
        
