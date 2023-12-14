from dataclasses import dataclass
from functools import reduce
import re
import sys

@dataclass
class ConversionRange:
    destination_start: int
    source_start: int
    length: int

class Converter:
    def __init__(self: "Converter", source_map: str, destination_map: str, ranges: list[ConversionRange]):
        self.source_map = source_map
        self.destination_map = destination_map
        self.ranges = ranges
    
    def convert(self: "Converter", value: int) -> int:
        for range in self.ranges:
            if range.source_start <= value and value < range.source_start + range.length:
                return range.destination_start + value - range.source_start

        return value
    
    def __repr__(self: "Converter") -> str:
        return f"Converter({self.source_map}, {self.destination_map}, {self.ranges})"

def read_input() -> list[str]:
    data = []

    while True:
        try:
            data.append(input())
        except EOFError:
            break

    return data

def parse_seeds(data: str) -> list[int]:
    return [int(x) for x in data.split(": ")[1].split(" ")]

pattern_map_header = re.compile(r"^([a-z]+)-to-([a-z]+) map:$")

def split_maps(data: list[str]) -> list[list[str]]:
    map = []
    maps = []
    state = "initial"

    for row in data:
        if state == "initial":
            match = pattern_map_header.fullmatch(row)

            if match is not None:
                state = "reading_map"
                map = [row]
            
        elif state == "reading_map":
            if len(row) == 0:
                state = "initial"
                maps.append(map)
            
            else:
                map.append(row)
    
    if state == "reading_map":
        maps.append(map)

    return maps

def parse_range(data: str) -> ConversionRange:
    splitted_data = [int(x) for x in data.split(" ")]

    return ConversionRange(
        splitted_data[0],
        splitted_data[1],
        splitted_data[2]
    )

def parse_map(data: list[str]) -> Converter:
    match = pattern_map_header.fullmatch(data[0])

    if match is None:
        raise ValueError()

    source_map = match.group(1)
    destination_map = match.group(2)

    return Converter(source_map, destination_map, [parse_range(x) for x in data[1:]])

def parse_maps(data: list[str]) -> list[Converter]:
    return [parse_map(x) for x in split_maps(data)]

def parse_input(data: list[str]) -> tuple[list[int], list[Converter]]:
    return parse_seeds(data[0]), parse_maps(data[2:])

def main():
    seeds, maps = parse_input(read_input())
    minimal_value = None

    for seed in seeds:
        value = seed

        for converter in maps:
            value = converter.convert(value)

        if minimal_value is None or value < minimal_value:
            minimal_value = value

    print(minimal_value)

    minimal_value = None

    for i in range(0, len(seeds), 2):
        range_start = seeds[i]
        range_length = seeds[i + 1]

        for j in range(range_start, range_start + range_length):
            value = j

            if value % 10000000 == 0:
                print(f"{((j - range_start) * 100) / range_length:.2f}%")
                sys.stdout.flush()

            for converter in maps:
                value = converter.convert(value)

            if minimal_value is None or value < minimal_value:
                minimal_value = value

        print(minimal_value)

if __name__ == "__main__":
    main()
