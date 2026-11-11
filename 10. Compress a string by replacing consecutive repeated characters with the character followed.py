string = "aaabbccccdd"

count = 1
result = ""

for i in range(1, len(string)):

    if string[i] == string[i-1]:
        count += 1

    else:
        result += string[i-1] + str(count)
        count = 1

result += string[-1] + str(count)

print(result)