import time

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

count = 0
while True:
    value = GPIO.input(24)
    if value is True:
        count += 1
        print(count)
    time.sleep(0.1)
