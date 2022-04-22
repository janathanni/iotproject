import spidev
import os
from multiprocessing import Process
import threading
import RPi.GPIO as GPIO

# from cctv import ex_scene_adjustment
from firecaution import firealarm
# from led import led_mqtt
# from smartspeakers import smartspeakers
from smartspeakers import smartspeakers
from Dong import controller


if __name__ == "__main__":
    # p1 = threading.Thread(target = firealarm.main)
    # p2 = threading.Thread(target = ex_scene_adjustment.main)
    # p3 = threading.Thread(target = led_mqtt.main)
    p4 = threading.Thread(target = smartspeakers.main)
    p5 = threading.Thread(target = controller.main)

    p4.start()
    p5.start()
    # p2.start()
    # p3.start()
    # p4.start()