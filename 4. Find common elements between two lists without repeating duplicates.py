List1 = [1, 2, 3, 4, 5, 2, 3]
List2 = [3, 4, 5, 6, 7, 3, 4]

new_list=[]
for num in List1:
    if num in List2 and num not in new_list:
        new_list.append(num)
print(new_list)