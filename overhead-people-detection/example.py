from api import Detector

import cv2
from PIL import Image
import datetime

# # Initialize detector
# detector = Detector(model_name='rapid',
#                     weights_path='./weights/pL1_MWHB1024_Mar11_4000.ckpt',
#                     use_cuda=False)

# # A simple example to run on a single image and plt.imshow() it
# detector.detect_one(img_path='./images/test5.jpeg',
#                     input_size=1024, conf_thres=0.3,
#                     visualize=True)


detector = Detector(model_name='rapid', weights_path='./weights/pL1_MWHB1024_Mar11_4000.ckpt', use_cuda=False)

cap = cv2.VideoCapture('./videos/test8 - Trim.mp4')

frame_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    frame_count += 1
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    
    width = 500
    height = int(width*frame.shape[0]/frame.shape[1])
    frame = cv2.resize(frame, (width, height))
    cv2.imshow('video', frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    if frame_count % 25 == 0:
        frame = Image.fromarray(frame)
        detections, count = detector.detect_one(pil_img=frame, input_size=1024, conf_thres=0.2, return_img=True)
        print('Time: ', current_time)
        print('Number of people: ', count)
        
        frame = cv2.cvtColor(detections, cv2.COLOR_RGB2BGR)
        frame = cv2.resize(frame, (width, height))    
        cv2.imshow('frame', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()