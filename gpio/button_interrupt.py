import time

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.IN)


def handler():
    count = 0

    def inner(channel):
        nonlocal count
        count += 1
        print(count)

    return inner


GPIO.add_event_detect(24, GPIO.RISING, callback=handler(), bouncetile=500)


while True:
    time.sleep(1)
