import re

def read_input() -> list[str]:
    data = []

    while True:
        try:
            data.append(input())
        except EOFError:
            break

    return data

pattern_single_digit = re.compile(r"^[^\d]*(\d)[^\d]*$")
pattern_multiple_digits = re.compile(r"^[^\d]*(\d).*(\d)[^\d]*$")
pattern_single_digit_2 = re.compile(r"^.*(zero|one|two|three|four|five|six|seven|eight|nine|\d).*$")
pattern_multiple_digits_2 = re.compile(r"^.*?(zero|one|two|three|four|five|six|seven|eight|nine|\d).*(zero|one|two|three|four|five|six|seven|eight|nine|\d).*$")
digits = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

def main():
    data = read_input()

    sum = 0

    for string in data:
        match = pattern_multiple_digits.fullmatch(string)

        if match is not None:
            sum += int(match.group(1) + match.group(2))

        else:
            match = pattern_single_digit.fullmatch(string)
            
            if match is not None:
                sum += int(match.group(1) + match.group(1))

    print(sum)

    # Part 2
    sum = 0

    for string in data:
        match = pattern_multiple_digits_2.fullmatch(string)

        if match is not None:
            try:
                first_digit = int(match.group(1))
            except ValueError:
                first_digit = digits.index(match.group(1))

            try:
                last_digit = int(match.group(2))
            except ValueError:
                last_digit = digits.index(match.group(2))

        else:
            match = pattern_single_digit_2.fullmatch(string)

            if match is not None:
                try:
                    first_digit = int(match.group(1))
                except ValueError:
                    first_digit = digits.index(match.group(1))

                last_digit = first_digit
        
        sum += first_digit * 10 + last_digit

    print(sum)

if __name__ == "__main__":
    main()
