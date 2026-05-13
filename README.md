# City Name Game Solver

A small Python tool that solves the Polish "city name chain" game by constructing a directed graph of city names and finding an Eulerian path. The solver starts from the letter `k` (the game requires starting with Kraków) and tries to produce a chain where each city's first letter matches the previous city's last letter.

## Requirements

- Python 3.13+
- No external dependencies (see `pyproject.toml`).

## Quick start

1. Put one city per line in a plain text file (default: `cities.txt`).
2. Run the solver:

```bash
python main.py -i cities.txt -o output.txt
python main.py --no-validate -i mycities.txt -o path.txt
```

- `-i, --input`  : input file with one city per line (default `cities.txt`).
- `-o, --output` : output file where the resulting path is written (default `output.txt`).
- `--no-validate`: skip validation against `places_reference.json`.

## Windows executable (no Python required)

A standalone `.exe` can be built with [PyInstaller](https://pyinstaller.org/).
The executable bundles Python itself and `places_reference.json`, so no
interpreter or extra files are needed.

### Build locally

```cmd
pip install pyinstaller
pyinstaller city_name_game.spec
```

The `.exe` is created at `dist/city_name_game.exe`.

### Build via GitHub Actions

Push a tag to trigger an automated build:

```bash
git tag v1.0.0
git push origin v1.0.0
```

The workflow uploads `city_name_game.exe` as a build artifact, which you can
download from the repository's Actions page.

### Usage

When you run `city_name_game.exe` without arguments it enters **interactive mode**:

```
=== City Name Game Solver ===

Enter path to input file [cities.txt]:
Validate against reference places? (Y/n):
```

If you provide CLI arguments it works the same as the Python version:

```cmd
city_name_game.exe -i cities.txt -o output.txt
```

## Example

Sample input (`cities.txt`):
```city_name_game/cities.txt#L1-10
Kraków
Wąchock
Końskie
Ełk
Krosno
Opoczno
```

Sample output (`output.txt`):
```city_name_game/output.txt#L1-1
Kraków → Wąchock → Końskie → Ełk → Krosno → Opoczno
```

## How it works (high level)

- `solver/graph.py` defines `CityGraph`: a directed multigraph where vertices are single letters (first/last letters of city names) and edges are city names.
- `solver/validation.py` performs basic checks:
  - ensures the input is non-empty,
  - verifies that `Kraków` appears in the list (the solver expects to start from `k`),
  - optionally checks each city against the reference list in `places_reference.json`,
  - checks vertex degree conditions required for an Eulerian path.
- `solver/eulerian.py` implements a simple traversal that walks edges (cities) to build a path starting at `k`.

If validation passes, `main.py` computes the path, prints it to stdout, and writes it to the output file.

## Notes & limitations

- The validation step can be disabled with `--no-validate` (useful if your city names aren't present in `places_reference.json`).
- The path-finding implementation is straightforward and picks the first available edge at each step; it works when an Eulerian path exists but isn't optimized for all edge-selection strategies.
- If no valid path is found, the program exits with a non-zero status and prints an error message.

## Files of interest

- `main.py`: CLI entry point
- `cities.txt`: example input
- `places_reference.json`: reference list of Polish place names used for validation
- `solver/graph.py`, `solver/validation.py`, `solver/eulerian.py`: core implementation


Enjoy! Feel free to modify `cities.txt` and rerun the script to try different inputs.
