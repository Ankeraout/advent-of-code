from dataclasses import dataclass
import re

@dataclass
class Reindeer:
    speed: int
    stamina: int
    sleep_time: int

    def __hash__(self: "Reindeer") -> int:
        return self.speed

    def get_distance_after(self: "Reindeer", time: int) -> int:
        cycle_length = self.stamina + self.sleep_time
        distance_per_cycle = self.speed * self.stamina
        cycle_count = time // cycle_length
        cycle_phase = time % cycle_length
        cycle_sprint_time = min(cycle_phase, self.stamina)
        cycle_distance = cycle_sprint_time * self.speed

        return distance_per_cycle * cycle_count + cycle_distance

pattern_input = re.compile(r"^[A-Z][a-z]+ can fly (\d+) km\/s for (\d+) seconds, but then must rest for (\d+) seconds.$")

def read_input() -> list[str]:
    data = []

    while True:
        try:
            data.append(input())
        except EOFError:
            break

    return data

def parse_input(data: list[str]) -> list[Reindeer]:
    return_value = []

    for line in data:
        match = pattern_input.fullmatch(line)
        return_value.append(Reindeer(int(match.group(1)), int(match.group(2)), int(match.group(3))))

    return return_value

def get_answer_1(data: list[Reindeer]) -> int:
    return max(reindeer.get_distance_after(2503) for reindeer in data)

def get_answer_2(data: list[Reindeer]) -> int:
    scores = {reindeer: 0 for reindeer in data}
    
    for i in range(1, 2503):
        sorted_reindeers = sorted(data, key=lambda reindeer: reindeer.get_distance_after(i), reverse=True)
        scores[sorted_reindeers[0]] += 1
    
    sorted_reindeers = sorted(scores.items(), key=lambda item: item[1], reverse=True)

    return sorted_reindeers[0][1]

def main() -> None:
    data_str = read_input()
    data = parse_input(data_str)

    print(get_answer_1(data))
    print(get_answer_2(data))

if __name__ == "__main__":
    main()