
import streamlit as st
import torch
from PIL import Image
from facenet_pytorch import InceptionResnetV1, MTCNN

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')


@st.cache_resource

def load_models():
    
    mtcnn = MTCNN(
        image_size=160, 
        margin=0, 
        min_face_size=20,
        thresholds=[0.6, 0.7, 0.7], 
        factor=0.709,
        device=device

    )
    
    resnet = InceptionResnetV1(pretrained='vggface2').eval().to(device)
    
    return mtcnn, resnet

# Load the models once on startup
mtcnn, resnet = load_models()


def get_face_embedding(image):
    
    image_rgb = image.convert('RGB')
    face_tensor = mtcnn(image_rgb, save_path=None)
    if face_tensor is None:
        return None, " No face detected. Please try again."

    face_tensor = face_tensor.to(device)
    
    with torch.no_grad():
        embedding = resnet(face_tensor.unsqueeze(0))
    
   
    embedding_list = embedding.detach().cpu().numpy()[0].tolist()
    
    return embedding_list, " Face embedding created successfully!"


