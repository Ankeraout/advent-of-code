def read_input() -> str:
    return input()

def contains_straight(password: str) -> bool:
    for i in range(len(password) - 2):
        if ord(password[i + 1]) == ord(password[i]) + 1 and ord(password[i + 2]) == ord(password[i + 1]) + 1:
            return True
        
    return False

def contains_valid_characters_only(password: str) -> bool:
    return not any(character in password for character in "iol")

def locate_next_pair(password: str) -> int:
    for i in range(len(password) - 1):
        if password[i] == password[i + 1]:
            return i
        
    return None

def contains_two_pairs(password: str) -> bool:
    first_pair_index = locate_next_pair(password)

    if first_pair_index is None:
        return False
    
    second_pair_index = locate_next_pair(password[first_pair_index + 2:])

    if second_pair_index is None:
        return False
    
    second_pair_index += first_pair_index + 2
    
    return password[first_pair_index] != password[second_pair_index]

def is_password_valid(password: str) -> bool:
    return all(
        map(
            lambda function: function(password),
            [
                contains_straight,
                contains_valid_characters_only,
                contains_two_pairs
            ]
        )
    )

def get_next_password(password: str) -> str:
    ords = [ord(x) - ord('a') for x in password]

    ords[7] += 1

    index = 7

    while index >= 0 and ords[index] >= 26:
        ords[index] = 0
        ords[index - 1] += 1
        index -= 1

    return "".join([chr(x + ord('a')) for x in ords])

def get_answer(data_str: str) -> str:
    current_password = data_str

    while True:
        current_password = get_next_password(current_password)

        if is_password_valid(current_password):
            break

    return current_password

def main() -> None:
    data_str = read_input()

    answer = get_answer(data_str)

    print(answer)
    print(get_answer(answer))

if __name__ == "__main__":
    main()
