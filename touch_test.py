#!/usr/bin/python3
import RPi.GPIO as IO         # calling for header file which helps us use GPIO’s of PI
import time                             # calling for time to provide delays in program
import datetime   

TOUCH_pin_1 = 2
TOUCH_pin_2 = 17


IO.setwarnings(False)           # do not show any warnings
IO.setmode (IO.BCM)        # programming the GPIO by BCM pin numbers. (like PIN29 as‘GPIO5’)
IO.setup(TOUCH_pin_1,IO.IN)
IO.setup(TOUCH_pin_2,IO.IN)


def clock():
    while True:
        tp1 = IO.input(TOUCH_pin_1)
        tp2 = IO.input(TOUCH_pin_2)
        time.sleep(0.2)
        print(f'Left :{tp2}, Right:{tp1}')


clock()

'''
A co potem ?

1. Zegar
2. Obsluga guzików dotykowych w dolnej obudowie
3. Głośniczki Radiowe
'''
