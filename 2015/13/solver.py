from copy import deepcopy
import re
from itertools import permutations

pattern_input = re.compile(r"^([A-Z][a-z]+) would (gain|lose) (\d+) happiness units by sitting next to ([A-Z][a-z]+).$")

def read_input() -> list[str]:
    data = []

    while True:
        try:
            data.append(input())
        except EOFError:
            break

    return data

def parse_input(data: list[str]) -> dict[str, dict[str, int]]:
    return_value = {}

    for line in data:
        match = pattern_input.fullmatch(line)

        person = match.group(1)
        gain = int(match.group(3))
        neighbor = match.group(4)

        if match.group(2) == "lose":
            gain = -gain
        
        return_value.setdefault(person, {})
        return_value[person][neighbor] = gain

    return return_value

def get_permutation_score(data: dict[str, dict[str, int]], permutation: list[str]) -> int:
    score = 0

    for index in range(-1, len(permutation) - 1):
        person1 = permutation[index]
        person2 = permutation[index + 1]
        score += data[person1][person2]
        score += data[person2][person1]

    return score

def get_answer_1(data: dict[str, dict[str, int]]) -> int:
    return max(get_permutation_score(data, permutation) for permutation in permutations(set(data.keys())))

def get_answer_2(data: dict[str, dict[str, int]]) -> int:
    new_data = deepcopy(data)
    attendees = set(new_data.keys())

    new_data["yourself"] = {}

    for attendee in attendees:
        new_data[attendee]["yourself"] = 0
        new_data["yourself"][attendee] = 0
    
    return get_answer_1(new_data)

def main() -> None:
    data_str = read_input()
    data = parse_input(data_str)

    print(get_answer_1(data))
    print(get_answer_2(data))

if __name__ == "__main__":
    main()
