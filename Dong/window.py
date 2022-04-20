# ENA - GPIO26
# In1 - GPIO19
# In2 - GPIO13

import RPi.GPIO as GPIO
import time

def windowInit():
  GPIO.setmode(GPIO.BCM)
  GPIO.setwarnings(False)
  GPIO.setup(13, GPIO.OUT)
  GPIO.setup(19, GPIO.OUT)
  GPIO.setup(26, GPIO.OUT)
  pwm = GPIO.PWM(26,100)
  pwm.start(0)
  pwm.ChangeDutyCycle(50)



def forward(tf):
  GPIO.output(13,GPIO.LOW)
  GPIO.output(19,GPIO.HIGH)
  time.sleep(tf)
  print('forward')


def reverse(tf):
  GPIO.output(13,GPIO.HIGH)
  GPIO.output(19,GPIO.LOW)
  time.sleep(tf)
  print('reverse')

try:
  while(1):
    forward(4)
    reverse(2)
except KeyboardInterrupt:
  GPIO.cleanup()
