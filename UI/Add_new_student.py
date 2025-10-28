import streamlit as st
from BACKEND.RDB_connection_OP import supabase
from FUNC.navigation import go_to
from FUNC.g_spread import connect_to_gsheet, read_from_sheet, clear_sheet
import json
import datetime
from BACKEND.student_OP import process_and_upload_students

REGISTRATION_FORM_URL = "https://p14-student-registration-form.streamlit.app/" 

# -----------------------------CONFIRM GOOGLE SHEET CONNECTION-----------------------------------

try:
    sheet = connect_to_gsheet()
except Exception as e:
    st.error(f"Could not connect to Google Sheets: {e}")
    st.stop()




def add_new_students():
    
    if not st.session_state.get("logged_in"):
        st.warning("You must be logged in to view this page.")
        if st.button("Go to Login"):
            go_to("Admin_login")
            st.rerun()
        return

    st.title("Student Registration Management")
    st.header("Form Control")
    st.write("Control the live student registration form.")
    
    col1, col2 = st.columns(2)
    
    
    
    #------------------------ AFTER OPENING STUDENT CAN REGISTER THEMSELF --------------------------
    
    
    
    if col1.button("🟩 Open Registration Form 🟩",width='stretch'):
        try:
            
            supabase.table("app_controls") \
                    .update({"is_registration_open": True}) \
                    .eq("is_registration_open", False) \
                    .execute()
            st.success("Registration Form is now LIVE.")
            st.info(f"Share this URL with students: {REGISTRATION_FORM_URL}")
        except Exception as e:
            st.error(f"Failed to open form: {e}")

    if col2.button("🟥 Close Registration Form 🟥", width='stretch'):
        try:
            
            supabase.table("app_controls") \
                    .update({"is_registration_open": False}) \
                    .eq("is_registration_open", True) \
                    .execute()
            st.warning("Registration Form is now CLOSED.")
        except Exception as e:
            st.error(f"Failed to close form: {e}")



    st.markdown("---")
    st.header("Data Upload")
    st.write("Pull student data from the temporary sheet and save it to the main database.")
    
    
    # ----------------------------UPLOAD DATA FROM GOOGLE SHEET TO DATABASE-------------------------------
    
    
    if st.button("Upload New Students to Database", width='stretch'):
        if sheet is None:
            st.error("Cannot connect to Google Sheet.")
            st.stop()
            
        with st.spinner("Fetching data from Google Sheet..."):
            student_records = read_from_sheet(sheet)
            if not student_records:
                st.warning("No new student records found in the sheet.")
                st.stop()
        
      
        with st.spinner(f"Found {len(student_records)} records. Processing and uploading..."):
            try:
                processed_count,email_success,email_fail = process_and_upload_students(student_records)
                
                st.success(f"✅ Successfully uploaded {processed_count} records!")
                st.info("Data split between Supabase (info) and Qdrant (embeddings).")
                
                
                
# ------------------------------------AFTER SUCCESSFULLY REGISTER THEY GOT MAIL-------------------------
                
                
                if email_success > 0:
                    st.success(f"📧 Sent {email_success} confirmation emails successfully.")
                if email_fail > 0:
                    st.warning(f"⚠️ Failed to send {email_fail} confirmation emails. Check logs or student email addresses.")
                
                cleared_successfully = clear_sheet(sheet)
                if cleared_successfully:
                    st.info("Temporary sheet has been cleared.")
                else:
                    st.error("Failed to clear the temporary sheet. Please check manually.")
                
            except Exception as e:
                st.error(f"Failed to upload to database: {e}")
                st.warning("Data has NOT been cleared from the sheet.")
    




    st.markdown("---")
    if st.button("🔙 Back to Admin Menu"):
        go_to("Admin_option")
        st.rerun()