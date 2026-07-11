import random
from typing import List, Tuple

from maze import Cell


class MazeGenerator:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = [
            [Cell(x, y) for x in range(width)]
            for y in range(height)
        ]

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
