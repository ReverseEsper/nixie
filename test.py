import RPi.GPIO as IO         # calling for header file which helps us use GPIO’s of PI
import time
#17,4,3 bangla

touchpin = (2,3,4,17)


IO.setwarnings(False)           # do not show any warnings
IO.setmode (IO.BCM)        # programming the GPIO by BCM pin numbers. (like PIN29 as‘GPIO5’)
for tp in touchpin:
    IO.setup(tp,IO.IN)


while True:
    time.sleep(0.1)
    state = []
    for tp in touchpin:
        print(IO.input(tp))
    print ("##################")

