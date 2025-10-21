
import streamlit as st
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams

# This will be the name of your vector "table"
QDRANT_COLLECTION_NAME = "student_face_encodings_"

try:
    # 1. Get secrets
    qdrant_url = st.secrets["qdrant"]["url"]
    qdrant_api_key = st.secrets["qdrant"]["api_key"]
    
    # 2. Initialize the client
    qdrant_client = QdrantClient(
        url=qdrant_url, 
        api_key=qdrant_api_key,
    )
    
    
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
         
except Exception as e:
    st.error(f"Error connecting to Qdrant: {e}")
    st.stop()