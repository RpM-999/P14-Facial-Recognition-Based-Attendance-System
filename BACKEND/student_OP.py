

import datetime
import json
import uuid
from BACKEND.RDB_connection_OP import supabase
from BACKEND.VDB_connection_OP import qdrant_client, QDRANT_COLLECTION_NAME
from qdrant_client.http.models import PointStruct




def process_and_upload_students(student_records: list):
    
    try:
        
        today_str = datetime.datetime.now().strftime("%y%m%d")
        
        # 2. Check Supabase for the last ID used today
        response = supabase.table("students").select("student_id") \
                             .like("student_id", f"{today_str}-%") \
                             .order("student_id", desc=True) \
                             .limit(1).execute()

        start_index = 0
        if response.data:
            last_id = response.data[0]['student_id']
            last_index_str = last_id.split('-')[1]
            start_index = int(last_index_str) + 1

        supabase_batch_payload = []
        qdrant_points_payload = []
        current_index = start_index
        
        for record in student_records:
        
            new_student_id = f"{today_str}-{str(current_index).zfill(4)}"
            current_index += 1
            
            
            face_embeddings_json = record.pop("S_live_face_photos")
            face_embeddings_list = json.loads(face_embeddings_json)
            
            # 5. Prepare Supabase payload (the *rest* of the record)
            record['student_id'] = new_student_id  # Add the new ID
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
                            "student_id": new_student_id, # Link back to the student
                            "image_index": i # e.g., 0=front, 1=left, 2=right
                        }
                    )
                )
        
        # 7. Execute batch uploads
        if supabase_batch_payload:
            supabase.table("students").insert(supabase_batch_payload).execute()
        
        if qdrant_points_payload:
            qdrant_client.upsert(
                collection_name=QDRANT_COLLECTION_NAME,
                points=qdrant_points_payload,
                wait=True # Wait for the operation to complete
            )
        
        # Return the number of students processed
        return len(supabase_batch_payload)

    except Exception as e:
        raise e