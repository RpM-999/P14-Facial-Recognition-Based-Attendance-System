
import streamlit as st
from utils.navigation import go_to
from database.connection import supabase 
from utils.g_spread import connect_to_gsheet, read_from_sheet, clear_sheet
import json
import datetime

# --- IMPORTANT ---
# This is the public URL you got after deploying App-2
REGISTRATION_FORM_URL = "https://p14-student-registration-form.streamlit.app/" 

try:
    sheet = connect_to_gsheet()
except Exception as e:
    st.error(f"Could not connect to Google Sheets: {e}")
    st.stop()

def ():
    
    if not st.session_state.get("logged_in"):
        st.warning("You must be logged in to view this page.")
        if st.button("Go to Login"):
            go_to("Admin_login")
            st.rerun()
        return

    st.title("Student Registration Management")

    # --- 1. Open/Close Form Buttons ---
    st.header("Form Control")
    st.write("Control the live student registration form.")
    
    col1, col2 = st.columns(2)
    if col1.button("🟢 Open Registration Form", width='stretch'):
        try:
            # We use .single() here because there is only one row
            supabase.table("app_controls").update({"is_registration_open": True}).single().execute()
            st.success("Registration Form is now LIVE.")
            st.info(f"Share this URL with students: {REGISTRATION_FORM_URL}")
        except Exception as e:
            st.error(f"Failed to open form: {e}")

    if col2.button("🔴 Close Registration Form", width='stretch'):
        try:
            supabase.table("app_controls").update({"is_registration_open": False}).single().execute()
            st.warning("Registration Form is now CLOSED.")
        except Exception as e:
            st.error(f"Failed to close form: {e}")

    st.markdown("---")

    # --- 2. Upload to Database Button ---
    st.header("Data Upload")
    st.write("Pull student data from the temporary sheet and save it to the main database.")
    
    if st.button("Upload New Students to Database", width='stretch', type="primary"):
        if sheet is None:
            st.error("Cannot connect to Google Sheet.")
            st.stop()
            
        with st.spinner("Fetching data from Google Sheet..."):
            student_records = read_from_sheet(sheet)
            if not student_records:
                st.warning("No new student records found in the sheet.")
                st.stop()
        
        with st.spinner(f"Found {len(student_records)} records. Generating IDs and uploading..."):
            try:
                # 1. Get today's date string in YYMMDD format
                today_str = datetime.datetime.now().strftime("%y%m%d")
                
                # 2. Check Supabase for the last ID used today
                response = supabase.table("students").select("student_id") \
                                     .like("student_id", f"{today_str}-%") \
                                     .order("student_id", desc=True) \
                                     .limit(1) \
                                     .execute()

                start_index = 0
                if response.data:
                    last_id = response.data[0]['student_id']   # e.g., '251021-0000'
                    last_index_str = last_id.split('-')[1]   # '0000'
                    start_index = int(last_index_str) + 1    # 1

                processed_records_with_ids = []
                current_index = start_index
                
                for record in student_records:
                    new_id = f"{today_str}-{str(current_index).zfill(4)}" # '251021-0001'
                    
                    record['student_id'] = new_id
                    
                    # Convert embedding string back to list/JSON
                    record["S_live_face_photos"] = json.loads(record["S_live_face_photos"])
                    
                    processed_records_with_ids.append(record)
                    current_index += 1
                
                # Insert all new records into Supabase 'students' table
                supabase.table("students").insert(processed_records_with_ids).execute()
                
                st.success(f"✅ Successfully uploaded {len(processed_records_with_ids)} records!")
                
                # Clear the sheet after successful upload
                clear_sheet(sheet)
                st.info("Temporary sheet has been cleared.")
                
            except Exception as e:
                st.error(f"Failed to upload to database: {e}")
                st.warning("Data has NOT been cleared from the sheet.")

    st.markdown("---")
    if st.button("⬅️ Back to Admin Menu"):
        go_to("Admin_option")
        st.rerun()