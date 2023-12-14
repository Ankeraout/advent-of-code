from copy import deepcopy
from functools import cache, reduce

def read_input() -> list[str]:
    data = []

    while True:
        try:
            data.append(input())
        except EOFError:
            break

    return data

def parse_input(data_str: list[str]) -> list[list[str]]:
    return [[cell for cell in row] for row in data_str]

def roll_rocks(data: list[list[str]], direction: str = "N") -> list[str]:
    return_value = deepcopy(data)

    if direction == "N":
        for last_row_to_check in range(len(return_value) - 1, 0, -1):
            for row in range(0, last_row_to_check):
                for column in range(0, len(return_value[0])):
                    if return_value[row][column] == "." and return_value[row + 1][column] == "O":
                        return_value[row][column], return_value[row + 1][column] = return_value[row + 1][column], return_value[row][column]

    elif direction == "S":
        for last_row_to_check in range(len(return_value) - 1):
            for row in range(len(return_value) - 1, last_row_to_check, -1):
                for column in range(0, len(return_value[0])):
                    if return_value[row - 1][column] == "O" and return_value[row][column] == ".":
                        return_value[row][column], return_value[row - 1][column] = return_value[row - 1][column], return_value[row][column]

    elif direction == "W":
        for last_column_to_check in range(len(data[0]) - 1, 0, -1):
            for column in range(0, last_column_to_check):
                for row in range(0, len(return_value)):
                    if return_value[row][column] == "." and return_value[row][column + 1] == "O":
                        return_value[row][column], return_value[row][column + 1] = return_value[row][column + 1], return_value[row][column]

    elif direction == "E":
        for last_column_to_check in range(len(return_value[0]) - 1):
            for column in range(len(return_value[0]) - 1, last_column_to_check, -1):
                for row in range(0, len(return_value)):
                    if return_value[row][column - 1] == "O" and return_value[row][column] == ".":
                        return_value[row][column], return_value[row][column - 1] = return_value[row][column - 1], return_value[row][column]
    
    return return_value

def compute_weight(data: list[list[str]]) -> int:
    return sum((len(data) - row_index) * row.count("O") for row_index, row in enumerate(data))

def spin_cycle(data: list[list[str]]) -> list[list[str]]:
    return reduce(lambda grid, direction: roll_rocks(grid, direction), "NWSE", data)

def get_answer_1(data: list[list[str]]) -> int:
    return compute_weight(roll_rocks(data))

def print_data(data: list[list[str]]) -> None:
    print("\n".join("".join(row) for row in data))

def main():
    data_str = read_input()
    data = parse_input(data_str)
    current_data = data
    
    print(get_answer_1(data))

    for i in range(200):
        current_data = spin_cycle(current_data)
        print(f"{i + 1}: {compute_weight(current_data)}")

if __name__ == "__main__":
    main()
