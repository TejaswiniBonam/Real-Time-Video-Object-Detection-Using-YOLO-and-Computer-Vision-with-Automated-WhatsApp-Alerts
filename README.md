# real-time-object-detection-with-automated-whatsapp-alerts-using-dl

### Real-Time Object Detection with automated whatsApp alerts using Twilio and deep learning... This project helps someone who owns a place and needs monitoring at the least cost.

### Abstract:
The Human Detection and WhatsApp Alert System is an AI-driven security solution that utilizes YOLO (You Only Look Once) object detection to identify human presence in real-time. The system captures live video from a webcam, detects humans, and upon detection, takes a screenshot and sends an automated WhatsApp alert via Twilio API.

## Required things
* **Python** - for overall project script.
* **Computer Vision** - for webcam management, screenshots, recording, saving the media.
* **YOLO (YOU ONLY LOOK ONCE)** - for object detection.
* **Deep Learning** - for yolo.
* **Twilio** - for sending alerts through WhatsApp.
* **Pywhatkit** - for sending alerts through WhatsApp.
* **ngrok** - for giving public URLs to the local media files.
* **apache server** - for giving public URLs to the local media files.
* **shutil** - for moving files, it says shutil  package is already in python so we can just directly import in the code without installing


## Installation

xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

### Python
* **Role:** Python is the primary programming language used to write the entire script. It acts as the backbone of the project, integrating all the components and libraries.
* **Usage:** Python is used for:
      Webcam management (using OpenCV),
      Object detection (using YOLO),
      Sending WhatsApp alerts (using Twilio),
      File management (using shutil), and
      Executing additional scripts (e.g., Emergency_act.py).

```bash
python --version
```
It says Pythob 3.13.0 for me
```bash
 pip install 
```
```bash
pip install opencv-python
pip install opencv-python-headless
pip uninstall opencv-contrib-python
pip install opencv-contrib-python  # If you're running this on a server without a GUI
```

## For YOLO8
The latest version of YOLO as of October 2023 is YOLOv8, developed by Ultralytics. YOLOv8 is more efficient, accurate, and easier to use than previous versions. It comes with a Python package called ultralytics that simplifies object detection tasks.
```bash
pip install ultralytics
from ultralytics import YOLO
```


# NGROK
* install ngrok somewhere
* place ngrok.exe file somewhere , like "C:/"
* go to environment variables, got to system variables, click on Path and click edit
* click new and add C:/ngrok.exe path

# APACHE & XAMPP
* start apache server using XAMPP
* My port for apache is 8083
* now go to ngrok.exe, cmd like thing will open
```bash
ngrok http 8083
```
* run the command, you will see a link that is needed to give public url to our local files
* copy that link and paste it in your code before running
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

* X = '-A-Ca40ab86502b72a1ee2e3b5ef28195c53-'
* Y = '-c-a3b32aa91b86d88a021915f72d8b1b9-'


https://www.makeareadme.com/
