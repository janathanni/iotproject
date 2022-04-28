import cv2
import datetime
from PIL import ImageFont, ImageDraw, Image
import numpy as np
from threading import Thread, Lock
import os
import paho.mqtt.client as mqtt

 
class USBCam:
    def __init__(self, show=False, framerate=25, width=640, height=800):
        self.size = (width, height)
        self.show = show
        self.framerate = framerate
        self.font = ImageFont.truetype('SCDream6.otf', 20) 
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID') 
        self.cap = cv2.VideoCapture(0) # 0번 카메라 picamera가 있는 곳으로 하면  에러 떠요. 무조건 USB CAM!!!
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.size[0])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.size[1])
        self.is_record = False
        self.video = None
        self.msg = []
 
class MJpegStreamCam(USBCam):
    def __init__(self, IP_address, show=True, framerate=25, width=640, height=800):
        USBCam.__init__(self, show=show, framerate=framerate, width=width, height=height)
        self.IP_address  = IP_address
    
    def nowdatetime(self, path = False):
        now = datetime.datetime.now()
        if path:
            return now.strftime('%Y-%m-%d %H_%M_%S')
        
        else:
            return now.strftime('%Y-%m-%d %H:%M:%S')

    def __iter__(self):  # 열거 가능객체 이기 위한 조건 for x in MJpegStreamCam()
        Thread(target = self.my_mqtt).start()
        
        while True:
            try:
                frame = self.make_frame()

                if self.msg:

                    if self.msg[-1] == 'r' and self.is_record == True:
                        self.video.write(frame)

                    elif self.msg[-1] == 'r' and self.is_record == False:
                        print("Recording Start.")
                        self.video = cv2.VideoWriter("web_cam " + self.nowdatetime(True) + ".avi", self.fourcc, 15, (frame.shape[1], frame.shape[0]))
                        self.is_record = True

                    elif self.msg[-1] == 'rs' and self.is_record == True:
                        self.is_record = False      
                        self.video.release()
                        self.msg = []
                        print("Recording finished.")

                        
                    elif self.msg[-1] == 'c':
                        cv2.imwrite("capture " + self.nowdatetime(True) + ".png", frame)
                        print("frame captured.")
                        self.msg.pop()


                _, jpg = cv2.imencode('.JPEG', frame)

                yield (
                    b'--myboundary\n'
                    b'Content-Type:image/jpeg\n'
                    b'Content-Length: ' + f"{len(jpg)}".encode() + b'\n'
                    b'\n' + jpg.tobytes() + b'\n'
                )

            except Exception as e:
                print(e)
                # self.cap.release()     

    def make_frame(self):
        _, frame = self.cap.read()


        frame = Image.fromarray(frame)
        draw = ImageDraw.Draw(frame)
        draw.text(xy=(10, 15),  text="IOT_3 Webcam "+self.nowdatetime(), font=self.font, fill=(255, 255, 255))
            
        frame = np.array(frame)

        return frame
    
    # def record(self):        
    #     print("Recording Started.")

    #     videoframe = self.make_frame()
                
    #     self.video.write(videoframe)


    # def record_stop(self):
    #     self.video.release()
    #     print("Recording Stop.")
    
    def connect_result(self, client, userdata, flags, rc):
        print("connect . .. " + str(rc))
        if rc == 0:
            client.subscribe("iot/cctv")
        else:
            print("연결실패...")

    def on_message(self, client, userdata, message):
        myval = message.payload.decode('utf-8')
        self.msg.append(myval)


    def my_mqtt(self):
        mqttClient = mqtt.Client()
        mqttClient.on_connect = self.connect_result 
        mqttClient.on_message = self.on_message 
        mqttClient.connect(self.IP_address, 1883, 60)
        mqttClient.loop_forever()
    