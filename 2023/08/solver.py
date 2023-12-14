import re
import math

pattern_node = re.compile(r"^([A-Z0-9]{3}) = \(([A-Z0-9]{3}), ([A-Z0-9]{3})\)$")

def read_input() -> list[str]:
    data = []

    while True:
        try:
            data.append(input())
        except EOFError:
            break

    return data

def parse_input(data_str: list[str]) -> tuple[str, dict[str, tuple[str, str]]]:
    return_value = dict()

    for node in data_str[2:]:
        match = pattern_node.fullmatch(node)
        return_value[match.group(1)] = (match.group(2), match.group(3))
    
    return data_str[0], return_value

def get_answer_1(data: tuple[str, dict[str, tuple[str, str]]]) -> int:
    current_node: str = "AAA"
    count = 0

    while current_node != "ZZZ":
        direction = data[0][count % len(data[0])]
        count += 1

        if direction == 'L':
            current_node = data[1][current_node][0]
        
        else:
            current_node = data[1][current_node][1]

    return count

def get_loop_length(data: tuple[str, dict[str, tuple[str, str]]], current_node: str) -> int:
    count = 0

    while not current_node.endswith("Z"):
        direction = data[0][count % len(data[0])]
        count += 1

        if direction == 'L':
            current_node = data[1][current_node][0]
        
        else:
            current_node = data[1][current_node][1]

    return count

def get_answer_2(data: tuple[str, dict[str, tuple[str, str]]]) -> int:
    current_nodes: list[str] = tuple(x for x in data[1] if x.endswith("A"))
    loop_lengths: list[int] = [get_loop_length(data, current_node) for current_node in current_nodes]

    return math.lcm(*loop_lengths)

def main():
    data_str = read_input()
    data = parse_input(data_str)

    print(get_answer_1(data))
    print(get_answer_2(data))

if __name__ == "__main__":
    main()
