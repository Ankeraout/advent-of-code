from functools import cache

def read_input() -> tuple[str]:
    data = []

    while True:
        try:
            data.append(input())
        except EOFError:
            break

    return tuple(data)

def parse_input(data_str: tuple[str]) -> tuple[tuple[str, tuple[int]]]:
    return_value = []
    
    for line in data_str:
        sequence, groups = line.split()
        return_value.append((sequence, tuple(int(x) for x in groups.split(','))))

    return tuple(return_value)

@cache
def get_possible_placements(data: str, length: int, is_final: bool) -> tuple[int]:
    group_length = length if is_final else length + 1
    
    places = []

    for place in range(len(data) - group_length + 1):
        if (
            all(character != "." for character in data[place:place + length])
            and (is_final or data[place + length] != "#")
            and (place == 0 or data[place - 1] != "#")
            and (place + length >= len(data) or data[place + length] != "#")
            and "#" not in data[:place]
        ):
            places.append(place)

    return tuple(places)

@cache
def get_answer_single_input(data: tuple[str, tuple[int]]) -> int:
    if len(data[1]) == 0:
        return 1 if "#" not in data[0] else 0

    is_final = len(data[1]) == 1
    group_length = data[1][0] if is_final else data[1][0] + 1

    return_value = 0

    for place in get_possible_placements(data[0], data[1][0], is_final):
        return_value += get_answer_single_input((data[0][place + group_length:], data[1][1:]))

    return return_value

def get_answer_1(data: tuple[str, tuple[int]]) -> int:
    return sum(get_answer_single_input(row) for row in data)

def get_answer_2(data: tuple[str, tuple[int]]) -> int:
    return sum(get_answer_single_input(("?".join([row[0]] * 5), row[1] * 5)) for row in data)

def main():
    data_str = read_input()
    data = parse_input(data_str)

    print(get_answer_1(data))
    print(get_answer_2(data))

if __name__ == "__main__":
    main()
