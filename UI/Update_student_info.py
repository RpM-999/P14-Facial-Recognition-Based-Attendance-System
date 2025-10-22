import streamlit as st
from UTILS.navigation import go_to
from PIL import Image
from BACKEND.student_OP import get_student_by_id, update_student_info, update_student_embeddings
from UTILS.face_embedding_OP import get_face_embedding 

# --- Rename function to show() if needed for your router ---
def update_student(): # Or keep as update_student() if your router calls that
    
    # --- 1. MODIFIED SUCCESS HANDLING & INITIALIZATION ---
    
    # Check if a successful update just happened
    if st.session_state.get("update_successful", False):
        st.success("Successfully updated all information!")
        # Clear the flag immediately
        st.session_state.update_successful = False
        # Delete the student data to go back to search view
        if "student_to_edit" in st.session_state:
            del st.session_state.student_to_edit
        if "renew_face" in st.session_state:
             del st.session_state.renew_face # Clean up renew_face too
        # NO RERUN HERE - Let Streamlit redraw naturally
        
    # Standard initialization (this part is fine)
    if "student_to_edit" not in st.session_state:
        st.session_state.student_to_edit = None
    if "renew_face" not in st.session_state:
        st.session_state.renew_face = False
    if st.session_state.student_to_edit is None:
        st.session_state.renew_face = False # Ensure reset when searching
    # --------------------------------------------------

    # --- (Auth check - fine) ---
    if not st.session_state.get("logged_in"):
        st.warning("You must be logged in to view this page.")
        if st.button("Go to Login"):
            go_to("Admin_login")
            st.rerun()
        return

    st.title("Update Student Information")
    
    # --- (Search phase - fine) ---
    if st.session_state.student_to_edit is None:
        st.subheader("Find Student")
        search_id = st.text_input("Enter Student ID to find (e.g., 251021-0000)")
        if st.button("Search"):
            if not search_id:
                st.warning("Please enter a Student ID.") # Improved message
            else:
                with st.spinner("Searching..."):
                    student_data = get_student_by_id(search_id)
                    if student_data:
                        st.session_state.student_to_edit = student_data
                        # st.success(f"Found student: {student_data['S_name']}") # Optional: Remove for cleaner transition
                        st.rerun() 
                    else:
                        st.error("Student ID not found. Please check the ID and try again.")
    
    # --- (Edit phase - fine) ---
    else:
        student = st.session_state.student_to_edit
        st.subheader(f"Editing Student: {student['S_name']} ({student['S_id']})")
        st.subheader("Facial Recognition Data")
        renew_face_data = st.checkbox(
            "Renew Face Embedding (Requires 3 New Photos)",
            key="renew_face" 
        )

        with st.form("update_student_form"):
            # ... (Your form inputs: s_name, s_mail, etc. - fine) ...
            st.info("Update the student's information below.")
            s_name = st.text_input("Full Name", value=student['S_name'])
            s_mail = st.text_input("Email", value=student['S_mail'])
            s_phone = st.text_input("Phone Number", value=student['S_phone'])
            s_address = st.text_area("Address", value=student['S_Address'])
            
            st.markdown("---")
            
            # ... (Your camera inputs - fine) ...
            img_front, img_left, img_right = None, None, None
            if st.session_state.renew_face:
                st.warning("Please provide 3 new, clear photos.")
                col_img1, col_img2, col_img3 = st.columns(3)
                img_front = col_img1.camera_input("1. New Front View", key="cam_front")
                img_left = col_img2.camera_input("2. New Left View", key="cam_left")
                img_right = col_img3.camera_input("3. New Right View", key="cam_right")
            
            st.markdown("---")
            
            submitted = st.form_submit_button("Update Student Information")

            if submitted:
                try:
                    # --- (Update logic - fine) ---
                    # ... (Updating text info) ...
                    with st.spinner("Updating student information..."):
                        info_payload = { "S_name": s_name, "S_mail": s_mail, "S_phone": s_phone, "S_Address": s_address }
                        update_student_info(student['S_id'], info_payload)
                    
                    # ... (Updating face info) ...
                    if st.session_state.renew_face:
                        if not all([img_front, img_left, img_right]):
                            st.error("You checked 'Renew Face' but did not provide all 3 photos.")
                            st.stop()
                        with st.spinner("Processing new faces..."):
                            all_embeddings = [] 
                            # (Your logic to get embeddings)
                            image_buffers = [img_front, img_left, img_right]
                            for i, img_buffer in enumerate(image_buffers):
                                image = Image.open(img_buffer)
                                embedding, message = get_face_embedding(image)
                                if embedding is None:
                                    st.error(f"Error with Photo {i+1}: {message}")
                                    st.stop()
                                all_embeddings.append(embedding)
                            update_student_embeddings(student['S_id'], all_embeddings)
                    
                    # --- 6. MODIFIED: Just set flag and rerun ---
                    st.session_state.update_successful = True
                    st.rerun() # This rerun triggers the success block at the top

                except Exception as e:
                    st.error(f"An error occurred during update: {e}")
    st.markdown("---")
    if st.button("⬅️ Back to Admin Menu"):
        if "student_to_edit" in st.session_state:
            del st.session_state.student_to_edit
        # 'renew_face' will be reset by logic at top
        go_to("Admin_option")
        st.rerun()

'''   # --- (Cancel button - fine, simplified cleanup) ---
        if st.button("Cancel and Search for Another Student"):
            if "student_to_edit" in st.session_state:
                 del st.session_state.student_to_edit
            # 'renew_face' will be reset by logic at top
            st.rerun()



    # --- (Back to Menu button - fine, simplified cleanup) ---
    st.markdown("---")
    if st.button("⬅️ Back to Admin Menu"):
        if "student_to_edit" in st.session_state:
            del st.session_state.student_to_edit
        # 'renew_face' will be reset by logic at top
        go_to("Admin_option")
        st.rerun()
'''