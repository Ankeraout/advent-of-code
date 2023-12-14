import re

pattern = re.compile(
    r"^(?:toggle|turn on|turn off) (\d+),(\d+) through (\d+),(\d+)$"
)
data = []

while True:
    try:
        data.append(input())
    except EOFError:
        break

def get_instruction(instruction: str):
    if instruction.startswith("turn on"):
        return lambda _: True

    elif instruction.startswith("turn off"):
        return lambda _: False

    elif instruction.startswith("toggle"):
        return lambda state: not state
    
lights = [False] * 1000000

for instruction in data:
    match = pattern.fullmatch(instruction)

    x1 = int(match.group(1))
    y1 = int(match.group(2))
    x2 = int(match.group(3))
    y2 = int(match.group(4))
    opcode = get_instruction(instruction)

    for y in range(y1, y2 + 1):
        yoff = y * 1000

        for x in range(x1, x2 + 1):
            off = yoff + x
            lights[off] = opcode(lights[off])

print(sum(lights))

# Part 2
lights = [0] * 1000000

def get_instruction2(instruction: str):
    if instruction.startswith("turn on"):
        return lambda state: state + 1

    elif instruction.startswith("turn off"):
        return lambda state: state - 1 if state > 0 else 0

    elif instruction.startswith("toggle"):
        return lambda state: state + 2

for instruction in data:
    match = pattern.fullmatch(instruction)

    x1 = int(match.group(1))
    y1 = int(match.group(2))
    x2 = int(match.group(3))
    y2 = int(match.group(4))
    opcode = get_instruction2(instruction)

    for y in range(y1, y2 + 1):
        yoff = y * 1000

        for x in range(x1, x2 + 1):
            off = yoff + x
            lights[off] = opcode(lights[off])

print(sum(lights))
