import cv2
import numpy as np
from take_screenshot import save_screenshot
from send_alert import twilio_alert, user_reply
from values import needed
import time
import os
from datetime import datetime
import face_recognition
import mysql.connector
import json
import numpy as np
from database_functions import get_all_faces_from_db, find_matching_face, register_new_face


# Paths to YOLO configuration, weights, and classes files
yolo_cfg = 'C:/Users/brlte/OneDrive/Desktop/Ultimate/yolo_files/yolov4.cfg'  # Path to YOLO configuration file
yolo_weights = 'C:/Users/brlte/OneDrive/Desktop/Ultimate/yolo_files/yolov4.weights'  # Path to YOLO weights file
coco_names = 'C:/Users/brlte/OneDrive/Desktop/Ultimate/yolo_files/coco.names'  # Path to the class labels (e.g., coco.names)


values = needed()

with open(coco_names, 'r') as f:
    class_names = [line.strip() for line in f.readlines()]

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

screenshot_taken = None
recording = False
video_writer = None
last_human_detected_time = None
owner_alert = 0
emergency = 0
face_recognition_details = ""
owner_presence = 0
fm = set()

screenrecord_dir = "C:/xampp/htdocs/screen_recordings"
if not os.path.exists(screenrecord_dir):
    os.makedirs(screenrecord_dir)

last_alert_time = None
response_tracker = {'device1': "-", 'device2': "-", 'device3': "-"}

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Unable to capture frame.")
        break
    
    height, width, _ = frame.shape
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    rgb_frame = np.ascontiguousarray(frame[:, :, ::-1])
    face_locations = face_recognition.face_locations(rgb_frame)
    reco_name = None
    net.setInput(blob)
    outs = net.forward(output_layers)

    boxes = []
    confidences = []
    class_ids = []

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.25:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)
    
    indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    human_detected = False

    if len(indices) > 0:
        for i in indices.flatten():
            box = boxes[i]
            x, y, w, h = box
            label = f"{class_names[class_ids[i]]}: {confidences[i]:.2f}"
            color = (0, 255, 0)

            if class_names[class_ids[i]].lower() == "person":
                human_detected = True
                last_human_detected_time = time.time()
                if recording:
                    break
                color = (0, 0, 255)

                if not screenshot_taken:
                    screenshot_taken = save_screenshot(frame)
                if not recording:
                    recording = True
                    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                    filename = os.path.join(screenrecord_dir, f"{timestamp}.mp4")
                    fourcc = cv2.VideoWriter_fourcc(*'H264')
                    video_writer = cv2.VideoWriter(filename, fourcc, 10, (width, height))
                    print(f"Recording started: {filename}")
                break           
    
    if screenshot_taken and owner_alert==0:
        twilio_alert(values['device1_x'], values['device1_y'], values['ngrok_link'], screenshot_taken, 0, 0, 0, None)
        twilio_alert(values['device2_x'], values['device2_y'], values['ngrok_link'], screenshot_taken, 0, 0, 1, None)
        twilio_alert(values['device3_x'], values['device3_y'], values['ngrok_link'], screenshot_taken, 0, 0, 2, None)
        print("ALERTS SENT 1")
        owner_alert = 1
        last_alert_time = time.time()

    start_time = time.time()
    device1_response = user_reply(values['device1_x'], values['device1_y'], 0)
    device2_response = user_reply(values['device2_x'], values['device2_y'], 1)
    device3_response = user_reply(values['device3_x'], values['device3_y'], 2)
    response_tracker['device1'] = device1_response
    response_tracker['device2'] = device2_response
    response_tracker['device3'] = device3_response

    if emergency == 0 and (device1_response=="yes" or device2_response=="yes" or device3_response=="yes"):
        twilio_alert(values['emg_x'], values['emg_y'], values['ngrok_link'], screenshot_taken, 1, 0, 3, None)
        print("EMERGENCY ALERT 1")
        #print(response_tracker)
        emergency = 1

    if face_locations:
        #print("No faces detected.")
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        #print(f"Image shape: {rgb_frame.shape}, dtype: {rgb_frame.dtype}")
        #print(f"Face locations: {face_locations}")
        for face_encoding, face_location in zip(face_encodings, face_locations):
            match = find_matching_face(face_encoding)
            if match:
                reco_name = match[1]
                print(f"Recognized: {reco_name}")
                if owner_presence == 0 and reco_name=="User _11":
                    twilio_alert(values['device1_x'], values['device1_y'], values['ngrok_link'], screenshot_taken, 4, 0, 0, None)
                    twilio_alert(values['device2_x'], values['device2_y'], values['ngrok_link'], screenshot_taken, 4, 0, 1, None)
                    twilio_alert(values['device3_x'], values['device3_y'], values['ngrok_link'], screenshot_taken, 4, 0, 2, None)
                    print("OWNER RECOGNISING ALERT ")
                    owner_presence = 1
            else:
                print("New face detected. Auto-registering...")
                new_name = f"Person _{len(get_all_faces_from_db()) + 1}"
                register_new_face(new_name, face_encoding)
    if reco_name is None:
        pass
    else:
        fm.add(reco_name)

    if human_detected:
        last_human_detected_time = time.time()
    else:
        if recording and last_human_detected_time and (time.time() - last_human_detected_time > 5):
            recording = False
            owner_presence = 0
            if video_writer:
                name = os.path.basename(filename) 
                video_writer.release()
                print(f"Recording stopped and saved: {filename}")
                twilio_alert(values['device1_x'], values['device1_y'], values['ngrok_link'], name, 2, 1, 0, None)
                twilio_alert(values['device1_x'], values['device1_y'], values['ngrok_link'], name, 3, 2, 0, fm)
                twilio_alert(values['device2_x'], values['device2_y'], values['ngrok_link'], name, 2, 1, 1, None)
                twilio_alert(values['device2_x'], values['device2_y'], values['ngrok_link'], name, 3, 2, 1, fm)
                twilio_alert(values['device3_x'], values['device3_y'], values['ngrok_link'], name, 2, 1, 2, None)
                twilio_alert(values['device3_x'], values['device3_y'], values['ngrok_link'], name, 3, 2, 2, fm)
                print("screen record and face alerts sent")
                if emergency==1:
                    twilio_alert(values['emg_x'], values['emg_y'], values['ngrok_link'], name, 2, 1, 3, None)
                    print("screen reco alert emergency")
                    emergency = 0
                video_writer = None
                fm.clear()

    if last_alert_time and (time.time() - last_alert_time > 600):  # 600 seconds = 10 minutes
        if not (device1_response=="yes" or device2_response=="yes" or device3_response=="yes"):  # If no response from any device
            twilio_alert(values['device1_x'], values['device1_y'], values['ngrok_link'], screenshot_taken, 0, 0, 0, None)
            twilio_alert(values['device2_x'], values['device2_y'], values['ngrok_link'], screenshot_taken, 0, 0, 1, None)
            twilio_alert(values['device3_x'], values['device3_y'], values['ngrok_link'], screenshot_taken, 0, 0, 2, None)
            print("ALERTS SENT 2")
            last_alert_time = time.time()

    # Do not send emergency alert if all devices replied with "no"
    if all(response == "no" for response in response_tracker.values()):
        emergency = 0
    
    if recording and video_writer:
        video_writer.write(frame)

    cv2.imshow("Live Object Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
if recording and video_writer:
    video_writer.release()
cv2.destroyAllWindows()