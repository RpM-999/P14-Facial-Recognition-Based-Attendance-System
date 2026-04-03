
import streamlit as st
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PayloadSchemaType


# --------------------- PROVIDE THE NAME OF THE VECTOR DATABASE -----------------------------


QDRANT_COLLECTION_NAME = "student_face_encodings_"

try:

    # ------------------------------ GET SECRETS ---------------------------------


    qdrant_url = st.secrets["qdrant"]["url"]
    qdrant_api_key = st.secrets["qdrant"]["api_key"]
    

    # ------------------------------- INITIALIZE THE CLIENT---------------------------


    qdrant_client = QdrantClient(
        url=qdrant_url, 
        api_key=qdrant_api_key,
    )
    

    # ------------------------------------ ENSURE COLECTION EXIST ---------------------




    try:
        qdrant_client.get_collection(collection_name=QDRANT_COLLECTION_NAME)
    except Exception:
        st.warning("First-time setup: Creating Qdrant vector collection...")
        qdrant_client.create_collection(
            collection_name=QDRANT_COLLECTION_NAME,
            vectors_config=VectorParams(
                size=512,  
                distance=Distance.COSINE 
            )
        )
        st.success("Qdrant collection created!")


    # -------------------Ensure there is a payload index on S_id for filtered operations---------------------


    try:
        qdrant_client.create_payload_index(
            collection_name=QDRANT_COLLECTION_NAME,
            field_name="S_id",
            field_schema=PayloadSchemaType.KEYWORD,
        )
    except Exception:
        pass
         
except Exception as e:
    st.error(f"Error connecting to Qdrant: {e}")
    st.stop() 
    
    
    