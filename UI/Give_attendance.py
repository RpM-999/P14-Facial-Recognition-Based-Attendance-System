import streamlit as st
from UTILS.navigation import go_to # Assuming go_to is still needed for Back button
from PIL import Image
# Import only the backend processing function
from BACKEND.attendance_OP import process_attendance_attempt
# Import time constants for display
from BACKEND.attendance_OP import ATTENDANCE_START_TIME, ATTENDANCE_END_TIME, LOCAL_TIMEZONE
import datetime

def give_attendence():   

    st.title("📸 Mark Student Attendance")

    
    now_local_time = datetime.datetime.now(LOCAL_TIMEZONE).time()
    is_window_open = (ATTENDANCE_START_TIME <= now_local_time < ATTENDANCE_END_TIME)

    if is_window_open:
        st.info(f"Attendance window is OPEN ({ATTENDANCE_START_TIME.strftime('%I:%M %p')} - {ATTENDANCE_END_TIME.strftime('%I:%M %p')}). Center face below.")
    else:
        st.warning(f"Attendance window is CLOSED (Active: {ATTENDANCE_START_TIME.strftime('%I:%M %p')} - {ATTENDANCE_END_TIME.strftime('%I:%M %p')}).")
        st.info(f"Current time: {now_local_time.strftime('%I:%M:%S %p %Z')}")

    img_buffer = None
    if is_window_open:
        img_buffer = st.camera_input("Camera Feed", key="attendance_cam", label_visibility="collapsed")

    if img_buffer and is_window_open:
        with st.spinner("Processing..."):
            
            result = process_attendance_attempt(img_buffer)
            
            status = result.get("status", "error")
            message = result.get("message", "An unknown error occurred.")

            if status == "success":
                st.success(message)
                details = result.get("details")
                if details: st.subheader(details)
                st.balloons()
            elif status == "warning": st.warning(message)
            elif status == "error": st.error(message)
            elif status == "info": st.info(message)
            else: st.error(message)

    # --- Back Button (Now goes to Home) ---
    st.markdown("---")
    # --- 2. MODIFY BACK BUTTON DESTINATION ---
    if st.button("⬅️ Back to Home"): # Changed label and destination
        go_to("Home") # Go back to the main public page
        st.rerun()
    # --------------------------------------

