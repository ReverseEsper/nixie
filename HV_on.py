import RPi.GPIO as IO         # calling for header file which helps us use GPIO’s of PI
import time                             # calling for time to provide delays in program
import datetime   

HV_pin = 14
DATA_pin = 16
CLOCK_pin = 21       
SHOW_pin = 20
WAIT_TIME = 0.00001
VISIBLE = True
TOUCH_pin = 2
TOUCH_pin2 = 17

digit_table = {
    0 : [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    1 : [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
    2 : [0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0],
    3 : [0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
    4 : [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0],
    5 : [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0],
    6 : [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0],
    7 : [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
    8 : [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0],
    9 : [0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],
    10 :[0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],
    11 :[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
}


'''
Timecheet stats :
Max Clock : 4,2MHz @2V (21MHz@4.5V)
Pulse Duration : min 120 ns
SetUp Time : min 150ns
Minimal time: time.sleep(1ms)
'''

IO.setwarnings(False)           # do not show any warnings
IO.setmode (IO.BCM)        # programming the GPIO by BCM pin numbers. (like PIN29 as‘GPIO5’)
IO.setup(DATA_pin,IO.OUT)            # initialize GPIO Pins as an output.
IO.setup(CLOCK_pin,IO.OUT)
IO.setup(SHOW_pin,IO.OUT)
IO.setup(HV_pin,IO.OUT)
IO.setup(TOUCH_pin,IO.IN)
IO.setup(TOUCH_pin2,IO.IN)


#Put current to output
IO.output(HV_pin,1)


def show():
    IO.output(SHOW_pin,1)            # pull the SHIFT pin high to put the 8 bit data out parallel
    time.sleep(WAIT_TIME)
    IO.output(SHOW_pin,0)            # pull down the SHIFT pin

def send_bit(bit):
    IO.output(DATA_pin,bit)            # pull up the data pin for every bit.
    time.sleep(WAIT_TIME)            # wait for 100ms
    IO.output(CLOCK_pin,1)            # pull CLOCK pin high
    time.sleep(WAIT_TIME)
    IO.output(CLOCK_pin,0)            # pull CLOCK pin down, to send a rising edge
    IO.output(DATA_pin,0)            # clear the DATA pin


def push_digit(character,dot=False):
    digit_map = digit_table[character]
    if dot:
        digit_map[5]=1
    else:
        digit_map[5]=0
        

    for bit in digit_map:
        send_bit(bit)

def show_time(dot=False):
    now = datetime.datetime.now()
    min_last = now.minute%10
    min_first = int(now.minute/10)
    h_last = now.hour%10
    h_first = int(now.hour/10)
    #push_digit(int(now.minute/10),dot)
    push_digit(h_first,dot)
    push_digit(h_last,dot)
    push_digit(min_first,dot)
    push_digit(min_last,dot)
    show()

def show_dot(state):
    push_digit(11)
    push_digit(11,True)
    push_digit(11,True)
    push_digit(11)
    show()

#for i in range (0,10):
#    push_digit(i)
#    show()
#    time.sleep(1)

def clock():
    global VISIBLE
    blink = False
    while True:
        if blink:
            blink = False
        else:
            blink = True
        # Sprawdzamy czas
        now = datetime.datetime.now()
        at23 = now.replace(hour=21,minute=0,second=0)
        at05 = now.replace(hour=5,minute=0,second=0)
        tp = IO.input(TOUCH_pin)
        tp2 = IO.input(TOUCH_pin2)
        if  now < at23 and  now > at05 or tp:
            if not VISIBLE:
                VISIBLE = True
                IO.output(HV_pin,1)
            if tp2:
                VISIBLE = False
                IO.output(HV_pin,0)
        else:
            if VISIBLE:
                VISIBLE = False
                IO.output(HV_pin,0)



        show_time(blink)
        time.sleep(1)
        print(VISIBLE)


clock()

'''
A co potem ?

1. Zegar
2. Obsluga guzików dotykowych w dolnej obudowie
3. Głośniczki Radiowe
'''
