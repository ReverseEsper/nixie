def en(a,b):
    sign = -1 if a > b else 1
    return range(a,b+sign,sign)


a = 0
b = 10

for i in rever(a,b):
    print(i)