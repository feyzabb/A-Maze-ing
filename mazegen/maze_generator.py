import random
from typing import List, Tuple

from .maze import Cell


class MazeGenerator:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = [
            [Cell(x, y) for x in range(width)]
            for y in range(height)
        ]
        self._pattern_cells: List[Tuple[int, int]] = (
            self._compute_42_pattern_cells()
        )

    def _compute_42_pattern_cells(self) -> List[Tuple[int, int]]:
        pattern_width = 8
        pattern_height = 5

        if self.width < pattern_width or self.height < pattern_height:
            return []

        start_x = (self.width - pattern_width) // 2
        start_y = (self.height - pattern_height) // 2

        pattern_offsets = [
            (0, 0),         (2, 0),
            (0, 1),         (2, 1),
            (0, 2), (1, 2), (2, 2),
                            (2, 3),
                            (2, 4),

            (5, 0), (6, 0), (7, 0),
                            (7, 1),
            (5, 2), (6, 2), (7, 2),
            (5, 3),
            (5, 4), (6, 4), (7, 4)
        ]

        return [(start_x + dx, start_y + dy) for dx, dy in pattern_offsets]

    def mark_42_pattern_as_visited(self) -> None:
        if not self._pattern_cells:
            print("Error: Maze size is not big enough for the 42 pattern!")
            return

        for x, y in self._pattern_cells:
            self.grid[y][x].visited = True

    def _get_neighbors(
        self,
        cell: Cell
    ) -> List[Tuple[str, Cell]]:
        neighbors = []
        x, y = cell.x, cell.y

        if y > 0 and not self.grid[y - 1][x].visited:
            neighbors.append(("N", self.grid[y - 1][x]))

        if y < self.height - 1 and not self.grid[y + 1][x].visited:
            neighbors.append(("S", self.grid[y + 1][x]))

        if x < self.width - 1 and not self.grid[y][x + 1].visited:
            neighbors.append(("E", self.grid[y][x + 1]))

        if x > 0 and not self.grid[y][x - 1].visited:
            neighbors.append(("W", self.grid[y][x - 1]))

        return neighbors

    def generate_perfect_maze(self) -> None:
        start_cell = self.grid[0][0]
        start_cell.visited = True

        stack = [start_cell]

        while stack:
            current = stack[-1]
            valid_moves = self._get_neighbors(current)

            if valid_moves:
                direction, next_cell = random.choice(valid_moves)

                opposite_walls = {
                    "N": "S",
                    "S": "N",
                    "E": "W",
                    "W": "E",
                }

                current.walls[direction] = False
                next_cell.walls[opposite_walls[direction]] = False
                next_cell.visited = True
                stack.append(next_cell)
            else:
                stack.pop()

    def generate_pacman_maze(self) -> None:
        self.generate_perfect_maze()
        self._remove_dead_ends()

    def _remove_dead_ends(self):

        opposite_walls = {
                    "N": "S",
                    "S": "N",
                    "E": "W",
                    "W": "E",
                }
        pattern_cells = set(self._pattern_cells)
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) in pattern_cells:
                    continue

                cell = self.grid[y][x]

                closed_walls = [
                    direction
                    for direction, is_closed in cell.walls.items()
                    if is_closed
                ]

                if len(closed_walls) == 3:
                    breakable_walls = []
                    if "N" in closed_walls and y > 0:
                        breakable_walls.append("N")
                    if "S" in closed_walls and y < self.height - 1:
                        breakable_walls.append("S")
                    if "E" in closed_walls and x < self.width - 1:
                        breakable_walls.append("E")
                    if "W" in closed_walls and x > 0:
                        breakable_walls.append("W")
                    if breakable_walls:
                        wall_to_break = random.choice(breakable_walls)
                        cell.walls[wall_to_break] = False

                        if wall_to_break == "N":
                            neighbor = self.grid[y-1][x]
                        elif wall_to_break == "S":
                            neighbor = self.grid[y+1][x]
                        elif wall_to_break == "E":
                            neighbor = self.grid[y][x+1]
                        elif wall_to_break == "W":
                            neighbor = self.grid[y][x-1]

                        neighbor.walls[opposite_walls[wall_to_break]] = False

    def _close_cell_completely(self, x: int, y: int) -> None:
        cell = self.grid[y][x]
        cell.walls["N"] = True
        cell.walls["S"] = True
        cell.walls["E"] = True
        cell.walls["W"] = True

        if y > 0:
            self.grid[y-1][x].walls["S"] = True
        if y < self.height - 1:
            self.grid[y+1][x].walls["N"] = True
        if x > 0:
            self.grid[y][x-1].walls["E"] = True
        if x < self.width - 1:
            self.grid[y][x+1].walls["W"] = True

    def add_42(self) -> None:
        if not self._pattern_cells:
            print("Error: Maze size is not big enough for the 42 pattern!")
            return

        for x, y in self._pattern_cells:
            self._close_cell_completely(x, y)
