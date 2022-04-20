import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt 
# from phone_lock import SleepManager
import window

restSeconds = 0

def connect_result(client, userdata, flags, rc):
    print("connect . .. " + str(rc))

    if rc == 0:
        client.subscribe("iot/#")
    
    else:
        print("연결실패ㅣ...")

def on_message(client, userdata, message):
    global restSeconds
    myval = message.payload.decode('utf-8')
    if myval == 'OPEN':
        window.forward()
    elif(myval == 'NOTHING'):
        print('nothing')
    elif(myval == 'CLOSE'):
        window.reverse()

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
        restSeconds = int(myval)
        print(restSeconds)

def main():
    try:
        window.windowInit()
        mqttClient = mqtt.Client()
        mqttClient.on_connect = connect_result 
        mqttClient.on_message = on_message 
        mqttClient.connect("172.30.1.17", 1883, 60)
        mqttClient.loop_forever()

    except KeyboardInterrupt:
        GPIO.cleanup()


main()