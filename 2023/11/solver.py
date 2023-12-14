from dataclasses import dataclass
from itertools import combinations

@dataclass
class Vector2i:
    x: int
    y: int

    def __add__(self: "Vector2i", other: "Vector2i") -> "Vector2i":
        return Vector2i(self.x + other.x, self.y + other.y)
    
    def __sub__(self: "Vector2i", other: "Vector2i") -> "Vector2i":
        return Vector2i(self.x - other.x, self.y - other.y)
    
    def __hash__(self: "Vector2i") -> int:
        return (self.x << 16) | self.y
    
    def get_euclidian_distance(self: "Vector2i") -> int:
        return abs(self.x) + abs(self.y)
    
    def get_euclidian_distance_to(self: "Vector2i", other: "Vector2i") -> int:
        return (self - other).get_euclidian_distance()

def read_input() -> list[str]:
    data = []

    while True:
        try:
            data.append(input())
        except EOFError:
            break

    return data

def parse_input(data_str: list[str]) -> list[list[str]]:
    return [[x for x in row] for row in data_str]

def get_galaxies(data: list[list[str]]) -> list[Vector2i]:
    galaxies = []
    
    for row_index, row in enumerate(data):
        for column_index, cell in enumerate(row):
            if cell == "#":
                galaxies.append(Vector2i(column_index, row_index))
    
    return galaxies

def get_answer(galaxies: list[Vector2i]) -> int:
    return sum(u.get_euclidian_distance_to(v) for u, v in combinations(galaxies, 2))

def expand_universe_2(galaxies: list[Vector2i], data: list[list[str]], expansion_rate: int) -> list[Vector2i]:
    row_offsets = []
    column_offsets = []

    current_offset = -1

    for row in data:
        if "#" not in row:
            current_offset += expansion_rate

        else:
            current_offset += 1
        
        row_offsets.append(current_offset)

    current_offset = -1
    
    for column_index in range(len(data[0])):
        if not any(row[column_index] == "#" for row in data):
            current_offset += expansion_rate

        else:
            current_offset += 1

        column_offsets.append(current_offset)

    return [Vector2i(column_offsets[galaxy.x], row_offsets[galaxy.y]) for galaxy in galaxies]

def main():
    data_str = read_input()
    data = parse_input(data_str)
    galaxies = get_galaxies(data)

    print(get_answer(expand_universe_2(galaxies, data, 2)))
    print(get_answer(expand_universe_2(galaxies, data, 1000000)))

if __name__ == "__main__":
    main()
