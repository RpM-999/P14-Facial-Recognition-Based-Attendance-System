
import streamlit as st
import datetime
import json
import uuid
from BACKEND.RDB_connection_OP import supabase
from BACKEND.VDB_connection_OP import qdrant_client, QDRANT_COLLECTION_NAME
from qdrant_client.http.models import PointStruct, Filter, FieldCondition, MatchValue
from UTILS.send_email import send_registration_email



def process_and_upload_students(student_records: list):
    
    processed_students_for_email = []
    
    try:
        
        today_str = datetime.datetime.now().strftime("%y%m%d")
        
        # 2. Check Supabase for the last ID used today
        response = supabase.table("students").select("S_id") \
                             .like("S_id", f"{today_str}-%") \
                             .order("S_id", desc=True) \
                             .limit(1).execute()

        start_index = 0
        if response.data:
            last_id = response.data[0]['S_id']
            last_index_str = last_id.split('-')[1]
            start_index = int(last_index_str) + 1

        supabase_batch_payload = []
        qdrant_points_payload = []
        current_index = start_index
        
        for record in student_records:
        
            new_student_id = f"{today_str}-{str(current_index).zfill(4)}"
            current_index += 1
            
            student_detail_for_email = record.copy()
            student_detail_for_email['S_id'] = new_student_id
            processed_students_for_email.append(student_detail_for_email)
            
            
            face_embeddings_json = record.pop("S_live_face_photos")
            face_embeddings_list = json.loads(face_embeddings_json)
            
            # 5. Prepare Supabase payload (the *rest* of the record)
            
            
            record['S_id'] = new_student_id  # Add the new ID
            supabase_batch_payload.append(record)
            
            
            
            # 6. Prepare Qdrant payload (one point for each embedding)
            
            
            for i, embedding in enumerate(face_embeddings_list):
                # We need a unique ID for each vector point
                point_id = str(uuid.uuid4())
                
                qdrant_points_payload.append(
                    PointStruct(
                        id=point_id,
                        vector=embedding,
                        payload={
                            "S_id": new_student_id, # Link back to the student
                            "image_index": i # e.g., 0=front, 1=left, 2=right
                        }
                    )
                )  
        
        if supabase_batch_payload:
            supabase.table("students").insert(supabase_batch_payload).execute()
        
        if qdrant_points_payload:
            qdrant_client.upsert(
                collection_name=QDRANT_COLLECTION_NAME,
                points=qdrant_points_payload,
                wait=True # Wait for the operation to complete
            )
            
            
            
        email_success_count = 0
        email_fail_count = 0
        st.write("Sending confirmation emails...") # Give feedback in UI
        email_progress_bar = st.progress(0)
        
        
        for i, student_detail in enumerate(processed_students_for_email):
            success, message = send_registration_email(student_detail)
            if success:
                email_success_count += 1
            else:
                email_fail_count += 1
            email_progress_bar.progress((i + 1) / len(processed_students_for_email))

        return len(supabase_batch_payload),email_success_count,email_fail_count

    except Exception as e:
        raise e
    
    
    
    
    #------------------------------------------------ RETIVE STUDENT DATAILS------------------------------------------
    
    
    
    
def get_student_by_id(S_id):
    try:
        response = supabase.table("students").select("*") \
                           .eq("S_id", S_id).single().execute()
        return response.data
    except Exception as e:
        print(f"Error getting student: {e}")
        return None
    
def update_student_info(S_id, new_data):
    try:
        supabase.table("students").update(new_data) \
                .eq("S_id", S_id).execute()
    except Exception as e:
        raise e 
    
    
    
    
    
    #---------------------- UPDATE STUDENT FACE EMBEDDING WHOSE FACE RECOGNITION DOESNOT WORK PROPERLY----------
    
    
    
    

def update_student_embeddings(S_id, new_embeddings_list):
    
    try:
        qdrant_client.delete(
            collection_name=QDRANT_COLLECTION_NAME,
            points_selector=Filter(
                must=[
                    FieldCondition(
                        key="S_id", 
                        match=MatchValue(value=S_id)
                    )
                ]
            )
        )
        
        qdrant_points_payload = []
        for i, embedding in enumerate(new_embeddings_list):
            point_id = str(uuid.uuid4()) 
            
            qdrant_points_payload.append(
                PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload={
                        "S_id": S_id,
                        "image_index": i
                    }
                )
            )
            
        if qdrant_points_payload:
            qdrant_client.upsert(
                collection_name=QDRANT_COLLECTION_NAME,
                points=qdrant_points_payload,
                wait=True
            )
            
    except Exception as e:
        raise e
    
    
    
    #-------------------------------------- DELETE STUDENT DETAILS ---------------------------------------------
    
    
    
def delete_student(student_id: str):
    try:
        
        qdrant_client.delete(
            collection_name=QDRANT_COLLECTION_NAME,
            points_selector=Filter(
                must=[
                    FieldCondition(
                        key="S_id", # Match the payload key used during upload
                        match=MatchValue(value=student_id)
                    )
                ]
            )
        )
        
    
        supabase.table("students").delete().eq("S_id", student_id).execute()
        
    except Exception as e:
        # Raise the error to be handled by the frontend
        raise e
