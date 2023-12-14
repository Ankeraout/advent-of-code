def read_input() -> list[str]:
    data = []

    while True:
        try:
            data.append(input())
        except EOFError:
            break

    return data

def parse_input(data_str: list[str]) -> list[list[int]]:
    return [[int(x) for x in line.split()] for line in data_str]

def compute_differences(history: list[int]) -> list[list[int]]:
    # Compute differences until there are only 0's remaining
    differences = [history.copy()]

    while not all([x == 0 for x in differences[-1]]):
        differences.append([differences[-1][i] - differences[-1][i - 1] for i in range(1, len(differences[-1]))])

    return differences

def get_answer_1_history(history: list[int]) -> int:
    differences = compute_differences(history)
    
    # Add a zero
    differences[-1].append(0)

    # Compute new extrapolated values
    index = len(differences) - 2

    while index >= 0:
        differences[index].append(differences[index][-1] + differences[index + 1][-1])
        index -= 1

    return differences[0][-1]

def get_answer_1(data: list[list[int]]) -> int:
    return sum([get_answer_1_history(history) for history in data])

def get_answer_2_history(history: list[int]) -> int:
    differences = compute_differences(history)

    # Add a zero
    differences[-1].insert(0, 0)

    # Compute new extrapolated values
    index = len(differences) - 2

    while index >= 0:
        differences[index].insert(0, differences[index][0] - differences[index + 1][0])
        index -= 1

    return differences[0][0]

def get_answer_2(data: list[list[int]]) -> int:
    return sum([get_answer_2_history(history) for history in data])

def main():
    data_str = read_input()
    data = parse_input(data_str)

    print(get_answer_1(data))
    print(get_answer_2(data))

if __name__ == "__main__":
    main()
