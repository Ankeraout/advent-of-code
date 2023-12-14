def read_input() -> list[str]:
    data = []

    while True:
        try:
            data.append(input())
        except EOFError:
            break

    return data

def parse_input(string: str) -> bytes:
    buffer = bytearray()
    index = 0

    while index < len(string):
        character = string[index]
        index += 1

        if character == "\\":
            character = string[index]
            index += 1

            if character == "\"":
                buffer.append(ord("\""))
            
            elif character == "\\":
                buffer.append(ord("\\"))

            elif character == "x":
                buffer.append(int(string[index:index + 2], 16))
                index += 2

        else:
            buffer.append(ord(character))

    return buffer

def escape_input(string: str) -> bytes:
    index = 0
    buffer = ""

    while index < len(string):
        character = string[index]
        index += 1

        if character == "\\":
            buffer += "\\\\"
        
        elif character == "\"":
            buffer += "\\\""

        else:
            buffer += character
    
    return buffer

def main():
    data = read_input()
    total = 0

    for string in data:
        total += len(string) - len(parse_input(string[1:-1]))

    print(total)

    total = 0

    for string in data:
        total += len(escape_input(string)) + 2 - len(string)

    print(total)

    print()

if __name__ == "__main__":
    main()
