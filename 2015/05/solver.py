def check_vowels(string: str) -> bool:
    return sum(x in "aeiou" for x in string) >= 3

def check_double(string: str) -> bool:
    previous_letter = string[0]

    for letter in string[1:]:
        if letter == previous_letter:
            return True
        
        else:
            previous_letter = letter

    return False

def check_bad_strings(string: str) -> bool:
    return all(x not in string for x in ("ab", "cd", "pq", "xy"))

def is_string_nice(string: str) -> bool:
    return (
        check_vowels(string)
        and check_double(string)
        and check_bad_strings(string)
    )

data = []

while True:
    try:
        data.append(input())
    except EOFError:
        break

print(sum(is_string_nice(x) for x in data))

# Part 2

def check_pair(string: str) -> bool:
    letter_pairs = [string[x] + string[x + 1] for x in range(len(string) - 1)]
    
    for index, letter_pair in enumerate(letter_pairs[:-2]):
        if letter_pair in letter_pairs[index + 2:]:
            return True
        
    return False

def check_letter_repeat(string: str) -> bool:
    for index, letter in enumerate(string[:-2]):
        if string[index + 2] == letter:
            return True
        
    return False

def is_string_nice2(string: str) -> bool:
    return check_pair(string) and check_letter_repeat(string)

print(sum(is_string_nice2(x) for x in data))
