text = input()
value = 0
basementIndex = None

for index, character in enumerate(text):
    if character == '(':
        value += 1
    else:
        value -= 1

    if value == -1:
        if basementIndex is None:
            basementIndex = index + 1

print(value)
print(basementIndex)
