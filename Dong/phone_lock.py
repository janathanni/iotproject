from gpiozero import AngularServo
from time import sleep
from datetime import datetime
from threading import Thread
import os

# sudo pigpiod
# You start the pigpio daemon
# 위를 꼭 실행시켜줄것

from gpiozero import AngularServo
from time import sleep
from datetime import datetime
from threading import Thread

# sudo pigpiod
# You start the pigpio daemon
# 위를 꼭 실행시켜줄것

class SleepManager(Thread):
  def __init__(self, sleep_time):
    Thread.__init__(self)
    self.sleep_time = sleep_time

  def begin_timer(self):
    servo.angle = -90
    sleep(self.sleep_time)
    servo.angle = 90
    # sleep(1)


from gpiozero.pins.pigpio import PiGPIOFactory

factory = PiGPIOFactory()

servo = AngularServo(24, min_angle=-90, max_angle=90, min_pulse_width=0.0004, max_pulse_width=0.0024,pin_factory=factory)


print('### End ###')
  
if __name__ == "__main__":
  main()

