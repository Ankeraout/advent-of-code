from functools import reduce
import re

def read_input() -> list[str]:
    data = []

    while True:
        try:
            data.append(input())
        except EOFError:
            break

    return data

pattern_game = re.compile(r"^Game (\d+): (.*)$")
pattern_cube = re.compile(r"^(\d+) (red|green|blue)$")

def parse_cube(cube: str) -> tuple[str, int]:
    match = pattern_cube.fullmatch(cube)
    return match.group(2), int(match.group(1))

def parse_set(set: str) -> dict[str, int]:
    cubes = [parse_cube(cube) for cube in set.split(", ")]
    return {cube[0]: cube[1] for cube in cubes}

def parse_sets(sets: str) -> list[dict[str, int]]:
    return [parse_set(set) for set in sets.split("; ")]

def parse_game(game: str) -> tuple[int, list[dict[str, int]]]:
    match_game = pattern_game.fullmatch(game)
    return int(match_game.group(1)), parse_sets(match_game.group(2))

def is_set_possible(set: dict[str, int], reference: dict[str, int]) -> bool:
    return all(set[k] <= reference[k] for k in set)

def is_game_possible(
    game_data: list[dict[str, int]],
    reference: dict[str, int]
) -> bool:
    return all(is_set_possible(set, reference) for set in game_data)

def get_minimums(game_data: list[dict[str, int]]):
    minimums = {
        "red": 0,
        "green": 0,
        "blue": 0
    }

    for set in game_data:
        for color, quantity in set.items():
            minimums[color] = max(minimums[color], quantity)
    
    return minimums

def main():
    data = read_input()

    reference = {
        "red": 12,
        "green": 13,
        "blue": 14
    }

    parsed_games = [parse_game(game_string) for game_string in data]
    print(sum([game_id if is_game_possible(game_data, reference) else 0 for game_id, game_data in parsed_games]))
    print(sum([reduce(lambda x, y: x * y, get_minimums(game_data).values()) for _, game_data in parsed_games]))

if __name__ == "__main__":
    main()
