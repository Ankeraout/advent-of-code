from copy import copy
from dataclasses import dataclass
import sys

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
    
tiles: dict[str, dict[Vector2i, list[Vector2i]]] = {
    ".": {
        Vector2i(1, 0): [Vector2i(1, 0)],
        Vector2i(-1, 0): [Vector2i(-1, 0)],
        Vector2i(0, 1): [Vector2i(0, 1)],
        Vector2i(0, -1): [Vector2i(0, -1)]
    },
    "\\": {
        Vector2i(1, 0): [Vector2i(0, 1)],
        Vector2i(-1, 0): [Vector2i(0, -1)],
        Vector2i(0, 1): [Vector2i(1, 0)],
        Vector2i(0, -1): [Vector2i(-1, 0)]
    },
    "/": {
        Vector2i(1, 0): [Vector2i(0, -1)],
        Vector2i(-1, 0): [Vector2i(0, 1)],
        Vector2i(0, 1): [Vector2i(-1, 0)],
        Vector2i(0, -1): [Vector2i(1, 0)]
    },
    "|": {
        Vector2i(1, 0): [Vector2i(0, -1), Vector2i(0, 1)],
        Vector2i(-1, 0): [Vector2i(0, -1), Vector2i(0, 1)],
        Vector2i(0, 1): [Vector2i(0, 1)],
        Vector2i(0, -1): [Vector2i(0, -1)]
    },
    "-": {
        Vector2i(1, 0): [Vector2i(1, 0)],
        Vector2i(-1, 0): [Vector2i(-1, 0)],
        Vector2i(0, 1): [Vector2i(-1, 0), Vector2i(1, 0)],
        Vector2i(0, -1): [Vector2i(-1, 0), Vector2i(1, 0)]
    }
}

def read_input() -> list[str]:
    data = []

    while True:
        try:
            data.append(input())
        except EOFError:
            break

    return data

def parse_input(data_str: list[str]) -> list[str]:
    return copy(data_str)

def get_answer_1(data: list[str], initial_coordinates: Vector2i = Vector2i(0, 0), initial_direction: Vector2i = Vector2i(1, 0)) -> int:
    directions = [initial_direction]
    coordinates = [initial_coordinates]
    visited: set[tuple[Vector2i, Vector2i]] = set()

    while len(directions) > 0:
        if (coordinates[0], directions[0]) in visited or coordinates[0].x < 0 or coordinates[0].y < 0 or coordinates[0].x >= len(data[0]) or coordinates[0].y >= len(data):
            del coordinates[0]
            del directions[0]
            continue

        visited.add((coordinates[0], directions[0]))
        next_directions = tiles[data[coordinates[0].y][coordinates[0].x]][directions[0]]
        next_coordinates = list(map(lambda direction: coordinates[0] + direction, next_directions))

        del coordinates[0]
        del directions[0]

        directions += next_directions
        coordinates += next_coordinates
        
    return len(set(map(lambda x: x[0], visited)))

def get_answer_2(data: list[str]) -> int:
    to_test: list[tuple[Vector2i, Vector2i]] = []

    for x in range(len(data[0])):
        to_test.append((Vector2i(x, 0), Vector2i(0, 1)))
        to_test.append((Vector2i(x, len(data) - 1), Vector2i(0, -1)))
    
    for y in range(len(data)):
        to_test.append((Vector2i(0, y), Vector2i(1, 0)))
        to_test.append((Vector2i(len(data[0]) - 1, y), Vector2i(-1, 0)))

    return max([get_answer_1(data, situation[0], situation[1]) for situation in to_test])

def main():
    data_str = read_input()
    data = parse_input(data_str)

    print(get_answer_1(data))
    print(get_answer_2(data))

if __name__ == "__main__":
    main()
