import time
blinker = False
for i in range(100):
    blinker = not blinker
    if blinker:
        print("Blink")
    else:
        print("Not Blink")
    time.sleep(1)
    


