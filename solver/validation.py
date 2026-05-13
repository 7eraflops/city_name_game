from .graph import CityGraph
from dataclasses import dataclass
from pathlib import Path
import json
import sys


def _data_path(relative: str) -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS) / relative
    return Path(__file__).parent.parent / relative


@dataclass
class ValidationResult:
    is_valid: bool
    error_message: str | None = None
    start_vertex: str | None = None
    unknown_cities: list[str] | None = None


def load_reference_places(filepath: Path | None = None) -> set[str]:
    if filepath is None:
        filepath = _data_path("places_reference.json")

    if not filepath.exists():
        return set()

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Handle both array of strings and array of objects
    if isinstance(data[0], str):
        names = data
    else:
        names = [place["Name"] for place in data]

    # Normalize to lowercase and title case
    result = set()
    for name in names:
        name = name.strip()
        if name:
            parts = name.split("-")
            normalized = "-".join(
                p[0].upper() + p[1:].lower() if p else p for p in parts
            )
            result.add(normalized)
            result.add(normalized.lower())

    return result


def validate_graph(
    graph: CityGraph, reference_places: set[str] | None = None
) -> ValidationResult:
    if not graph.cities:
        return ValidationResult(False, "No cities in input file")

    if reference_places:
        unknown = []
        for city in graph.cities:
            city_normalized = city.strip()
            city_lower = city.lower().strip()
            if (
                city_normalized not in reference_places
                and city_lower not in reference_places
            ):
                unknown.append(city)

        if unknown:
            return ValidationResult(
                False,
                f"Unknown places (not in reference): {', '.join(unknown[:5])}{'...' if len(unknown) > 5 else ''}",
                unknown_cities=unknown,
            )

    has_krakow = False
    for city in graph.cities:
        if city.lower().strip() == "kraków":
            has_krakow = True
            break

    if not has_krakow:
        return ValidationResult(False, "Kraków not found in input file")

    out_by_vertex = {}
    in_by_vertex = {}

    for city in graph.cities:
        first = city[0].lower()
        last = city[-1].lower()
        out_by_vertex[first] = out_by_vertex.get(first, 0) + 1
        in_by_vertex[last] = in_by_vertex.get(last, 0) + 1

    all_vertices = set(out_by_vertex.keys()) | set(in_by_vertex.keys())

    start_candidates = []
    end_candidates = []

    for v in all_vertices:
        out_deg = out_by_vertex.get(v, 0)
        in_deg = in_by_vertex.get(v, 0)
        diff = out_deg - in_deg
        if diff == 1:
            start_candidates.append(v)
        elif diff == -1:
            end_candidates.append(v)
        elif diff != 0:
            return ValidationResult(
                False,
                f"No valid path: vertex '{v}' has degree imbalance (out={out_deg}, in={in_deg})",
            )

    if len(start_candidates) == 0 and len(end_candidates) == 0:
        start = "k"
    elif len(start_candidates) == 1 and len(end_candidates) == 1:
        if start_candidates[0] == "k":
            start = "k"
        else:
            return ValidationResult(
                False,
                f"Path would start at '{start_candidates[0]}' but game requires starting with Kraków (k)",
            )
    else:
        return ValidationResult(
            False,
            f"No valid Eulerian path: {len(start_candidates)} start vertices, {len(end_candidates)} end vertices",
        )

    if start not in out_by_vertex or out_by_vertex[start] == 0:
        return ValidationResult(False, f"Start vertex '{start}' has no outgoing edges")

    return ValidationResult(True, start_vertex=start)
