import streamlit as st
from UTILS.navigation import go_to # Assuming go_to is still needed for Back button
from PIL import Image
from BACKEND.attendance_OP import identify_student_from_image, log_attendance_to_sheet
from BACKEND.attendance_OP import ATTENDANCE_START_TIME, ATTENDANCE_END_TIME, LOCAL_TIMEZONE
import datetime




#-------------------------------------------- START NEW SESSIONS----------------------------------------------------------------




if "identified_student" not in st.session_state:
    st.session_state.identified_student = None
    
if "log_result" not in st.session_state:
    st.session_state.log_result = None



#----------------------------------------------- MAIN FUNCTIONS------------------------------------------------------------------



def give_attendence():   

    st.title("📸 Mark Student Attendance")
    
    if st.session_state.log_result:
        status = st.session_state.log_result.get("status")
        message = st.session_state.log_result.get("message")
        if status == "success":
            st.success(message)
        else:
            st.error(message)
        st.session_state.log_result = None




#--------------------------------------------- ENEBLE CAMERA FOR CERTAIN DURATION TO MAINTAIN DESCIPLINE ------------------------------------------------



    
    now_local_time = datetime.datetime.now(LOCAL_TIMEZONE).time()
    is_window_open = (ATTENDANCE_START_TIME <= now_local_time < ATTENDANCE_END_TIME)

    if not is_window_open:
        st.warning(f"Attendance window is CLOSED (Active: {ATTENDANCE_START_TIME.strftime('%I:%M %p')} - {ATTENDANCE_END_TIME.strftime('%I:%M %p')}).")
        st.info(f"Current time: {now_local_time.strftime('%I:%M:%S %p %Z')}")
        st.markdown("---")
        if st.button("⬅️ Back to Home"):
             st.session_state.identified_student = None
             st.session_state.log_result = None
             go_to("Home")
             st.rerun()
        return
    else:
        st.info(f"Attendance window is OPEN ({ATTENDANCE_START_TIME.strftime('%I:%M %p')} - {ATTENDANCE_END_TIME.strftime('%I:%M %p')}). Center face below.")





#------------------------------------------- IF ON-TIME OPEN THE CAMERA---------------------------------------------------------------



    img_buffer = None
    show_camera = is_window_open and st.session_state.identified_student is None
    if show_camera:
        img_buffer = st.camera_input(
            "Camera Feed",
            key="attendance_cam",
            label_visibility="collapsed",
            disabled=not is_window_open
        )
        
        
# --------------------------------------------- CAPTURE FACE FIND EMBEDDING ------------------------------------------------------------



        
    if img_buffer and show_camera:
        with st.spinner("Identifying..."):
            result = identify_student_from_image(img_buffer)
            status = result.get("status")

            if status == "found":
                st.session_state.identified_student = result.get("student_info")
                st.rerun()
            elif status in ["error", "warning", "info"]:
                if status == "error": st.error(result.get("message"))
                else: st.warning(result.get("message"))
            else:
                st.error("An unknown identification error occurred.")
                
             
                
                
    if st.session_state.identified_student is not None:
        student_info = st.session_state.identified_student
        st.subheader("Confirm Attendance:")
        st.write(f"**Name:** {student_info.get('S_name', 'N/A')}")
        st.write(f"**ID:** {student_info.get('S_id', 'N/A')}")
        
        
        
        
#---------------------------------------- CHECK YOUR NAME AND ID ------ IF OK --- CONFIRM ATTENDENCE------ELSE ------CANCEL-----------------



        
        col_confirm, col_cancel = st.columns(2)
        with col_confirm:
            if st.button("✔️ Confirm & Log Attendance", type="primary", width='stretch'):
                with st.spinner("Logging attendance..."):
                    log_result = log_attendance_to_sheet(student_info)
                    st.session_state.log_result = log_result
                    st.session_state.identified_student = None
                    st.rerun()

        with col_cancel:
            if st.button("❌ Cancel", width='stretch'):
                st.session_state.identified_student = None
                st.rerun()




    # ---------------------------------------------------- Back Button (Now goes to Home) ----------------------------------------------------
    
    
    
    st.markdown("---")
    if st.button("⬅️ Back to Home"): 
        go_to("Home") 
        st.rerun()
        
        
        
    # ----------------------------------------------------------------------------------------------------------------------------------------------

