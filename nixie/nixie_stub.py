import time                             # calling for time to provide delays in program
import datetime 
import logging  

class NixieStub:

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
        pass

    def button_L_state(self):
        return  False

    def button_R_state(self):
        return  False


    def power_on(self):
        print("Power On")

    def power_off(self):
        print("Power Off")

    def update_display(self):
        print("Wyswietlam Bufor")


    def send_bit(self,bit):
        print(bit,end='')

    def push_digit(self,character,dot=False):
        digit_map = self.digit_table[character]
        if dot:
            digit_map[5]=1
        else:
            digit_map[5]=0
            
        for bit in digit_map:
            self.send_bit(bit)
        print(" ",end="")

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



