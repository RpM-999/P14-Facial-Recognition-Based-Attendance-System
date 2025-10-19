import mysql.connector
from database.connection import get_db_connection


def add_department(d_id , d_name , d_hod_name, d_hod_email):
    try:
       
        conn = get_db_connection()
        cursor = conn.cursor()
        
    
        query = """
        INSERT INTO department (d_id, d_name, d_hod_name, d_hod_email) 
        VALUES (%s, %s, %s, %s)
        """
      
        args = (d_id, d_name, d_hod_name, d_hod_email)
        
        cursor.execute(query, args)
     
        conn.commit()
        
    except mysql.connector.Error as err:
        # If an error occurs (e.g., duplicate d_id), re-raise the exception
        # so the Streamlit page can catch it and display a user-friendly error.
        raise Exception(f"Database error: {err}")
        
    finally:
        # Ensure the connection is always closed, even if an error occurs
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
