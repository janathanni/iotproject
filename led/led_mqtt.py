import paho.mqtt.client as mqtt 
from gpiozero import LED

#subscribe from android mqtt. server : PC

def connect_result(client, userdata, flags, rc):
    print("connect . .. " + str(rc))

    if rc == 0:
        client.subscribe("iot/led")
    
    else:
        print("연결실패ㅣ...")


def on_message(client, userdata, message):
    myval = message.payload.decode('utf-8')
    if myval == 'on':
        led.on()
    
    else:
        led.off()

led = LED(19)

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