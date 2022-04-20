import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt 

def connect_result(client, userdata, flags, rc):
    print("connect . .. " + str(rc))

    if rc == 0:
        client.subscribe("iot/light")
    
    else:
        print("연결실패ㅣ...")


def on_message(client, userdata, message):
    myval = int(message.payload.decode('utf-8'))
    
    if 0<=myval<=100:
        pwm_led.ChangeDutyCycle(myval)


led_pin = 13

GPIO.setmode(GPIO.BCM)
GPIO.setup(led_pin, GPIO.OUT)

pwm_led = GPIO.PWM(led_pin, 500)
pwm_led.start(100)


try:
    mqttClient = mqtt.Client()
    mqttClient.on_connect = connect_result 
    mqttClient.on_message = on_message 
    mqttClient.connect("172.30.1.33", 1883, 60)
    mqttClient.loop_forever()

except KeyboardInterrupt:
    pass
finally:
    pass


GPIO.cleanup()
