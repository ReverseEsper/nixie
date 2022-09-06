__TEST__ = False

import asyncio
import datetime
import time
import logging

if __TEST__:
    import nixie.nixie_stub
    nixie = nixie.nixie_stub.NixieStub()
    logging.basicConfig(filename='nixie.log', level=logging.DEBUG)
else:
    import nixie.nixie
    nixie = nixie.nixie.Nixie()
    logging.basicConfig(filename='/var/log/nixie.log', level=logging.DEBUG)


def is_day():
    now = datetime.datetime.now()
    hour = now.hour
    # night is between 22:00 and 7:00
    if hour < 21 and hour > 6:
        return True
    else:
        return False


mode = "Calendar"
refresh_rate = 1
display_table = {
    'Digit1': 0,
    'Digit2': 1,
    'Digit3': 2,
    'Digit4': 3,
    'Dot': 0
}

async def main():

    clock_task = asyncio.create_task(clock())
    calendar_task = asyncio.create_task(calendar())
    main_task = asyncio.create_task(swap_modes())
    seconds_task = asyncio.create_task(seconds())
    #buttons_task = asyncio.create_task(watch_buttons())
    showoff_task = asyncio.create_task(showoff())
    
    await main_task


async def refresh_display():
    global refresh_rate, display_table

    nixie.push_digit(display_table['Digit1'],display_table['Dot'])
    nixie.push_digit(display_table['Digit2'],display_table['Dot'])
    nixie.push_digit(display_table['Digit3'],display_table['Dot'])
    nixie.push_digit(display_table['Digit4'],display_table['Dot'])
    nixie.update_display()


async def clock():
    global display_table,mode
    while True:
        if mode == "Zegar":
            now = datetime.datetime.now()
            display_table['Digit4'] = now.minute%10
            display_table['Digit3'] = int(now.minute/10)
            display_table['Digit2'] = now.hour%10
            display_table['Digit1'] = int(now.hour/10)
            display_table['Dot'] = now.second%2
        await refresh_display()
        await asyncio.sleep(1)

async def calendar():
    global display_table,mode
    while True:
        if mode == "Calendar":
            now = datetime.datetime.now()
            display_table['Digit4'] = now.month%10
            display_table['Digit3'] = int(now.month/10)
            display_table['Digit2'] = now.day%10
            display_table['Digit1'] = int(now.day/10)

            display_table['Dot'] = 1
        await refresh_display()
        await asyncio.sleep(1)

async def seconds():
    global display_table,mode
    while True:
        if mode == "Seconds":
            now = datetime.datetime.now()
            display_table['Digit4'] = now.second%10
            display_table['Digit3'] = int(now.second/10)
            display_table['Digit2'] = 11
            display_table['Digit1'] = 11
            display_table['Dot'] = 0
        await refresh_display()
        await asyncio.sleep(1)

async def showoff():
    global display_table,mode
    while True:
        if mode == "Showoff":
            display_table['Digit4'] = 11
            display_table['Digit3'] = 11
            display_table['Digit2'] = 11
            display_table['Digit1'] = 11
            display_table['Dot'] = 0
            await refresh_display()
            await asyncio.sleep(0.1)
            for i in range(0,10):
                display_table['Digit4'] = i
                display_table['Digit3'] = i
                display_table['Digit2'] = i
                display_table['Digit1'] = i
                await refresh_display()
                await asyncio.sleep(0.2)
            for i in range(9,1,-1):
                display_table['Digit4'] = i
                display_table['Digit3'] = i
                display_table['Digit2'] = i
                display_table['Digit1'] = i
                await refresh_display()
                await asyncio.sleep(0.02)
            await asyncio.sleep(5)
        await asyncio.sleep(1)

    



async def swap_modes():
    global mode
    tasks = (
        { "task": "Zegar", "time": 25},
        { "task": "Calendar", "time": 5},
        { "task": "Showoff", "time": 3}
    )
    

    while True:
        if is_day():
            nixie.power_on()
            for task in tasks:
                mode = task["task"]
                await asyncio.sleep(task["time"])
        else:
            # Is Night
            nixie.power_off()
            await asyncio.sleep(60)
            
async def watch_buttons():
    global mode
    while True:
        old_mode = mode
        while nixie.button_L_state():
            #logging.info(f"Guzik Prawy:{nixie.button_R_state()} Guzik Lewy:{nixie.button_L_state()}")
            #mode = "Seconds"
            await asyncio.sleep(1)
        #mode = old_mode




nixie.power_on()
try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Ctrl-C Pressed, Finish Task")
finally:
    nixie.power_off()