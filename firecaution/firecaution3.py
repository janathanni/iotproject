import spidev
import time 
import pyaudio
import wave
from gpiozero import LED
import paho.mqtt.client as mqtt 

#Publish for android mqtt. server : RPi

def readadc(adcnum):
    if adcnum < 0 or adcnum > 7:
        return -1
    r = spi.xfer2([1, 8+adcnum <<4, 0])
    data = ((r[1] & 3) << 8) + r[2]
    return data

def fire_alarm():
    CHUNK = 1024
    WAVE_FILENAME = "fire_alarm.wav"

    wf = wave.open(WAVE_FILENAME, 'rb')

    p = pyaudio.PyAudio()

    stream = p.open(format = p.get_format_from_width(wf.getsampwidth()),
                channels = wf.getnchannels(),
                rate = wf.getframerate(),
                output = True)

    data = wf.readframes(CHUNK)

    while data:
        stream.write(data)
        data = wf.readframes(CHUNK)
    
    stream.stop_stream()
    stream.close()

    p.terminate()

def main():
    client = mqtt.Client()

    try:
        client.connect("localhost", 1883, 60)

        pot_value = readadc(pot_channel)
        
        if pot_value < 1020:
            print("LDR value: %d" % pot_value)
            client.publish("iot/fire", "Fire!!")

        else:
            print("LDR value: %d" % pot_value)
            client.publish("iot/fire", "No Fire!!")

        client.loop_forever()
    
    except Exception as err:
        print('에러 : %s'%err)

led = LED(19)
pot_channel = 7

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 100000

main()
