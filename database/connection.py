import streamlit as st
import mysql.connector

def get_db_connection():
    conn = mysql.connector.connect(
        host=st.secrets["database"]["host"],
        port=st.secrets["database"]["port"],
        user=st.secrets["database"]["user"],
        password=st.secrets["database"]["password"],
        database=st.secrets["database"]["database"],
        ssl_ca=st.secrets["database"]["ssl_ca"],
        #ssl_verify_cert=True,
        #ssl_verify_identity=True
    )
    return conn
