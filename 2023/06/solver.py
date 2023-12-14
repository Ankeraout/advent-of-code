from dataclasses import dataclass
import re
from functools import reduce

pattern_input_line = re.compile(r"^(Time|Distance):((?:\s*\d+)+)$")

@dataclass
class Race:
    time: int
    distance: int

def read_input() -> list[str]:
    data = []

    while True:
        try:
            data.append(input())
        except EOFError:
            break

    return data

def parse_input_1(data: list[str]) -> list[Race]:
    for line in data:
        match = pattern_input_line.fullmatch(line)

        if match is None:
            raise ValueError
        
        array = [int(x) for x in match.group(2).split(" ") if len(x) > 0]
        
        if match.group(1) == "Time":
            times = array
        
        else:
            distances = array

    return [Race(times[i], distances[i]) for i in range(len(times))]

def get_answer_race(data: Race) -> int:
    return sum([hold_time * (data.time - hold_time) > data.distance for hold_time in range(1, data.time)])

def get_answer_1(data: list[Race]) -> int:
    return reduce(lambda x, y: x * get_answer_race(y), data, 1)

def parse_input_2(data: list[str]) -> Race:
    for line in data:
        match = pattern_input_line.fullmatch(line)

        if match is None:
            raise ValueError
        
        data = int("".join([x for x in match.group(2) if x.isdigit()]))
        
        if match.group(1) == "Time":
            time = data
        
        else:
            distance = data

    return Race(time, distance)

def get_answer_2(data: Race) -> int:
    return get_answer_race(data)

def main():
    data_str = read_input()
    print(get_answer_1(parse_input_1(data_str)))
    print(get_answer_2(parse_input_2(data_str)))

if __name__ == "__main__":
    main()
