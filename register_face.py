import cv2
import numpy as np
import mysql.connector
import json
import face_recognition

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

conn = mysql.connector.connect(
    host="localhost",
    user="root",      
    password="mysql",  
    database="face_recognition_db"
)
cursor = conn.cursor()

# Paths to YOLO configuration, weights, and classes files
yolo_cfg = 'C:/Users/brlte/OneDrive/Desktop/Ultimate/yolo_files/yolov4.cfg'  # Path to YOLO configuration file
yolo_weights = 'C:/Users/brlte/OneDrive/Desktop/Ultimate/yolo_files/yolov4.weights'  # Path to YOLO weights file
coco_names = 'C:/Users/brlte/OneDrive/Desktop/Ultimate/yolo_files/coco.names'  # Path to the class labels (e.g., coco.names) 


with open(coco_names, 'r') as f:
    class_names = [line.strip() for line in f.readlines()]

# Load YOLO model
net = cv2.dnn.readNet(yolo_weights, yolo_cfg)


layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

video_path = input("Enter video path (leave empty for webcam): ").strip()

if video_path:
    cap = cv2.VideoCapture(video_path)  # Open recorded video
else:
    cap = cv2.VideoCapture(0)  # Open webcam

 
if not cap.isOpened():
    print("Error: Unable to access the webcam.")
    exit()

print("Press 'q' to exit the live detection.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Unable to capture frame.")
        break

    small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
    rgb_frame = np.ascontiguousarray(frame[:, :, ::-1])
    face_locations = face_recognition.face_locations(rgb_frame)
    name = None
    if face_locations:
        print("No faces detected.")
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        print(f"Image shape: {rgb_frame.shape}, dtype: {rgb_frame.dtype}")
        print(f"Face locations: {face_locations}")
        for face_encoding, face_location in zip(face_encodings, face_locations):
            match = find_matching_face(face_encoding)
            if match:
                name = match[1]
                print(f"Recognized: {name}")
                
                top, right, bottom, left = face_location
                top, right, bottom, left = [v * 2 for v in [top, right, bottom, left]]  # Scale back up
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            else:
                print("New face detected. Auto-registering...")
                new_name = f"User _{len(get_all_faces_from_db()) + 1}"
                register_new_face(new_name, face_encoding)
                break
    if name is None:
        fm = "None"
    else:
        fm = "Recognized person : " + name
        break

    