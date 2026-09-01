from typing import List


class MazeDisplay():
    WALL_CHAR = "██"
    EMPTY_CHAR = " "
    PATH_CHAR = "••"

    COLOR_GREEN = "\033[92m"
    COLOR_RED = "\033[91m"
    COLOR_CYAN = "\033[96m"
    COLOR_RESET = "\033[0m"

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.grid: List[List[int]] = []
        self.path: List[str] = []
        self.entry: tuple[int, int] | None = None
        self.exit: tuple[int, int] | None = None
        self.load_maze()

    def load_maze(self) -> None:
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
                  f"Default settings will be used.")

    def parse_grid(self, grid_lines: List[str]) -> None:
        self.grid = []

        for line in grid_lines:
            row: List[int] = []
            for char in line:
                row.append(int(char, 16))
            self.grid.append(row)

    def parse_coordinates(self, footer_lines: List[str]) -> None:
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
        self.path = []
        path = footer_lines[2]

        for direction in path:
            if direction not in "EWSN":
                raise ValueError(f"Invalid direction: '{direction}'")
            self.path.append(direction)

    def get_walls(self, cell_value: int) -> dict[str, bool]:
        return {
            'N': bool(cell_value & 1),
            'E': bool(cell_value & 2),
            'S': bool(cell_value & 4),
            'W': bool(cell_value & 8)
        }

    def start_interactive_mode(self):
        show_path = False
        current_color = self.COLOR_GREEN

        while True:
            print("\n=== A-Maze_ing ===")
            print("1. Re-generate a new maze")
            print("2. Show/Hide the shortest path")
            print("3. Rotate the wall colours")
            print("4. Quit")

            choice = input("Choice?(1-4):")

            if choice == '1':
                pass
            elif choice == '2':
                show_path = not show_path
            elif choice == '3':
                pass
            elif choice == '4':
                print("Logging out...")
                break
            else:
                print("Invalid selection; please enter a "
                      "value between 1 and 4.")
