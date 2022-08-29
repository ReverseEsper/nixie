import RPi.GPIO as IO         # calling for header file which helps us use GPIO’s of PI
import time                             # calling for time to provide delays in program
import datetime   

class Nixie:
    HV_pin = 14
    DATA_pin = 16
    CLOCK_pin = 21       
    SHOW_pin = 20
    WAIT_TIME = 0.00001
    VISIBLE = True

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

    def __init__(self):
        IO.setwarnings(False)           # do not show any warnings
        IO.setmode (IO.BCM)        # programming the GPIO by BCM pin numbers. (like PIN29 as‘GPIO5’)
        IO.setup(self.DATA_pin,IO.OUT)            # initialize GPIO Pins as an output.
        IO.setup(self.CLOCK_pin,IO.OUT)
        IO.setup(self.SHOW_pin,IO.OUT)
        IO.setup(self.HV_pin,IO.OUT)


    '''
    Timecheet stats :
    Max Clock : 4,2MHz @2V (21MHz@4.5V)
    Pulse Duration : min 120 ns
    SetUp Time : min 150ns
    Minimal time: time.sleep(1ms)
    '''

    def power_on(self):
        IO.output(self.HV_pin,1)

    def power_off(self):
        IO.output(self.HV_pin,0)

    def update_display(self):
        IO.output(self.SHOW_pin,1)            # pull the SHIFT pin high to put the 8 bit data out parallel
        time.sleep(self.WAIT_TIME)
        IO.output(self.SHOW_pin,0)            # pull down the SHIFT pin


    def send_bit(self,bit):
        IO.output(self.DATA_pin,bit)            # pull up the data pin for every bit.
        time.sleep(self.WAIT_TIME)            # wait for 100ms
        IO.output(self.CLOCK_pin,1)            # pull CLOCK pin high
        time.sleep(self.WAIT_TIME)
        IO.output(self.CLOCK_pin,0)            # pull CLOCK pin down, to send a rising edge
        IO.output(self.DATA_pin,0)            # clear the DATA pin


    def push_digit(self,character,dot=False):
        digit_map = self.digit_table[character]
        if dot:
            digit_map[5]=1
        else:
            digit_map[5]=0
            
        for bit in digit_map:
            self.send_bit(bit)

    def show_time(self,dot=False):
        now = datetime.datetime.now()
        min_last = now.minute%10
        min_first = int(now.minute/10)
        h_last = now.hour%10
        h_first = int(now.hour/10)

        self.push_digit(h_first,dot)
        self.push_digit(h_last,dot)
        self.push_digit(min_first,dot)
        self.push_digit(min_last,dot)
        self.update_display()


try:
    nixie  = Nixie()
    nixie.power_on()

    blink = False

    while True:
        if blink:
            blink = False
        else:
            blink = True
        nixie.show_time(blink)
        time.sleep(0.5)
finally:
    nixie.power_off()
