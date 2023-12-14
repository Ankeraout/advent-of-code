def read_input() -> tuple[str]:
    data = []

    while True:
        try:
            data.append(input())
        except EOFError:
            break

    return tuple(data)

def parse_input(data_str: tuple[str]) -> tuple[tuple[str]]:
    current_pattern = []
    patterns = []

    for row in data_str:
        if len(row) == 0:
            patterns.append(tuple(current_pattern))
            current_pattern = []
        
        else:
            current_pattern.append(row)
    
    if len(current_pattern) != 0:
        patterns.append(tuple(current_pattern))

    return tuple(patterns)

def test_horizontal(pattern: tuple[str], row: int) -> bool:
    low_row = row - 1
    high_row = row

    while low_row >= 0 and high_row < len(pattern):
        if pattern[low_row] != pattern[high_row]:
            return False
        
        low_row -= 1
        high_row += 1
        
    return True

def test_vertical(pattern: tuple[str], column: int) -> bool:
    low_column = column - 1
    high_column = column

    while low_column >= 0 and high_column < len(pattern[0]):
        if not all(row[low_column] == row[high_column] for row in pattern):
            return False
        
        low_column -= 1
        high_column += 1

    return True

def get_answer_1_single(pattern: tuple[str], ignore_result: int = None) -> int:
    for row in range(1, len(pattern)):
        if test_horizontal(pattern, row):
            result = row * 100

            if result != ignore_result:
                return result
        
    for column in range(1, len(pattern[0])):
        if test_vertical(pattern, column):
            if column != ignore_result:
                return column

def get_answer_1(data: tuple[tuple[str]]) -> int:
    return sum(get_answer_1_single(pattern) for pattern in data)

def get_answer_2_single(pattern: tuple[str]) -> int:
    initial_result: int = get_answer_1_single(pattern)

    for row_index in range(len(pattern)):
        for column_index in range(len(pattern[0])):
            new_pattern = tuple(
                f"{row[:column_index]}{'#' if row[column_index] == '.' else '.'}{row[column_index + 1:]}" if row_index_2 == row_index else row for row_index_2, row in enumerate(pattern)
            )

            result = get_answer_1_single(new_pattern, initial_result)

            if result is not None:
                return result

def get_answer_2(data: tuple[tuple[str]]) -> int:
    return sum(get_answer_2_single(pattern) for pattern in data)

def main():
    data_str = read_input()
    data = parse_input(data_str)

    print(get_answer_1(data))
    print(get_answer_2(data))

if __name__ == "__main__":
    main()
