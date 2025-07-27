#!/usr/bin/env python3

import cv2
from datetime import datetime

def take_bird_photo():
    """Simple function to take a photo with USB webcam"""
    # Open the USB camera (usually device 0)
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open camera")
        return None
    
    # Set resolution (adjust as needed)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    # Give camera time to adjust exposure
    for i in range(5):
        ret, frame = cap.read()
    
    # Take the actual photo
    ret, frame = cap.read()
    
    if ret:
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"bird_{timestamp}.jpg"
        
        # Save photo
        cv2.imwrite(filename, frame)
        print(f"Photo saved: {filename}")
        
        # Release camera
        cap.release()
        return filename
    else:
        print("Error: Could not capture frame")
        cap.release()
        return None

if __name__ == "__main__":
    print("Taking a test photo with USB webcam...")
    take_bird_photo()
    print("Done!")