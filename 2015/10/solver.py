data = input()

def iterate(string: str) -> str:
    output_string = ""
    index = 0
    
    while index < len(string):
        current_digit = string[index]
        index += 1
        length = 1
        
        while index < len(string) and string[index] == current_digit:
            length += 1
            index += 1

        output_string += f"{length}{current_digit}"

    return output_string

current_data = data

for i in range(40):
    current_data = iterate(current_data)

print(len(current_data))

# Part 2
for i in range(10):
    current_data = iterate(current_data)

print(len(current_data))
