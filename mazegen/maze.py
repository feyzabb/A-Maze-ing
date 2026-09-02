"""Core maze data structures and file persistence utilities."""

from typing import List, Tuple


class Cell:
    """A single maze cell with four cardinal walls.

    Attributes:
        x: Column index of the cell within the maze grid.
        y: Row index of the cell within the maze grid.
        visited: Whether the cell has been visited during generation.
        walls: Mapping of cardinal directions ('N', 'E', 'S', 'W') to a
            boolean flag indicating whether that wall is closed.
    """

    def __init__(self, x: int, y: int):
        """Initialize a cell with all four walls closed.

        Args:
            x: Column index of the cell.
            y: Row index of the cell.
        """
        self.x = x
        self.y = y
        self.visited = False

        self.walls = {
            'N': True,
            'E': True,
            'S': True,
            'W': True
        }

    def get_hex_value(self) -> str:
        """Encode the cell's closed walls as a single hexadecimal digit.

        Uses the bitmask N=1, E=2, S=4, W=8, matching the output file
        format expected by the project.

        Returns:
            A single uppercase hexadecimal character representing which
            walls of the cell are closed.
        """
        value = 0

        if self.walls['N']:
            value += 1
        if self.walls['E']:
            value += 2
        if self.walls['S']:
            value += 4
        if self.walls['W']:
            value += 8
        return f"{value:X}"


def save_maze_to_file(maze_grid: List[List[Cell]], filepath: str,
                      entry: Tuple[int, int], exit: Tuple[int, int],
                      path: List[str]) -> None:
    """Write a generated maze to disk in the project's output format.

    The file contains one hexadecimal-encoded row per line, followed by
    a blank line, the entry coordinates, the exit coordinates, and the
    shortest-path directions.

    Args:
        maze_grid: 2D grid of Cell objects representing the maze.
        filepath: Destination path for the output file.
        entry: (x, y) coordinates of the maze entry point.
        exit: (x, y) coordinates of the maze exit point.
        path: Sequence of cardinal direction letters ('N', 'E', 'S',
            'W') describing the shortest path from entry to exit.

    Returns:
        None. The outcome is reported to stdout; any I/O error is
        caught and printed rather than raised, so the caller never sees
        an exception from this function.
    """
    try:
        with open(filepath, 'w') as f:
            for row in maze_grid:
                hex_row = ""
                for cell in row:
                    hex_row += cell.get_hex_value()
                f.write(hex_row + "\n")
            f.write("\n")
            f.write(f"{entry[0]},{entry[1]}\n")
            f.write(f"{exit[0]},{exit[1]}\n")
            f.write("".join(path)+"\n")

        print(f"Success: The maze has been saved to the {filepath} file!")
    except Exception as e:
        print(f"Error: The file could not be saved! {e}")
