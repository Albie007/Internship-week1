numbers = [1,2,3, 4, 5, 6, 7, 9]
target = 6

numbers.sort()

for i in range(len(numbers)):
    if numbers[i] >= target:
        continue

    for j in range(i + 1, len(numbers)):
        if numbers[i] + numbers[j] == target:
            print("Pair:", numbers[i], numbers[j])