string = "swiss"
word = list(string.strip())

for char in word:
    if word.count(char) == 1:
        print("First non-repeating character:", char)
        break
else:
    print("No non-repeating character found")