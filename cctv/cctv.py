import cv2
import datetime
from PIL import ImageFont, ImageDraw, Image
import numpy as np
from threading import Thread
# opencv python 코딩 기본 틀
# 카메라 영상을 받아올 객체 선언 및 설정(영상 소스, 해상도 설정)
class CCTV(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.capture = cv2.VideoCapture(0)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')  
        self.font = ImageFont.truetype('../cctv/fonts/SCDream6.otf', 20) 
        self.is_record = False
    def run(self):

        # 무한루프
        while True:
            now = datetime.datetime.now()
            nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')
            nowDatetime_path = now.strftime('%Y-%m-%d %H_%M_%S') 
            ret, frame = self.capture.read()    


            frame = Image.fromarray(frame)    
            draw = ImageDraw.Draw(frame)  
            draw.text(xy=(10, 15),  text="IOT_3 Webcam "+nowDatetime, font=self.font, fill=(255, 255, 255))
            frame = np.array(frame)

            key = cv2.waitKey(30)
            if key == ord('r') and self.is_record == False: 
                self.is_record = True           
                video = cv2.VideoWriter("web_cam " + nowDatetime_path + ".avi", self.fourcc, 15, (frame.shape[1], frame.shape[0]))
            elif key == ord('r') and self.is_record == True:
                self.is_record = False      
                video.release()         
            elif key == ord('c'):      
                cv2.imwrite("capture " + nowDatetime_path + ".png", frame)  
            elif key == ord('q'): 
                    break
                
            if self.is_record == True:
                video.write(frame)
                cv2.circle(img=frame, center=(620, 15), radius=5, color=(0,0,255), thickness=-1)
            cv2.imshow("output", frame)
        self.capture.release()                  
        cv2.destroyAllWindows()  
    
