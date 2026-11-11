val=int(input("Enter a number: "))
list=[3,4,9,5,12]
missing=[]
for i in range(1,val):
    new=i
    if new not in list:
        missing.append(new)
print(list)
print(missing)