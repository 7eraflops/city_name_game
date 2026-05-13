from collections import defaultdict
from pathlib import Path


class CityGraph:
    def __init__(self):
        self.edges = defaultdict(list)
        self.vertices = set()
        self.cities = []

    def add_city(self, city: str):
        city = city.strip()
        if not city:
            return
        first_letter = city[0].lower()
        last_letter = city[-1].lower()
        self.edges[first_letter].append((last_letter, city))
        self.vertices.add(first_letter)
        self.vertices.add(last_letter)
        self.cities.append(city)

    def load_from_file(self, filepath: Path):
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"City file not found: {filepath}")
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                self.add_city(line)

    def get_out_degree(self, vertex: str) -> int:
        return len(self.edges.get(vertex, []))

    def get_in_degree(self, vertex: str) -> int:
        count = 0
        for sources in self.edges.values():
            for dest, _ in sources:
                if dest == vertex:
                    count += 1
        return count

    def getDegree(self, vertex: str) -> tuple[int, int]:
        return (self.get_out_degree(vertex), self.get_in_degree(vertex))

    def remove_edge(self, from_vertex: str, to_vertex: str, city: str):
        if from_vertex in self.edges:
            self.edges[from_vertex] = [
                e for e in self.edges[from_vertex] if e[1] != city
            ]

    def get_edge(self, from_vertex: str, to_vertex: str, city: str):
        for edge in self.edges.get(from_vertex, []):
            if edge[1] == city:
                return edge
        return None

    def get_available_edges(self, vertex: str) -> list[tuple[str, str]]:
        return list(self.edges.get(vertex, []))
