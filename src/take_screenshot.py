import cv2
import os
from datetime import datetime

def save_screenshot(frame):
    """
    Save the given frame as a screenshot with a timestamped filename.

    Args:
        frame (numpy.ndarray): The current webcam frame to save.
    """
    # Ensure the screenshots directory exists
    screenshots_dir = "C:/xampp/htdocs/screenshots"
    if not os.path.exists(screenshots_dir):
        os.makedirs(screenshots_dir)

    # Generate a timestamped filename
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = os.path.join(screenshots_dir, f"{timestamp}.jpg")

    # Save the frame as an image
    cv2.imwrite(filename, frame)
    print(f"Screenshot saved: {filename}")
    return f"{timestamp}.jpg"

# Example usage (uncomment to test independently):
# if __name__ == "__main__":
#     # Simulate a frame capture from the webcam
#     cap = cv2.VideoCapture(0)
#     ret, frame = cap.read()
#     if ret:
#         save_screenshot(frame)
#     cap.release()
