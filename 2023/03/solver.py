class Entity:
    def __init__(self: "Entity", x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def is_colliding_with(self: "Entity", other: "Entity") -> bool:
        return (
            (self.x < other.x + other.width)
            & (self.x + self.width > other.x)
            & (self.y < other.y + other.height)
            & (self.y + self.height > other.y)
        )
    
    def __repr__(self: "Entity") -> str:
        return f"({self.x}, {self.y}, {self.width}, {self.height})"

class Symbol(Entity):
    def __init__(self: "Symbol", x: int, y: int, type: str):
        Entity.__init__(self, x - 1, y - 1, 3, 3)
        self.type = type

    def __repr__(self: "Entity") -> str:
        return f"Symbol{Entity.__repr__(self)}"

class Number(Entity):
    def __init__(self: "Number", x: int, y: int, number: int):
        Entity.__init__(self, x, y, len(str(number)), 1)
        self.number = number
    
    def __repr__(self: "Entity") -> str:
        return Entity.__repr__(self).replace("(", f"Number({self.number}, ")

def read_input() -> list[str]:
    data = []

    while True:
        try:
            data.append(input())
        except EOFError:
            break

    return data

def is_symbol(character: str) -> bool:
    return (not character.isdigit()) & (character != ".")

def parse_grid(data: list[str]) -> tuple[list[Symbol], list[Number]]:
    def add_current_number(numbers: list[Number], number: dict[str, int]):
        if number is not None:
            numbers.append(Number(number["x"], number["y"], number["number"]))

    numbers: list[Number] = list()
    symbols: list[Symbol] = list()
    number: dict[str, int] = None

    for y, row in enumerate(data):
        for x, cell in enumerate(row):
            if is_symbol(cell):
                add_current_number(numbers, number)
                number = None
                symbols.append(Symbol(x, y, cell))
            
            elif cell.isdigit():
                if number is None:
                    number = {
                        "x": x,
                        "y": y,
                        "number": int(cell)
                    }

                else:
                    number["number"] = number["number"] * 10 + int(cell)

            else:
                add_current_number(numbers, number)
                number = None
    
    add_current_number(numbers, number)

    return symbols, numbers

def main():
    data = read_input()
    symbols, numbers = parse_grid(data)
    part_numbers: list[Number] = list()

    for number in numbers:
        if any(number.is_colliding_with(symbol) for symbol in symbols):
            part_numbers.append(number)

    print(sum(part_number.number for part_number in part_numbers))

    # Part 2
    answer = 0

    for symbol in symbols:
        if symbol.type == '*':
            adjacent_parts = [part for part in numbers if part.is_colliding_with(symbol)]

            if len(adjacent_parts) == 2:
                gear_ratio = adjacent_parts[0].number * adjacent_parts[1].number
                answer += gear_ratio

    print(answer)

if __name__ == "__main__":
    main()
