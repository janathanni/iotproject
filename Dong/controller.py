import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt 
# from phone_lock import SleepManager
from time import sleep
from threading import Thread
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import AngularServo
from Dong.phone_lock import SleepManager

# sudo pigpiod
# 반드시 해줄 것


class Controller(Thread):
    def __init__(self):
        super().__init__()
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.Ena = 26
        self.In1 = 19
        self.In2 = 13


        GPIO.setup(self.Ena,GPIO.OUT)
        GPIO.setup(self.In1,GPIO.OUT)
        GPIO.setup(self.In2,GPIO.OUT)

        pwm = GPIO.PWM(self.Ena, 50)
        pwm.start(0)
        pwm.ChangeDutyCycle(50)

    def connect_result(self, client, userdata, flags, rc):
        print("connect . .. " + str(rc))
        if rc == 0:
            client.subscribe("iot/#")
        else:
            print("연결실패ㅣ...")

    def on_message(self, client, userdata, message):

        myval = message.payload.decode('utf-8')
        if myval == 'OPEN':
            print('OPEN')
            GPIO.output(19, GPIO.LOW)
            GPIO.output(13, GPIO.HIGH)
        elif(myval == 'NOTHING'):
            print('NOTHING')
            GPIO.output(19, GPIO.HIGH)
            GPIO.output(13, GPIO.LOW)
        elif(myval == 'CLOSE'):
            print('CLOSE')
            GPIO.output(19, GPIO.LOW)
            GPIO.output(13, GPIO.LOW)

        elif(myval.startswith('lockSeconds')):
            secs = myval.split(':')[-1]
            print(secs)
            t = SleepManager(int(secs))
            t.start()
            t.begin_timer()
            
        elif(myval == 'myroom turn off'):
            print('myroom turn off') 
            
        elif(myval == 'myroom turn on'):
            print('myroom turn on') 

        elif(myval == 'livingroom turn off'):
            print('livingroom turn off') 
        elif(myval == 'livingroom turn on'):
            print('livingroom turn on') 

        elif(myval == 'kitchen turn off'):
            print('kitchen turn off') 
        elif(myval == 'kitchen turn on'):
            print('kitchen turn on') 
        else:
            print('다른 곳으로 빠짐')

    def run(self):
        try:
            # factory = PiGPIOFactory()
            # servo = AngularServo(4, min_angle=-90, max_angle=90, min_pulse_width=0.0004, max_pulse_width=0.0024,pin_factory=factory)
            print('### End ###')
            GPIO.output(self.In1, GPIO.LOW)
            GPIO.output(self.In2, GPIO.LOW)
            print('controller.py')
            mqttClient = mqtt.Client()
            mqttClient.on_connect = self.connect_result 
            mqttClient.on_message = self.on_message 
            mqttClient.connect("172.30.1.17", 1883, 60)
            mqttClient.loop_forever()

        except KeyboardInterrupt:
            GPIO.cleanup()







