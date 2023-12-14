import math
import re

regex_box: re.Pattern = re.compile("^([0-9]+)x([0-9]+)x([0-9]+)$")

total = 0
total_ribbon = 0

while True:
    try:
        line = input()

    except EOFError:
        break

    box_data = regex_box.match(line)
    l = int(box_data.group(1))
    w = int(box_data.group(2))
    h = int(box_data.group(3))

    lengths = sorted([int(box_data.group(i)) for i in range(1, 4)])
    sides = [
        lengths[0] * lengths[1],
        lengths[1] * lengths[2],
        lengths[2] * lengths[0]
    ]

    area = sum(sides) * 2 + min(sides)

    total += area

    ribbon_length = (lengths[0] + lengths[1]) * 2 + math.prod(lengths)

    total_ribbon += ribbon_length

print(total)
print(total_ribbon)
