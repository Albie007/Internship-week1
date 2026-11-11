list=[23,4,45,7,880,999]
max=list[0]
for num in list:
    if num>max:
        max=num

digit=list[0]
for num in list:
    if num>digit and num<max:
        digit=num
    
print(max)
print(digit)
