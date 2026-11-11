val=int(input("enter a number: "))
numbers = [1, 2, 3, 4, 5, 6, 7,9,3,2,1,3,4]
new=[]
for i in range(numbers[val],len(numbers)):
    new.append(numbers[i])

for i in range(0,numbers[val]):  
    new.append(numbers[i])
    
print(new)

