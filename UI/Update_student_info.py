import streamlit as st
from FUNC.navigation import go_to
from PIL import Image
from BACKEND.student_OP import get_student_by_id, update_student_info, update_student_embeddings
from FUNC.face_embedding_OP import get_face_embedding 


def update_student(): 
    
    
    
    # ---  MODIFIED SUCCESS HANDLING & INITIALIZATION ---
    

    if st.session_state.get("update_successful", False):
        st.success("Successfully updated all information!")
        st.session_state.update_successful = False

        if "student_to_edit" in st.session_state:
            del st.session_state.student_to_edit
        if "renew_face" in st.session_state:
             del st.session_state.renew_face 
        
        

    if "student_to_edit" not in st.session_state:
        st.session_state.student_to_edit = None
    if "renew_face" not in st.session_state:
        st.session_state.renew_face = False
    if st.session_state.student_to_edit is None:
        st.session_state.renew_face = False 
        
        
        
    # ---------------------------------------------------------------------------------------------

    # ----------------------------------------- AUTH CHECK ----------------------------------------
    
    
    
    if not st.session_state.get("logged_in"):
        st.warning("You must be logged in to view this page.")
        if st.button("Go to Login"):
            go_to("Admin_login")
            st.rerun()
        return

    st.title("Update Student Information")
    
    
    
    # ------------------------------- SEARCH STUDENT DETAILS -------------------------------------
    
    
    
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
                        st.rerun() 
                    else:
                        st.error("Student ID not found. Please check the ID and try again.")
                        
                        
    
    # ------------------------------------ RENEW STUDENT DETAILS --------------------------------------
    
    
    
    else:
        student = st.session_state.student_to_edit
        st.subheader(f"Editing Student: {student['S_name']} ({student['S_id']})")
        st.subheader("Facial Recognition Data")
        renew_face_data = st.checkbox(
            "Renew Face Embedding (Requires 3 New Photos)",
            key="renew_face" 
        )

        with st.form("update_student_form"):
            st.info("Update the student's information below.")
            s_name = st.text_input("Full Name", value=student['S_name'])
            s_mail = st.text_input("Email", value=student['S_mail'])
            s_phone = st.text_input("Phone Number", value=student['S_phone'])
            s_address = st.text_area("Address", value=student['S_Address'])
            
            
            
            st.markdown("---")
            
            
#--------------------------------- IF STUDENT FACE IS NOT RECOGNIZED------------------------------
            
            
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
                    
                    with st.spinner("Updating student information..."):
                        info_payload = { "S_name": s_name, "S_mail": s_mail, "S_phone": s_phone, "S_Address": s_address }
                        update_student_info(student['S_id'], info_payload)
                    
                  
                    if st.session_state.renew_face:
                        if not all([img_front, img_left, img_right]):
                            st.error("You checked 'Renew Face' but did not provide all 3 photos.")
                            st.stop()
                        with st.spinner("Processing new faces..."):
                            all_embeddings = [] 
                        
                            image_buffers = [img_front, img_left, img_right]
                            for i, img_buffer in enumerate(image_buffers):
                                image = Image.open(img_buffer)
                                embedding, message = get_face_embedding(image)
                                if embedding is None:
                                    st.error(f"Error with Photo {i+1}: {message}")
                                    st.stop()
                                all_embeddings.append(embedding)
                            update_student_embeddings(student['S_id'], all_embeddings)
                    
                    
                 
                    st.session_state.update_successful = True
                    st.rerun() 

                except Exception as e:
                    st.error(f"An error occurred during update: {e}")
                    
                    
                    
                    
    st.markdown("---")
    if st.button("⬅️ Back to Admin Menu"):
        if "student_to_edit" in st.session_state:
            del st.session_state.student_to_edit
        # 'renew_face' will be reset by logic at top
        go_to("Admin_option")
        st.rerun()
