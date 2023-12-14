def update_location(
    current_location: tuple[int, int],
    direction: str
) -> tuple[int, int]:
    if direction == '^':
        current_location = (current_location[0] - 1, current_location[1])
    if direction == 'v':
        current_location = (current_location[0] + 1, current_location[1])
    if direction == '<':
        current_location = (current_location[0], current_location[1] - 1)
    if direction == '>':
        current_location = (current_location[0], current_location[1] + 1)

    return current_location

visited_houses = set()
current_location = (0, 0)
path = input()

visited_houses.add(current_location)

for character in path:
    current_location = update_location(current_location, character)
    visited_houses.add(current_location)

print(len(visited_houses))

# Part 2
i = 0
visited_houses.clear()
current_location = [(0, 0), (0, 0)]

while i < len(path):
    for turn in range(2):
        current_location[turn] = update_location(current_location[turn], path[i])
        visited_houses.add(current_location[turn])
        i += 1

print(len(visited_houses))
