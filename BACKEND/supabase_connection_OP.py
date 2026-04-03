import streamlit as st

db_config = st.secrets["supabase_db"]

host = db_config["host"]
user = db_config["user"]
password = db_config["password"]