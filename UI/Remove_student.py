import streamlit as st
from FUNC.navigation import go_to
from BACKEND.student_OP import get_student_by_id, delete_student

def remove_student():
    
    # --------------------------- Auth Check ---------------------------------------------
    
    
    if not st.session_state.get("logged_in"):
        st.warning("You must be logged in to view this page.")
        if st.button("Go to Login"):
            go_to("Admin_login")
            st.rerun()
        return

    st.title("Remove Student")

    # --------------------------------------- Initialize State -------------------------------------
    
    
    if "student_to_remove" not in st.session_state:
        st.session_state.student_to_remove = None



    # ---------------------------------------- Search Phase -------------------------------------------
    
    
    if st.session_state.student_to_remove is None:
        st.subheader("Step 1: Find Student to Remove")
        search_id = st.text_input("Enter Student ID to find (e.g., 251021-0000)")
        
        if st.button("Search"):
            if not search_id:
                st.warning("Please enter a Student ID.")
            else:
                with st.spinner("Searching..."):
                    student_data = get_student_by_id(search_id)
                    if student_data:
                        st.session_state.student_to_remove = student_data
                        st.rerun() 
                    else:
                        st.error("Student ID not found.")



    # ---------------------------------------- Confirmation Phase --------------------------------
    
    
    
    else:
        student = st.session_state.student_to_remove
        st.subheader("Step 2: Confirm Deletion")
        st.error(f"⚠️ You are about to permanently delete all data for:")
        st.markdown(f"**Name:** {student['S_name']}")
        st.markdown(f"**ID:** {student['S_id']}")
        st.markdown("This includes their information in Supabase and all face embeddings in Qdrant.")
        st.markdown("**This action cannot be undone.**")

        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Yes, Delete This Student", type="primary", width='stretch'):
                with st.spinner("Deleting student from all databases..."):
                    try:
                        delete_student(student['S_id'])
                        st.success(f"Successfully deleted {student['S_name']}.")
                        del st.session_state.student_to_remove
                        st.rerun()
                    except Exception as e:
                        st.error(f"An error occurred during deletion: {e}")

        with col2:
            if st.button("Cancel", width='stretch'):
                # Clear state to go back to search
                del st.session_state.student_to_remove
                st.rerun()
                
                

    # --------------------------------------- Back to Menu Button ------------------------------------
    
    
    
    st.markdown("---")
    if st.button("⬅️ Back to Admin Menu"):
        # Clear state if necessary before leaving
        if "student_to_remove" in st.session_state:
            del st.session_state.student_to_remove
        go_to("Admin_option")
        st.rerun()