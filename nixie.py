import asyncio
#import nixie.nixie_stub
import nixie.nixie
import datetime
import time

#nixie = nixie.nixie_stub.NixieStub()
nixie = nixie.nixie.Nixie()

def is_day():
    now = datetime.datetime.now()
    hour = now.hour
    # night is between 22:00 and 7:00
    if hour < 22 and hour > 7:
        return True


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
    task1 = asyncio.create_task(
        refresh_display()
    )
    task2 = asyncio.create_task(
        clock()
    )
    task3 = asyncio.create_task(
         calendar()
    )
    task4 = asyncio.create_task(
         swap_modes()
    )
    task4 = asyncio.create_task(
         seconds()
    )
    await task1

async def refresh_display():
    global refresh_rate, display_table
    while True:
        nixie.push_digit(display_table['Digit1'],display_table['Dot'])
        nixie.push_digit(display_table['Digit2'],display_table['Dot'])
        nixie.push_digit(display_table['Digit3'],display_table['Dot'])
        nixie.push_digit(display_table['Digit4'],display_table['Dot'])
        nixie.update_display()

        await asyncio.sleep(refresh_rate)

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
        await asyncio.sleep(0.1)

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
        await asyncio.sleep(0.1)

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
        await asyncio.sleep(0.1)



async def swap_modes():
    global mode
    tasks = (
        { "task": "Zegar", "time": 25},
        { "task": "Calendar", "time": 5}
       # { "task": "Seconds", "time": 10}
    )

    while True:
        for task in tasks:
            mode = task["task"]
            await asyncio.sleep(task["time"])
            


nixie.power_on()
try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Ctrl-C Pressed, Finish Task")
finally:
    nixie.power_off()