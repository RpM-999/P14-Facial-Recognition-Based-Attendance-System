import streamlit as st
import numpy as np
from PIL import Image

from database.student_OP import get_all_students
from database.attendence_OP import mark_attendance
from utils.face_OP import encode_face, match_face

st.title("📸 Give Attendance")

@st.cache_data
def load_known_faces():
    students = get_all_students()
    encodings, ids = [], []
    for s in students:
        if s['face_encoding']:
            enc = np.fromstring(s['face_encoding'][1:-1], sep=',')
            encodings.append(enc)
            ids.append(s['student_id'])
    return ids, encodings

picture = st.camera_input("Take a photo")
if picture:
    image = Image.open(picture)
    rgb_img = np.array(image)
    face_encoding = encode_face(rgb_img)

    if face_encoding is None:
        st.error("No face detected. Please try again.")
    else:
        ids, encodings = load_known_faces()
        index, matched = match_face(face_encoding, encodings)
        if matched:
            student_id = ids[index]
            mark_attendance(student_id)
            st.success("✅ Attendance marked successfully.")
        else:
            st.warning("⚠️ Face not recognized. Please contact admin.")
