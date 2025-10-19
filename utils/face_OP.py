import face_recognition
import numpy as np

def encode_face(image):
    encodings = face_recognition.face_encodings(image)
    if len(encodings) > 0:
        return encodings[0]
    return None

def match_face(face_encoding, known_encodings, tolerance=0.7):
    matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance)
    if True in matches:
        index = matches.index(True)
        return index, True
    return -1, False
