import datetime
import pytz # Make sure to install pytz (pip install pytz)
from PIL import Image
import streamlit as st # Only needed here if connect_to_gsheet uses st.secrets directly

from BACKEND.RDB_connection_OP import supabase
from BACKEND.student_OP import find_student_by_embedding, get_student_by_id
from UTILS.face_embedding_OP import get_face_embedding
from UTILS.attendance_gspread import connect_to_gsheet, write_to_sheet



# --------------------------------------- Time Configuration ------------------------------------------



try:
    LOCAL_TIMEZONE = pytz.timezone("Asia/Kolkata")
except pytz.UnknownTimeZoneError:
    print("Warning: Asia/Kolkata timezone not found, defaulting to UTC.")
    LOCAL_TIMEZONE = pytz.utc 

ATTENDANCE_START_TIME = datetime.time(8, 0, 0)
ATTENDANCE_END_TIME = datetime.time(10, 0, 0)



#-------------------------------------- MAIN FUNCTION------------------------------------------------------


def process_attendance_attempt(img_buffer):
    
    now_local_dt = datetime.datetime.now(LOCAL_TIMEZONE)
    now_local_time = now_local_dt.time()
    today_date_str = now_local_dt.strftime("%Y-%m-%d") 

    if not (ATTENDANCE_START_TIME <= now_local_time < ATTENDANCE_END_TIME):
        
        return {
            "status": "warning", 
            "message": f"Attendance window closed (Active: {ATTENDANCE_START_TIME.strftime('%I:%M %p')} - {ATTENDANCE_END_TIME.strftime('%I:%M %p')})."
        }

    if img_buffer is None:
        
         return {"status": "info", 
                 "message": "No image received from camera."}

    try:
        
        image = Image.open(img_buffer)
        live_embedding, msg_emb = get_face_embedding(image)
        
        
        if live_embedding is None:
            
            return {"status": "warning",
                    "message": f"Could not process face: {msg_emb}"}

        student_id, msg_search = find_student_by_embedding(live_embedding)
        
        if not student_id:
            return {"status": "error", 
                    "message": f"Attendance Failed: {msg_search}"}

        student_details = get_student_by_id(student_id)
        
        
        if not student_details:
            print(f"CRITICAL ERROR: Matched S_id {student_id} in Qdrant but not found in Supabase.")
            return {"status": "error", 
                    "message": f"Data Integrity Error: Matched face (ID: {student_id}) but student details are missing."}


        name = student_details.get('S_name', 'N/A')
        dept_id = student_details.get('dep_id', 'N/A') # Get the correct department foreign key

        attendance_data = {
            "Date": today_date_str, # Store today's date
            "S_id": student_id,    # Store the matched student ID
            "dep_id": dept_id      # Store the department ID
        }

        
        attendance_sheet = connect_to_gsheet()
        
        
        if attendance_sheet is None:
             
             print("ERROR: Failed to connect to attendance Google Sheet.")
             
             return {"status": "error", 
                     "message": "System Error: Failed to connect to the attendance log. Please contact admin."}

        success_write, msg_write = write_to_sheet(attendance_sheet, attendance_data)

        if success_write:

            return {
                "status": "success",
                "message": f"Attendance Logged for: **{name}**",
                "details": f"ID: {student_id} | Dept: {dept_id}" # Return details for display
            }
        else:
            
            print(f"ERROR: Failed to write attendance log to GSheet for {student_id}: {msg_write}")
            return {"status": "error", 
                    "message": f"Recognition OK, but failed to log attendance: {msg_write}. Please try again or contact admin."}

    except Exception as e:
        
        print(f"!!! UNEXPECTED ERROR in process_attendance_attempt for student {student_id if 'student_id' in locals() else 'unknown'}: {e}")
        # Return a generic error to the user
        return {"status": "error", 
                "message": f"An unexpected system error occurred during processing. Please contact admin."}

