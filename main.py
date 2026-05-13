import argparse
import sys
from pathlib import Path

from solver import CityGraph, find_eulerian_path, validate_graph, load_reference_places


def run(input_path: Path, output_path: Path, validate: bool) -> None:
    graph = CityGraph()
    graph.load_from_file(input_path)

    reference = None if not validate else load_reference_places()
    validation = validate_graph(graph, reference)
    if not validation.is_valid:
        print(f"Error: {validation.error_message}", file=sys.stderr)
        sys.exit(1)

    result = find_eulerian_path(graph, validation.start_vertex)

    display = " → ".join(result)

    print(display)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(display + "\n")

    print(f"\nPath written to {output_path}")


def interactive() -> None:
    print("=== City Name Game Solver ===\n")

    default_input = "cities.txt"
    inp = input(f"Enter path to input file [{default_input}]: ").strip()
    if not inp:
        inp = default_input
    input_path = Path(inp).resolve()

    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}", file=sys.stderr)
        input("\nPress Enter to exit...")
        return

    val = input("Validate against reference places? (Y/n): ").strip().lower()
    validate = val != "n"

    output_path = input_path.parent / "output.txt"

    try:
        run(input_path, output_path, validate)
    except SystemExit:
        pass

    input("\nPress Enter to exit...")


def cli() -> None:
    parser = argparse.ArgumentParser(
        description="Solve the Polish city name chain game using Eulerian path"
    )
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        default="cities.txt",
        help="Input file containing Polish cities (one per line)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="output.txt",
        help="Output file for the result path",
    )
    parser.add_argument(
        "--no-validate",
        action="store_true",
        help="Skip validation against reference places",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}", file=sys.stderr)
        sys.exit(2)

    run(input_path, output_path, not args.no_validate)


def main() -> None:
    if len(sys.argv) <= 1:
        interactive()
    else:
        cli()


if __name__ == "__main__":
    main()
