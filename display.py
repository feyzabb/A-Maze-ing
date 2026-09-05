"""Interactive terminal-based ASCII renderer for A-Maze-ing mazes."""

from typing import List
import os
import sys


class MazeDisplay():
    """Loads a maze output file and renders it as coloured ASCII art.

    Provides an interactive terminal menu to regenerate the maze,
    toggle the shortest-path overlay, and cycle through wall colours.

    Attributes:
        filepath: Path to the maze output file being displayed.
        grid: 2D list of integer wall-bitmask values, one per cell.
        path: List of direction letters describing the shortest path.
        entry: (x, y) coordinates of the maze entry, or None.
        exit: (x, y) coordinates of the maze exit, or None.
        show_path: Whether the shortest-path overlay is currently shown.
        color_index: Index of the currently selected wall colour.
    """

    WALL_CHAR = "██"
    EMPTY_CHAR = " "
    PATH_CHAR = "  "

    COLOR_GREEN = "\033[48;5;52m"
    COLOR_RED = "\033[48;5;91m"
    COLOR_CYAN = "\033[48;5;111m"
    COLOR_RESET = "\033[0m"
    PATH_COLOR = "\033[48;5;015m"

    def __init__(self, filepath: str):
        """Load and parse the maze file at the given path.

        Args:
            filepath: Path to the maze output file to load and display.
        """
        self.filepath = filepath
        self.grid: List[List[int]] = []
        self.path: List[str] = []
        self.entry: tuple[int, int] | None = None
        self.exit: tuple[int, int] | None = None
        self.show_path = False
        self.color_index = 0
        self.load_maze()

    def load_maze(self) -> None:
        """Read the maze file and populate grid, entry, exit, and path.

        The file is split into a grid section (hexadecimal rows) and a
        footer section (entry, exit, and path), separated by a blank
        line. Exits the program with an error message if the file is
        missing or cannot be parsed.
        """
        grid_lines: List[str] = []
        footer_lines: List[str] = []
        reading_grid = True

        try:
            with open(self.filepath, 'r') as file:
                for line in file:
                    line = line.strip()

                    if not line:
                        reading_grid = False
                        continue
                    if reading_grid:
                        grid_lines.append(line)
                    else:
                        footer_lines.append(line)
            self.parse_grid(grid_lines)
            self.parse_coordinates(footer_lines)
            self.parse_paths(footer_lines)

        except FileNotFoundError:
            print(f"Error:'{self.filepath}' is not found!"
                  f"Please ensure the maze was generated successfully."
                  f"file=sys.stderr")
            sys.exit(1)
        except Exception as e:
            print(f"Error: An unexpected issue occurred while reading '"
                  f"{self.filepath}': {e}", file=sys.stderr)
            sys.exit(1)

    def parse_grid(self, grid_lines: List[str]) -> None:
        """Convert the hexadecimal grid lines into integer wall values.

        Args:
            grid_lines: Raw text lines from the file's grid section, one
                hexadecimal digit per cell.
        """
        self.grid = []

        for line in grid_lines:
            row: List[int] = []
            for char in line:
                row.append(int(char, 16))
            self.grid.append(row)

    def parse_coordinates(self, footer_lines: List[str]) -> None:
        """Extract entry and exit coordinates from the file footer.

        Args:
            footer_lines: Lines following the blank line separator; the
                first two lines are expected to hold the entry and exit
                coordinates as 'x,y'.
        """
        entry_parts = footer_lines[0].split(',')
        self.entry = (
            int(entry_parts[0]),
            int(entry_parts[1])
        )

        exit_parts = footer_lines[1].split(',')
        self.exit = (
            int(exit_parts[0]),
            int(exit_parts[1])
        )

    def parse_paths(self, footer_lines: List[str]) -> None:
        """Extract the shortest-path directions from the file footer.

        Args:
            footer_lines: Lines following the blank line separator; the
                third line is expected to hold the path as a string of
                'N', 'E', 'S', 'W' characters.

        Raises:
            ValueError: If the path string contains a character other
                than 'N', 'E', 'S', or 'W'.
        """
        self.path = []
        path = footer_lines[2]

        for direction in path:
            if direction not in "EWSN":
                raise ValueError(f"Invalid direction: '{direction}'")
            self.path.append(direction)

    def get_walls(self, cell_value: int) -> dict[str, bool]:
        """Decode a cell's hexadecimal wall bitmask into a dict of walls.

        Args:
            cell_value: Integer wall bitmask (N=1, E=2, S=4, W=8).

        Returns:
            A dictionary mapping each cardinal direction to whether that
            wall is closed.
        """
        return {
            'N': bool(cell_value & 1),
            'E': bool(cell_value & 2),
            'S': bool(cell_value & 4),
            'W': bool(cell_value & 8)
        }

    def start_interactive_mode(self) -> bool:
        """Run the interactive terminal menu loop.

        Repeatedly draws the maze and prompts the user to regenerate the
        maze, toggle the shortest-path overlay, rotate wall colours, or
        quit. Runs until the user chooses to quit.
        """
        show_path = False
        colors = [self.COLOR_GREEN, self.COLOR_CYAN, self.COLOR_RED]
        color_index = 0

        while True:
            current_color = colors[color_index]
            self.draw(show_path, current_color)

            print("\n=== A-Maze_ing ===")
            print("1. Re-generate a new maze")
            print("2. Show/Hide the shortest path")
            print("3. Rotate the wall colours")
            print("4. Quit")

            choice = input("Choice?(1-4):")

            if choice == '1':
                print("A new maze is being generated...")
                return True
            elif choice == '2':
                show_path = not show_path
            elif choice == '3':
                color_index = (color_index + 1) % len(colors)
            elif choice == '4':
                print("Terminating...")
                return False
            else:
                print("Invalid selection; please enter a "
                      "value between 1 and 4.")
                input("Press Enter to continue...")

    def draw(self, show_path: bool, current_color: str) -> None:
        """Clear the terminal and render the full maze once.

        Args:
            show_path: Whether to highlight the shortest path.
            current_color: ANSI background colour escape code to use
                for the maze walls.
        """
        os.system('clear' if os.name == 'posix' else 'cls')

        path_coords = self._get_path_coords(show_path)
        self._color = current_color
        self._path_coords = path_coords

        print(self._border_line(0, 'N'))
        for y, row in enumerate(self.grid):
            print(self._room_line(y, row))
            print(self._border_line(y, 'S'))

    def _get_path_coords(self, show_path: bool) -> dict[tuple[int, int], str]:
        """Compute, for each cell on the shortest path, its exit direction.

        Args:
            show_path: Whether the path overlay is enabled. If False
                (or if there is no entry/path data), an empty mapping is
                returned.

        Returns:
            A dictionary mapping each (x, y) cell on the path to the
            direction letter used to leave it (empty string for the
            final cell).
        """
        path_coords: dict[tuple[int, int], str] = {}
        if not (show_path and self.entry and self.path):
            return path_coords

        moves = {'N': (0, -1), 'S': (0, 1), 'E': (1, 0), 'W': (-1, 0)}
        curr_x, curr_y = self.entry

        for direction in self.path:
            path_coords[(curr_x, curr_y)] = direction
            dx, dy = moves[direction]
            curr_x, curr_y = curr_x + dx, curr_y + dy
        path_coords[(curr_x, curr_y)] = ""
        return path_coords

    def _border_line(self, y: int, key: str) -> str:
        """Render one horizontal border line (north or south) of a row.

        Args:
            y: Row index whose border is being rendered.
            key: Which side of the row this border represents, 'N' or
                'S'.

        Returns:
            The rendered border line as a string, including ANSI colour
            codes and any highlighted path segments.
        """
        line = f"{self._color}  {self.COLOR_RESET}"
        for x, cell_val in enumerate(self.grid[y]):
            walls = self.get_walls(cell_val)
            connected_down = (
                key == 'S'
                and y < len(self.grid) - 1
                and (x, y) in self._path_coords
                and (x, y + 1) in self._path_coords
                and (
                    self._path_coords[(x, y)] == 'S'
                    or self._path_coords[(x, y + 1)] == 'N'
                )
            )
            if connected_down:
                segment = (
                    f"{self.PATH_COLOR}"
                    f"  "
                    f"{self.COLOR_RESET}"
                )
            else:
                segment = (
                    f"{self._color}  {self.COLOR_RESET}"
                    if walls[key]
                    else "  "
                )
            line += segment + f"{self._color}  {self.COLOR_RESET}"
        return line

    def _room_line(self, y: int, row: list[int]) -> str:
        """Render one row of maze cells, including side walls and symbols.

        Args:
            y: Row index being rendered.
            row: List of wall bitmask values for the cells in this row.

        Returns:
            The rendered row as a string, including ANSI colour codes,
            highlighted path segments, and entry/exit markers.
        """
        line = ""

        for x, cell_val in enumerate(row):
            walls = self.get_walls(cell_val)

            connected_left = (
                x > 0
                and (x, y) in self._path_coords
                and (x - 1, y) in self._path_coords
                and (
                    self._path_coords[(x - 1, y)] == 'E'
                    or self._path_coords[(x, y)] == 'W'
                )
            )

            if connected_left:
                line += (
                    f"{self.PATH_COLOR}  {self.COLOR_RESET}"
                )
            else:
                line += (
                    f"{self._color}  {self.COLOR_RESET}"
                    if walls['W']
                    else "  "
                )

            line += self._room_symbol(x, y, cell_val)

        last_walls = self.get_walls(row[-1])

        line += (
            f"{self._color}  {self.COLOR_RESET}"
            if last_walls['E']
            else "  "
        )

        return line

    def _room_symbol(self, x: int, y: int, cell_val: int) -> str:
        """Pick the symbol to render for a single cell.

        Args:
            x: Column index of the cell.
            y: Row index of the cell.
            cell_val: Wall bitmask value of the cell.

        Returns:
            'E ' for the entry cell, ' X' for the exit cell, a solid
            block for a fully closed ('42' pattern) cell, a highlighted
            path marker if the cell is on the shown path, or two blank
            spaces otherwise.
        """
        if (x, y) == self.entry:
            return "E "
        if (x, y) == self.exit:
            return " X"
        if cell_val == 15:
            return f"{self._color}{self.WALL_CHAR}{self.COLOR_RESET}"
        if (x, y) in self._path_coords:
            return f"{self.PATH_COLOR}{self.PATH_CHAR}{self.COLOR_RESET}"
        return "  "
