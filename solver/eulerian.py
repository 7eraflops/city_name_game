from .graph import CityGraph


def find_eulerian_path(graph: CityGraph, start_letter: str | None = None) -> list[str]:
    if start_letter is None:
        start_letter = "k"
    if start_letter not in graph.vertices:
        return []

    used_edges: set[tuple[str, str, str]] = set()
    city_path: list[str] = []

    stack: list[tuple[str, str]] = []

    first_city = None
    for dest, city in graph.edges.get(start_letter, []):
        if (start_letter, dest, city) not in used_edges:
            first_city = city
            break

    if not first_city:
        return []

    used_edges.add((start_letter, first_city[-1].lower(), first_city))
    city_path.append(first_city)
    stack.append((first_city[-1].lower(), start_letter))

    while stack:
        current_last, prev_start = stack[-1]
        available = [
            (dest, city)
            for dest, city in graph.edges.get(current_last, [])
            if (current_last, dest, city) not in used_edges
        ]

        if available:
            to_vertex, city = available[0]
            used_edges.add((current_last, to_vertex, city))
            city_path.append(city)
            stack.append((to_vertex, current_last))
        else:
            stack.pop()

    return city_path
