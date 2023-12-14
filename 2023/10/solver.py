from dataclasses import dataclass
from copy import copy, deepcopy
import sys

def read_input() -> list[str]:
    data = []

    while True:
        try:
            data.append(input())
        except EOFError:
            break

    return data

@dataclass
class Location:
    x: int
    y: int

    def __add__(self: "Location", other: "Location") -> "Location":
        return Location(self.x + other.x, self.y + other.y)
    
    def __sub__(self: "Location", other: "Location") -> "Location":
        return Location(self.x - other.x, self.y - other.y)
    
    def __hash__(self: "Location") -> int:
        return (self.y << 8) | self.x

@dataclass
class Cell:
    character: str
    movements: set[Location]
    upscaled: str

    def can_move_up(self: "Cell") -> bool:
        return self.can_move(Location(0, -1))

    def can_move_down(self: "Cell") -> bool:
        return self.can_move(Location(0, 1))

    def can_move_left(self: "Cell") -> bool:
        return self.can_move(Location(-1, 0))

    def can_move_right(self: "Cell") -> bool:
        return self.can_move(Location(1, 0))
    
    def can_move(self: "Cell", movement: Location) -> bool:
        return movement in self.movements
    
    def traverse(self: "Cell", previous_movement: Location) -> Location:
        if previous_movement.y == 0: # Horizontal movement
            if self.can_move_up():
                return Location(0, -1)
            elif self.can_move_down():
                return Location(0, 1)
            else:
                return previous_movement
        else: # Vertical movement
            if self.can_move_left():
                return Location(-1, 0)
            elif self.can_move_right():
                return Location(1, 0)
            else:
                return previous_movement
    
    def __repr__(self: "Cell") -> str:
        return self.character

class Grid:
    movements: dict[str, Cell] = {
        "|": Cell("|", {Location(0, -1), Location(0, 1)}, "|.|."),
        "-": Cell("-", {Location(-1, 0), Location(1, 0)}, "--.."),
        "L": Cell("L", {Location(0, -1), Location(1, 0)}, "L-.."),
        "J": Cell("J", {Location(0, -1), Location(-1, 0)}, "J..."),
        "7": Cell("7", {Location(-1, 0), Location(0, 1)}, "7.|."),
        "F": Cell("F", {Location(0, 1), Location(1, 0)}, "F-|."),
        "I": Cell("I", set(), "IIII"),
        "O": Cell("O", set(), "OOOO"),
        ".": Cell(".", set(), "....")
    }

    def __init__(self: "Grid", data_str: list[str], start_location: Location) -> None:
        # Populate cells
        self.cells = [[Grid.movements[character] if character != "S" else None for character in row] for row in data_str]

        # Determine pipe type at start location
        if self.get_cell_at(start_location + Location(0, -1)).can_move_down():
            if self.get_cell_at(start_location + Location(-1, 0)).can_move_right():
                start_pipe_type = "J"
            elif self.get_cell_at(start_location + Location(1, 0)).can_move_left():
                start_pipe_type = "L"
            else:
                start_pipe_type = "|"

        elif self.get_cell_at(start_location + Location(0, 1)).can_move_up():
            if self.get_cell_at(start_location + Location(-1, 0)).can_move_right():
                start_pipe_type = "7"
            elif self.get_cell_at(start_location + Location(1, 0)).can_move_left():
                start_pipe_type = "F"

        else:
            start_pipe_type = "-"

        self.cells[start_location.y][start_location.x] = Grid.movements[start_pipe_type]
    
    def get_cell_at(self: "Grid", location: Location) -> Cell:
        if location.x < 0 or location.y < 0 or location.x >= len(self.cells[0]) or location.y >= len(self.cells):
            return Grid.movements["."]
        
        else:
            return self.cells[location.y][location.x]
        
    def __repr__(self: "Grid"):
        return "\n".join(["".join([str(cell) for cell in row]) for row in self.cells])
    
    def get_upscaled(self: "Grid") -> "Grid":
        upscaled_grid = copy(self)
        upscaled_grid.cells = []

        for _ in range(0, len(self.cells) * 2):
            upscaled_grid.cells.append(["."] * (len(self.cells[0]) * 2))

        for row_index, row in enumerate(self.cells):
            for col_index, cell in enumerate(row):
                for pixel_index, pixel in enumerate(cell.upscaled):
                    upscaled_grid.cells[row_index * 2 + pixel_index // 2][col_index * 2 + pixel_index % 2] = Grid.movements[pixel]

        return upscaled_grid
    
    def get_cleaned(self: "Grid", start_location: Location) -> "Grid":
        cleaned_grid = deepcopy(self)
        loop_locations = set()

        location: Location = start_location

        # Choose a direction
        direction: Location = next(iter(self.get_cell_at(location).movements))

        while True:
            loop_locations.add(location)
            direction = self.get_cell_at(location).traverse(direction)
            location += direction

            if location == start_location:
                break

        # Replace all tiles that are not part of the loop with a ground tile
        for y in range(len(self.cells)):
            for x in range(len(self.cells[0])):
                location = Location(x, y)

                if location not in loop_locations:
                    cleaned_grid.cells[y][x] = Grid.movements["."]

        return cleaned_grid

    def get_centered(self: "Grid") -> "Grid":
        centered_grid = deepcopy(self)
        
        for row in centered_grid.cells:
            row.insert(0, Grid.movements["."])
            row.append(Grid.movements["."])

        centered_grid.cells.insert(0, [Grid.movements["."]] * len(centered_grid.cells[0]))
        centered_grid.cells.append([Grid.movements["."]] * len(centered_grid.cells[0]))

        return centered_grid
    
    def get_uncentered(self: "Grid") -> "Grid":
        uncentered_grid = deepcopy(self)

        del uncentered_grid.cells[0]
        del uncentered_grid.cells[-1]

        for row in uncentered_grid.cells:
            del row[0]
            del row[-1]

        return uncentered_grid
    
    def get_downscaled(self: "Grid") -> "Grid":
        downscaled_grid = copy(self)
        downscaled_grid.cells = [[self.cells[y][x] for x in range(0, len(self.cells[0]), 2)] for y in range(0, len(self.cells), 2)]
        return downscaled_grid

def parse_input(data_str: list[str]) -> tuple[tuple[int, int], Grid]:
    start_location = None

    # Determine start location
    for row_index, row in enumerate(data_str):
        for col_index, cell in enumerate(row):
            if cell == "S":
                start_location = Location(col_index, row_index)
                break
        
        if start_location is not None:
            break

    return start_location, Grid(data_str, start_location)

def get_answer_1(start_location: Location, grid: Grid) -> int:
    location: Location = start_location

    # Choose a direction
    direction: Location = next(iter(grid.get_cell_at(location).movements))

    # Compute the length of the loop
    loop_length: int = 0

    while True:
        direction = grid.get_cell_at(location).traverse(direction)
        location += direction
        loop_length += 1

        if location == start_location:
            break

    return loop_length // 2

def get_answer_2(start_location: Location, grid: Grid) -> int:
    cleaned_grid = grid.get_cleaned(start_location)
    upscaled_grid = cleaned_grid.get_upscaled()
    centered_grid = upscaled_grid.get_centered()
    flooded_grid = deepcopy(centered_grid)
    flood_directions: set[Location] = {
        Location(1, 0),
        Location(0, -1),
        Location(-1, 0),
        Location(0, 1)
    }

    # Flood the grid
    def grid_flood(grid: Grid, location: Location) -> None:
        if location.x < 0 or location.y < 0 or location.x >= len(grid.cells[0]) or location.y >= len(grid.cells) or grid.cells[location.y][location.x] != Grid.movements["."]:
            return
        
        grid.cells[location.y][location.x] = Grid.movements["O"]

        for direction in flood_directions:
            grid_flood(grid, location + direction)

    grid_flood(flooded_grid, Location(0, 0))

    # We know that unflooded areas are inside the loop
    flooded_grid.cells = [[Grid.movements["I"] if cell == Grid.movements["."] else cell for cell in row] for row in flooded_grid.cells]

    uncentered_grid = flooded_grid.get_uncentered()
    downscaled_grid = uncentered_grid.get_downscaled()

    return sum(sum(cell == Grid.movements["I"] for cell in row) for row in downscaled_grid.cells)

def main():
    data_str = read_input()
    start_location, grid = parse_input(data_str)

    sys.setrecursionlimit(100000)

    print(get_answer_1(start_location, grid))
    print(get_answer_2(start_location, grid))

if __name__ == "__main__":
    main()
