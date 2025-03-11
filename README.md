# Real-Time-Video-Object-Detection-Using-YOLO-and-Computer-Vision-with-Automated-WhatsApp-Alerts-for-Security-and-Surveillance.


### Abstract:
The Human Detection and WhatsApp Alert System is an AI-driven security solution that utilizes YOLO (You Only Look Once) object detection to identify human presence in real-time. The system captures live video from a webcam, detects humans, and upon detection, takes a screenshot and sends an automated WhatsApp alert via Twilio API.

## Key Features
### Real-Time Human Detection:

* Uses YOLOv4 to detect humans in real-time from a webcam or video feed.
* Captures screenshots and records video when a human is detected.

### Face Recognition:

* Recognizes known faces using the face_recognition library.
* Auto-registers new faces and stores their encodings in a MySQL database.

### Alert System:

* Sends WhatsApp alerts to multiple devices using Twilio.
* Provides options for emergency alerts and user responses (e.g., "yes" or "no").

### Local Server Hosting:

* Uses XAMPP to host screenshots and screen recordings locally.
* Ngrok is used to expose the local server to the internet for remote access.

### Database Integration:

* Stores face encodings and metadata in a MySQL database.
* Supports querying and matching faces in real-time.

### User Interaction:

* Allows users to respond to alerts via WhatsApp.
* Tracks user responses and triggers emergency alerts if necessary.

## Tools and Technologies Used
### YOLOv4:
A state-of-the-art object detection model used for detecting humans in the video feed.

### OpenCV:
Used for image processing, video capture, and displaying the live feed.

### face_recognition Library:
A Python library for face detection and recognition.

### Twilio:
A cloud communications platform used for sending WhatsApp alerts.

### Ngrok:
A tool to expose local servers to the internet, allowing remote access to screenshots and recordings.

### XAMPP:
A local server solution used to host screenshots and recordings.

### MySQL Workbench:
A database management tool used to store and manage face encodings and metadata.

### shutil
for moving files, it says shutil  package is already in python so we can just directly import in the code without installing

### Python:
The primary programming language used for the entire project.






## How to Set Up and Run the Project

-------------------------------------------------------------------

### Installations

#### Install the required dependencies through the following commands
```bash
python --version
pip install 
```

```bash
pip install opencv-python 
pip install face_recognition 
pip install twilio 
pip install mysql-connector-python 
pip install numpy
```

### Set Up XAMPP
* Install XAMPP and start the Apache server.
* Create directories screenshots and screen_recordings in C:/xampp/htdocs/.

### Set Up MySQL Database
* Create a database named face_recognition_db.
* Create a table faces with columns: id, name, and face_encoding.

### Configure Ngrok
* Download and install Ngrok.
* Run Ngrok to expose the local server
```bash
ngrok http 80
```
* Use the Ngrok URL in the values.py file.

### Configure Twilio
* Create a Twilio account and get the X and Y values (API keys).
* Update the values.py file with Twilio credentials.

### Run the Project
* Execute the initiate.py script to start the system
```bash
python initiate.py
```
* Provide the video path (or leave it empty to use the webcam).

# GITHUB LFS
https://docs.github.com/en/repositories/working-with-files/managing-large-files
For object detection, we need yolo files, we can access them online, but having offline files makes the process easier aqnd faster.. AND Normal way doesn't support GITHUB storage, as they are kinda large files, so we need to use "GITHUB LFS (LARGE FILE STORAGE)" for storing these yolo files.
* with free github acc, You can have LFS space upto 2 GB.
* upload yolo files in lfs
```bash
git lfs install
git lfs track "yolo_files/coco.names"
git lfs track "yolo_files/yolov4.cfg"
git lfs track "yolo_files/yolov4.weights"
git add yolo_files/coco.names
git add yolo_files/yolov4.cfg
git add yolo_files/yolov4.weights

#if u need to check the status of your github LFS files
git lfs ls-files
```

# Instructions:
## Setup Environment:

* Install the required Python libraries (see Requirements section).

* Set up a MySQL database for face recognition data.

* Configure Twilio for WhatsApp alerts.

## Run the Project:

* Execute the initiate.py script to start the system.

* Provide the video path (or leave it empty to use the webcam).

* The system will detect objects, recognize faces, and send alerts as configured.

## Customization:

* Modify the values.py file to update Twilio credentials and ngrok links.

* Adjust the YOLO configuration and weights paths in the code if needed.

* Customize the alert messages and emergency handling logic.




