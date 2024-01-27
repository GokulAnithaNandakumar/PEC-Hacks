# streamlit app to display webcam video

import streamlit as st
import cv2
from PIL import Image
import numpy as np
import os
import time
from api import Detector
import datetime

import geocoder

# Set title
st.title("Webcam Live Feed")

detector = Detector(model_name='rapid', weights_path='./weights/pL1_MWHB1024_Mar11_4000.ckpt', use_cuda=False)

# open webcam
video_capture = cv2.VideoCapture(0)

# Set dimensions of webcam feed
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

# show video feed
show_video = st.checkbox("Show Video Feed")

if show_video:
    video_display = st.empty()
    frame_count = 0
    
    while True:
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        ret, frame = video_capture.read()
        frame_count += 1
        
        frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))
        video_display.image(frame, channels="BGR")
        
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        if frame_count % 25 == 0:
            frame = Image.fromarray(frame)
            detections, count = detector.detect_one(pil_img=frame, input_size=1024, conf_thres=0.2, return_img=True)
            
            frame = cv2.cvtColor(detections, cv2.COLOR_RGB2BGR)
            frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))    
            
            # display time and count
            st.write('Time:', current_time)
            st.write('Count: ', count)
            
            g = geocoder.ip('me')
            lat = g.latlng[0]
            lon = g.latlng[1]
            
            st.write("Location: ", lat, lon)
            
            # display frame
            st.image(frame, channels="BGR")
else:
    video_display = None

