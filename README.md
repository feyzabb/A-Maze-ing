*This project has been created as part of the 42 curriculum by fbiber, raltunda.*

# A-Maze-ing

A standalone Python maze generation and solving project featuring an interactive terminal-based ASCII renderer.

## Description
A-Maze-ing is a modular Python tool capable of generating random mazes based on a provided configuration file. It outputs the maze using a hexadecimal wall representation. The generator supports two distinct modes: a perfect maze with exactly one valid path from entry to exit, and a default Pac-Man style playable board with multiple loops and no dead-ends. A hidden "42" pattern is explicitly embedded into the maze structure unless the grid size is too small. The project also includes an interactive terminal user interface for visualization.

## Instructions

### Requirements
* Python 3.10 or later.

### Installation & Usage

**1. Create a virtual environment and install dependencies via Makefile:**
```bash
python3 -m venv venv
source venv/bin/activate
make install
```
*(Note: `make install` installs required packages.)*

**2. Run the generator:**
```bash
make run
```
*Or manually execute the script with the configuration file:*
```bash
python3 a_maze_ing.py config.txt
```
*(Note: The main script must be named `a_maze_ing.py` and accept a single configuration file argument.)*

**Interactive Controls (Terminal UI):**
When the display launches, you can use the following numeric inputs:
* `1`: Re-generate a new maze.
* `2`: Show/Hide the shortest path.
* `3`: Rotate the wall colours.
* `4`: Quit.

## Algorithm Details

The project utilizes a randomized Depth-First Search (DFS) approach to construct the mazes.

* **Perfect Mazes (`PERFECT=True`):** The algorithm uses an iterative stack-based implementation to carve out a perfect spanning tree. This guarantees exactly one solution path from the entry to the exit and prevents Python `RecursionError` on large grids.
* **Imperfect Mazes (Pac-Man Mode):** When `PERFECT=False` (the default mode), the algorithm first generates a perfect maze, then actively removes dead-ends and adds at least two independent loops (`_add_loops`) to ensure multiple routes exist. During wall removal, it strictly validates the structure to prevent the creation of open areas larger than 2x2 cells, explicitly blocking any 3x3 open spaces.

## Configuration Format

The maze generation is controlled by a plain text file (e.g., `config.txt`) using a strict `KEY=VALUE` format. Lines starting with `#` are ignored.

**Mandatory Keys:**
* `WIDTH`: Maze width in cells (e.g., `WIDTH=20`).
* `HEIGHT`: Maze height in cells (e.g., `HEIGHT=20`).
* `ENTRY`: Entry coordinates formatted as `x,y` (e.g., `ENTRY=0,0`).
* `EXIT`: Exit coordinates formatted as `x,y` (e.g., `EXIT=19,19`).
* `OUTPUT_FILE`: The output filename for the hexadecimal maze data (e.g., `OUTPUT_FILE=maze.txt`).
* `PERFECT`: Boolean flag (`True` or `False`).

**Optional Keys:**
* `SEED`: An integer seed for the random number generator to ensure reproducible mazes.

## Code Reusability

The core maze generation logic is decoupled into a standalone package named `mazegen`.

**Usage Example in Python:**
```python
from mazegen.maze_generator import MazeGenerator
from mazegen.maze import save_maze_to_file

# 1. Instantiate the generator
generator = MazeGenerator(width=20, height=20)

# 2. Mark the 42 pattern and generate the maze
generator.mark_42_pattern_as_visited()
generator.generate_perfect_maze()

# 3. Solve the maze to find the shortest path
shortest_path = generator.solve_maze((0, 0), (19, 19))

# 4. Access the generated structure directly (grid of Cell objects)
for row in generator.grid:
    for cell in row:
        walls = cell.walls  # {'N': bool, 'E': bool, 'S': bool, 'W': bool}
```

## Team and Project Management

* **Roles:**
  * **fbiber** was responsible for the core algorithm logic: the perfect/pac-man maze generation, the iterative DFS implementation, and the "42" pattern integration inside the `mazegen` package.owned the middle layer connecting the two sides: the configuration file reading/validation and the `a_maze_ing.py` entry point that wires the `mazegen` backend to the display frontend.
  * **raltunda** managed the interactive terminal display (`display.py`), the hexadecimal file parsing, and the user interface for toggling paths and colours.
 

* **Planning & Evolution:** We split the project into three clear layers — the backend (`mazegen` package), the middle/integration layer (config parsing and `a_maze_ing.py`), and the frontend (`display.py`) — which let the three of us work in parallel with minimal blocking dependencies.

* **Tools Used:** Git for version control, `Makefile` for task automation, `flake8` for syntax checking, and `mypy` for strict static type checking.

## Resources & AI Usage
* **Resources:** Python official documentation for type hinting (`typing`) and standard libraries.
* **AI Usage:** AI was utilized to help refine standard `Makefile` recipes, debug `mypy` typing issues (especially regarding list structures in display rendering), and format this `README.md` to meet the specific requirements of the assignment.