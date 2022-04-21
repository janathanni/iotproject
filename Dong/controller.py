import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt 
# from phone_lock import SleepManager
from time import sleep

# sudo pigpiod
# 반드시 해줄 것


lockSeconds = 0

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
Ena,In1,In2 = 26,19,13

GPIO.setup(Ena,GPIO.OUT)
GPIO.setup(In1,GPIO.OUT)
GPIO.setup(In2,GPIO.OUT)

pwm = GPIO.PWM(Ena, 50)
pwm.start(0)
pwm.ChangeDutyCycle(50)


from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import AngularServo
from phone_lock import SleepManager

def main():
    os.system("sudo pigpiod")
    try:
        # factory = PiGPIOFactory()
        # servo = AngularServo(4, min_angle=-90, max_angle=90, min_pulse_width=0.0004, max_pulse_width=0.0024,pin_factory=factory)
        print('### End ###')
        GPIO.output(In1, GPIO.LOW)
        GPIO.output(In2, GPIO.LOW)
        print('controller.py')
        mqttClient = mqtt.Client()
        mqttClient.on_connect = connect_result 
        mqttClient.on_message = on_message 
        mqttClient.connect("172.30.1.17", 1883, 60)
        mqttClient.loop_forever()

    except KeyboardInterrupt:
        GPIO.cleanup()


def openWindow():
  GPIO.output(In1, GPIO.LOW)
  GPIO.output(In2, GPIO.HIGH)
def closeWindow():
  GPIO.output(In1, GPIO.HIGH)
  GPIO.output(In2, GPIO.LOW)
def cancelWindow():
  GPIO.output(In1, GPIO.LOW)
  GPIO.output(In2, GPIO.LOW)

def connect_result(client, userdata, flags, rc):
    print("connect . .. " + str(rc))
    if rc == 0:
        client.subscribe("iot/#")
    else:
        print("연결실패ㅣ...")

def on_message(client, userdata, message):
    
    global lockSeconds
    
    myval = message.payload.decode('utf-8')
    if myval == 'OPEN':
        openWindow()
    elif(myval == 'NOTHING'):
        cancelWindow()
    elif(myval == 'CLOSE'):
        closeWindow()

    elif(myval.startswith('lockSeconds')):
        secs = myval.split(':')[1]
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


if __name__ == "__main__":
    main()
