from gpiozero import AngularServo
from time import sleep
from datetime import datetime
from threading import Thread
import os

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

def main():
  os.system("sudo pigpiod")
  from gpiozero.pins.pigpio import PiGPIOFactory

  factory = PiGPIOFactory()

  servo = AngularServo(18, min_angle=-90, max_angle=90, min_pulse_width=0.0004, max_pulse_width=0.0024,pin_factory=factory)
  t = SleepManager("2022/04/20@13:01")      # 매개변수로 YYYY/MM/DD@HH/MM 포맷을 맞춰주세요. ex) 2022/04/17@22:00
  t.start()
  t.begin_timer(servo = servo)

servo = AngularServo(24, min_angle=-90, max_angle=90, min_pulse_width=0.0004, max_pulse_width=0.0024,pin_factory=factory)
# t = SleepManager("2022/04/17@22:38")      # 매개변수로 YYYY/MM/DD@HH/MM 포맷을 맞춰주세요. ex) 2022/04/17@22:00
# t.start()
# t.begin_timer()

  
if __name__ == "__main__":
  main()
