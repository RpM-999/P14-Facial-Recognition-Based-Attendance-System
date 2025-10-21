import streamlit as st
from PIL import Image
import numpy as np
from datetime import datetime

from database.connection import get_db_connection
from database.student_OP import insert_student, get_all_students
from database.attendence_OP import get_attendance_report

from utils.face_OP import encode_face
from utils.extract_OP import to_csv, to_excel

from database.student_OP import get_departments
from database.admin_OP import admin_verification

#from pages.Admin_option import admin_optionsdmin_options


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in: 

    st.title("🔐 Admin Panel")
    email = st.text_input("Enter Admin Email")
    password = st.text_input("Enter Admin Password", type="password")




    if st.button("Login"):
        is_admin, message = admin_verification(email, password)
        if is_admin:
            st.session_state.logged_in = True
            st.session_state.admin_name = message
            st.success(f"✅ Login successful! Welcome, {message}")
            st.rerun()
        else:
            st.warning(f"❌ {message}")




if st.button("Forgot Password"):
    pass

"""
if password == "admin123":
    
                            )

    if admin_menu == "Add Student":

        st.header("➕ Add New Student")
        name = st.text_input("Student Name")
        email = st.text_input("Email")
        department_name = st.selectbox("Select Department",["CSE", 
                                                       "CSE-AIML", 
                                                       "CSE-DataScience", 
                                                       "CSE-IoT", 
                                                       "CSE-CyberSecurity", 
                                                       "ME", 
                                                       "ECE"]
                                    )
        
        department_id = get_departments(department_name)
        
                            )

        photo = st.camera_input("Take Student Photo")

        if st.button("Register Student"):
            if not all([name, email, department_id,year, photo]):
                st.warning("All fields are required!")
            else:
                image = Image.open(photo)
                rgb_img = np.array(image)
                face_encoding = encode_face(rgb_img)
                if face_encoding is None:
                    st.error("No face detected in the photo.")
                else:
                    encoded_str = np.array2string(face_encoding, separator=',')
                    photo_file = f"images/{name}_{department_name}_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
                    image.save(photo_file)
                    try:
                        roll_no,join_date = insert_student(name, email, department_id, year, encoded_str, photo_file)
                        st.success("✅ Student Registered  successfully.")
                        

    elif admin_menu == "View Attendance Report":
        st.subheader("📊 Attendance Report")
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("From Date")
        with col2:
            end_date = st.date_input("To Date")

        if st.button("Generate Report"):
            report_data = get_attendance_report(start_date, end_date)
            st.dataframe(report_data)
            st.download_button("Download CSV", to_csv(report_data), "attendance.csv", "text/csv")
            st.download_button("Download Excel", to_excel(report_data), "attendance.xlsx",
                               mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    elif admin_menu == "Add Attendance Manually":
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT student_id, name, roll_number FROM students")
        students = cursor.fetchall()
        conn.close()

        st.subheader("📝 Manual Attendance Entry")
        names = [f"{s['name']} ({s['roll_number']})" for s in students]
        selected_name = st.selectbox("Select Student", names)
        selected_id = students[names.index(selected_name)]['student_id']
        date = st.date_input("Date")
        time = st.time_input("Time")
        status = st.selectbox("Status", ["Present", "Absent", "Late"])

        if st.button("Submit Attendance"):
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO attendance (student_id, date, time, status) VALUES (%s, %s, %s, %s)",
                (selected_id, date, time, status)
            )
            conn.commit()
            conn.close()
            st.success("✅ Attendance added manually.")
else:
    if password:
        st.error("❌ Incorrect password.")

        
        """