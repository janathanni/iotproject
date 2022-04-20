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
    a, b = sleep_time.split('@')
    Y,M,D = a.split('/')
    H,m = b.split(':')
    self.sleep_time = datetime(int(Y),int(M),int(D),int(H),int(m),0)

  def begin_timer(self):
    then = self.sleep_time
    now = datetime.now()
    duration = then - now
    duration_in_s = duration.total_seconds()
    print(duration_in_s)
    servo.angle = -90
    sleep(duration_in_s)
    servo.angle = 90
    sleep(1)


from gpiozero.pins.pigpio import PiGPIOFactory

factory = PiGPIOFactory()

servo = AngularServo(19, min_angle=-90, max_angle=90, min_pulse_width=0.0004, max_pulse_width=0.0024,pin_factory=factory)
t = SleepManager("2022/04/17@22:38")      # 매개변수로 YYYY/MM/DD@HH/MM 포맷을 맞춰주세요. ex) 2022/04/17@22:00
t.start()
t.begin_timer()

  
print('### End ###')

