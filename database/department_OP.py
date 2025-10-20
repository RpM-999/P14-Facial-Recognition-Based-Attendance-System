from database.connection import supabase
import streamlit as st


def add_department(dep_id , dep_name , dep_hod, dep_hod_mail):
    try:
        data = {
            "dep_id": dep_id,
            "dep_name": dep_name,
            "dep_hod": dep_hod,
            "dep_hod_mail": dep_hod_mail
        }
        supabase.table("department").insert(data).execute()
        
    except Exception as e:
        raise e
    
def get_all_departments():
    """Fetches all departments from the database."""
    try:
        response = supabase.table("department").select("*").order("dep_name").execute()
        return response.data
    except Exception as e:
        st.error(f"Error fetching departments: {e}")
        return []
    
def update_department(dep_id, dep_name ,dep_hod,dep_hod_mail):
    """
    Updates a specific department in the database using its dep_id.
    """
    try:
        
        new_data = {
            "dep_name": dep_name,
            "dep_hod": dep_hod,
            "dep_hod_mail": dep_hod_mail
        }
        supabase.table("department").update(new_data).eq("dep_id", dep_id).execute()
        
    except Exception as e:
        raise e