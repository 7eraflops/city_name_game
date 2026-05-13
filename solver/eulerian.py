from collections import defaultdict
from .graph import CityGraph


def _hierholzer(
    edges: dict[str, list[tuple[str, str]]], start: str
) -> list[str]:
    remaining = {v: list(e) for v, e in edges.items() if e}
    stack: list[tuple[str, str | None]] = [(start, None)]
    result: list[str] = []

    while stack:
        v, incoming = stack[-1]
        if v in remaining and remaining[v]:
            dest, city = remaining[v].pop(0)
            stack.append((dest, city))
        else:
            stack.pop()
            if incoming is not None:
                result.append(incoming)

    result.reverse()
    return result


def find_eulerian_path(graph: CityGraph, start_letter: str | None = None) -> list[str]:
    if start_letter is None:
        start_letter = "k"
    if start_letter not in graph.vertices:
        return []

    edges: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for v in graph.vertices:
        edges[v] = list(graph.edges.get(v, []))

    if start_letter == "k":
        krakow = None
        others: list[tuple[str, str]] = []
        for e in edges["k"]:
            if e[1].lower().strip() == "kraków":
                krakow = e
            else:
                others.append(e)
        if krakow:
            edges["k"] = others
            rest = _hierholzer(edges, krakow[0])
            return [krakow[1]] + rest

    return _hierholzer(edges, start_letter)
