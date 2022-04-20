import cv2
import datetime
from PIL import ImageFont, ImageDraw, Image
import numpy as np


# opencv python 코딩 기본 틀
# 카메라 영상을 받아올 객체 선언 및 설정(영상 소스, 해상도 설정)
capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

fourcc = cv2.VideoWriter_fourcc(*'XVID')  
font = ImageFont.truetype('fonts/SCDream6.otf', 20) 
is_record = False

# 무한루프
while True:
    now = datetime.datetime.now()
    nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')
    nowDatetime_path = now.strftime('%Y-%m-%d %H_%M_%S') 
    ret, frame = capture.read()    

    frame = Image.fromarray(frame)    
    draw = ImageDraw.Draw(frame)  
    draw.text(xy=(10, 15),  text="IOT_3 Webcam "+nowDatetime, font=font, fill=(255, 255, 255))
    frame = np.array(frame)

    key = cv2.waitKey(30)
    if key == ord('r') and is_record == False: 
        is_record = True           
        video = cv2.VideoWriter("web_cam " + nowDatetime_path + ".avi", fourcc, 15, (frame.shape[1], frame.shape[0]))
    elif key == ord('r') and is_record == True:
        is_record = False      
        video.release()         
    elif key == ord('c'):      
        cv2.imwrite("capture " + nowDatetime_path + ".png", frame)  
    elif key == ord('q'): 
            break
        
    if is_record == True:
        video.write(frame)
        cv2.circle(img=frame, center=(620, 15), radius=5, color=(0,0,255), thickness=-1)
    cv2.imshow("output", frame)

capture.release()                  
cv2.destroyAllWindows()          