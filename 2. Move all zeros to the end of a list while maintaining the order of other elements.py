list=[0,4,0,6,0,2,0,2]
count=0
new_list=[]
for num in list:
    if num==0:
        count+=1
    else:
        new_list.append(num)
for i in range(count):
    new_list.append(0)
    
print(list)
print(new_list)
