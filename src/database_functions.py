import face_recognition
import mysql.connector
import json
import numpy as np

conn = mysql.connector.connect(
    host="localhost",
    user="root",      
    password="mysql",  
    database="face_recognition_db"
)
cursor = conn.cursor()


def get_all_faces_from_db():
    cursor.execute("SELECT * FROM faces")
    return cursor.fetchall()

def find_matching_face(face_encoding):
    all_faces = get_all_faces_from_db()
    for row in all_faces:
        stored_encoding = np.array(json.loads(row[2]))  # Deserialize JSON
        match = face_recognition.compare_faces([stored_encoding], face_encoding)
        if True in match:
            return row
    return None

def register_new_face(name, face_encoding):
    try:
        encoding_string = json.dumps(face_encoding.tolist())  # Serialize to JSON
        cursor.execute("INSERT INTO faces (name, face_encoding) VALUES (%s, %s)", (name, encoding_string))
        conn.commit()
        print(f"Registered {name} successfully!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
