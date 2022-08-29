import datetime


def is_day():
    now = datetime.datetime.now()
    hour = now.hour
    # night is between 22:00 and 7:00
    if hour < 22 and hour > 7:
        return True




if is_day():
    print("Jest dzien")
else:
    print("Jest noc")


