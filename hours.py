import datetime
mode =  "Zegar"
display_table = {}
display_table['Digit4'] = 0
display_table['Digit3'] = 0
display_table['Digit2'] = 0
display_table['Digit1'] = 0

def flashing(target,field):
    global display_table
    a = display_table[field]
    b = target
    sign = -1 if a > b else 1
    for i in range(a,b+sign,sign):
        display_table[field] = i
        print (f"i:{i}, field:{field}")


def clock():
    global display_table,mode

    if mode == "Zegar":
        now = datetime.datetime.now()            
        flashing(now.minute%10,'Digit4') 
        flashing(int(now.minute/10),'Digit3') 
        flashing(now.hour%10,'Digit2') 
        flashing(int(now.hour/10),'Digit1') 
        display_table['Dot'] = now.second%2


clock()



