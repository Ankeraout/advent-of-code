import re

from itertools import permutations

def read_input() -> list[str]:
    data = []

    while True:
        try:
            data.append(input())
        except EOFError:
            break

    return data

pattern_graph = re.compile(r"^(.+) to (.*) = (\d+)$")

def get_route_length(graph: dict[str, dict[str, int]], route: list[str]) -> int:
    if len(route) == 1:
        return 0
    
    else:
        if route[0] in graph and route[1] in graph[route[0]]:
            subroute_length = get_route_length(graph, route[1:])

            if subroute_length is not None:
                return graph[route[0]][route[1]] + subroute_length
            
            else:
                return None
        
        else:
            return None

def get_shortest_distance(graph: dict[str, dict[str, int]]):
    locations = get_locations(graph)
    minimum_route_length = None
    minimum_route = None

    for route in permutations(locations):
        route_length = get_route_length(graph, route)

        if route_length is None:
            continue

        if minimum_route_length is None or route_length < minimum_route_length:
            minimum_route_length = route_length
            minimum_route = route

    return minimum_route, minimum_route_length

def get_longest_distance(graph: dict[str, dict[str, int]]):
    locations = get_locations(graph)
    maximum_route_length = None
    maximum_route = None

    for route in permutations(locations):
        route_length = get_route_length(graph, route)

        if route_length is None:
            continue

        if maximum_route_length is None or route_length > maximum_route_length:
            maximum_route_length = route_length
            maximum_route = route

    return maximum_route, maximum_route_length

def build_graph(data: list[str]) -> dict[str, dict[str, int]]:
    graph: dict[str, dict[str, int]] = dict()

    for line in data:
        match = pattern_graph.fullmatch(line)

        source = match.group(1)
        destination = match.group(2)
        distance = int(match.group(3))

        if source not in graph:
            graph[source] = dict()
        
        if destination not in graph:
            graph[destination] = dict()

        graph[source][destination] = distance
        graph[destination][source] = distance
    
    return graph

def get_locations(graph: dict[str, dict[str, int]]):
    locations = set()
    
    for source in graph:
        locations.add(source)

        for destination in graph[source]:
            locations.add(destination)
    
    return locations

def main():
    graph = build_graph(read_input())
    print(get_shortest_distance(graph))
    print(get_longest_distance(graph))

if __name__ == "__main__":
    main()
