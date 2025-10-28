import datetime
import pytz 
from PIL import Image
import streamlit as st 

from BACKEND.RDB_connection_OP import supabase
from BACKEND.student_OP import find_student_by_embedding, get_student_by_id
from FUNC.face_embedding_OP import get_face_embedding
from FUNC.attendance_gspread import connect_to_gsheet, write_to_sheet



# --------------------------------------- Time Configuration ------------------------------------------



try:
    LOCAL_TIMEZONE = pytz.timezone("Asia/Kolkata")
except pytz.UnknownTimeZoneError:
    LOCAL_TIMEZONE = pytz.utc 

ATTENDANCE_START_TIME = datetime.time(21,0,0)
ATTENDANCE_END_TIME = datetime.time(23, 0, 0)



#-------------------------------------- MAIN FUNCTION------------------------------------------------------


def identify_student_from_image(img_buffer):
    
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
            return {"status": "error", 
                    "message": f"Data Integrity Error: Matched face (ID: {student_id}) but student details are missing."}


        name = student_details.get('S_name', 'N/A')
        dept_id = student_details.get('dep_id', 'N/A') 

        return {"status" : "found",
                "message": f"Identified: {name} ({student_id})",
                "student_info": { 
                "S_id": student_id,
                "S_name": name,
                "dep_id": dept_id
            }
            
        }
    except Exception as e:
        return {"status": "error", 
                "message": "An unexpected system error occurred during identification."}
        
        
        
        
        
#------------------------------------------------------ LOGIN-ATTENDANCE-------------------------------------------------------------





def log_attendance_to_sheet(student_info: dict):
    
    if not student_info or not student_info.get("S_id"):
        return {"status": "error", 
                "message": "Invalid student information provided for logging."}

    try:
        attendance_sheet = connect_to_gsheet()
        if attendance_sheet is None:
             print("ERROR: Failed to connect to attendance Google Sheet for logging.")
             return {"status": "error", 
                     "message": "System Error: Failed to connect to the attendance log."}

        today_date_str = datetime.datetime.now(LOCAL_TIMEZONE).strftime("%Y-%m-%d") 
        attendance_data = {
            "Date": today_date_str,
            "S_id": student_info.get("S_id"),    
            "dep_id": student_info.get("dep_id")
        }

        success_write, msg_write = write_to_sheet(attendance_sheet, attendance_data)

        if success_write:
    
            return {"status": "success", 
                    "message": f"Attendance logged successfully for {student_info.get('S_name')} ({student_info.get('S_id')})."}
        else:
            
            return {"status": "error", "message": f"Failed to log attendance: {msg_write}."}

    except Exception as e:
        return {"status": "error", "message": "An unexpected system error occurred during logging."}