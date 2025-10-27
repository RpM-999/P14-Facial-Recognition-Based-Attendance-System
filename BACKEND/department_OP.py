from BACKEND.RDB_connection_OP import supabase
import streamlit as st


#---------------------------------ADD NEW DEPARTMENT--------------------------------------------




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
    
    
    
#---------------------------------RETRIVE ALL THE DEPARTMENTS--------------------------------------
    
    
def get_all_departments():
    """Fetches all departments from the database."""
    try:
        response = supabase.table("department").select("*").order("dep_name").execute()
        return response.data
    except Exception as e:
        st.error(f"Error fetching departments: {e}")
        return []
    
    
#------------------------------------ UPDATE DEPARTMENT INFORMATIONS --------------------------------


    
def update_department(dep_id, dep_name ,dep_hod,dep_hod_mail):
    try:
        
        new_data = {
            "dep_name": dep_name,
            "dep_hod": dep_hod,
            "dep_hod_mail": dep_hod_mail
        }
        supabase.table("department").update(new_data).eq("dep_id", dep_id).execute()
        
    except Exception as e:
        raise e
    
    
#------------------------------- FETCH DEPARTMENT INFO ----------------------------------------------


def get_departments_with_hod():
    try:
        response = supabase.table("department") \
                           .select("dep_id, dep_name, dep_hod_mail") \
                           .order("dep_name", desc=False) \
                           .execute()

        return response.data

    except Exception as e:
        st.error(f"Could not fetch department list with HOD info: {e}")
        return [] 