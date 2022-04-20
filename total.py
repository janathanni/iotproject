import spidev
import os
from multiprocessing import Process
import threading
import RPi.GPIO as GPIO

from cctv import main as cctv
from firecaution import firealarm
from led import led_mqtt


if __name__ == "__main__":
    p1 = threading.Thread(target = firealarm.main)
    p2 = threading.Thread(target = cctv.main)
    p3 = threading.Thread(target = led_mqtt.main)
    p1.start()
    p2.start()
    p3.start()




