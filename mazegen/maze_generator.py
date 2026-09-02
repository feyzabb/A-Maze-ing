"""Maze generation logic: perfect mazes, Pac-Man style boards, and the
embedded '42' pattern.
"""

import random
from typing import List, Tuple, Dict
from collections import deque
from .maze import Cell
import sys


class MazeGenerator:
    """Generates and solves grid-based mazes.

    Supports two generation modes: a "perfect" maze with exactly one
    path between any two cells (a spanning tree, built via an iterative
    DFS), and a "Pac-Man" style board with loops and open corners/centre.
    A stylised "42" pattern is carved into the middle of the grid and
    kept fully walled off and disconnected from the rest of the maze.

    Attributes:
        width: Number of columns in the maze grid.
        height: Number of rows in the maze grid.
        grid: 2D list of Cell objects representing the maze.
    """

    def __init__(self, width: int, height: int):
        """Initialize the grid and pre-compute the '42' pattern cells.

        Args:
            width: Number of columns the maze should have.
            height: Number of rows the maze should have.
        """
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
        """Compute the grid coordinates that form the '42' pattern.

        The pattern is centred within the grid. If the grid is smaller
        than the pattern's bounding box, the pattern is omitted and a
        warning is printed to stderr.

        Returns:
            A list of (x, y) coordinates belonging to the '42' pattern,
            or an empty list if the grid is too small to fit it.
        """
        pattern_width = 8
        pattern_height = 5

        if self.width < pattern_width or self.height < pattern_height:
            print("Warning: Maze size is too small to fit the '42' pattern.",
                  file=sys.stderr)
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

    def is_pattern_cell(self, x: int, y: int) -> bool:
        """Check whether a coordinate belongs to the '42' pattern.

        Args:
            x: Column index to check.
            y: Row index to check.

        Returns:
            True if (x, y) is part of the '42' pattern, False otherwise.
        """
        return (x, y) in self._pattern_cells

    def mark_42_pattern_as_visited(self) -> None:
        """Mark all '42' pattern cells as visited.

        Must be called before maze generation so that the DFS never
        carves into the pattern, keeping it isolated from the rest of
        the maze.
        """
        if not self._pattern_cells:
            return

        for x, y in self._pattern_cells:
            self.grid[y][x].visited = True

    def _get_neighbors(
        self,
        cell: Cell
    ) -> List[Tuple[str, Cell]]:
        """List the unvisited neighbours of a cell.

        Args:
            cell: The cell whose neighbours should be examined.

        Returns:
            A list of (direction, neighbour_cell) pairs for each
            adjacent, in-bounds, not-yet-visited cell.
        """
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
        """Carve a perfect maze using an iterative depth-first search.

        Starting from (0, 0), repeatedly moves to a random unvisited
        neighbour (removing the wall between them) and pushes it onto a
        stack, backtracking by popping the stack whenever a cell has no
        unvisited neighbours left. The result is a spanning tree: exactly
        one path exists between any two cells. Cells belonging to the
        '42' pattern are skipped if already marked visited via
        `mark_42_pattern_as_visited`.
        """
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
        """Turn a perfect maze into a playable Pac-Man style board.

        Removes dead-ends, adds independent loops, and opens the four
        corners and the centre cell so the board is fully connected and
        offers a chased player multiple escape routes.
        """
        self._remove_dead_ends()
        self._add_loops(2)
        self._open_pacman_special_cells()

    def _is_safe_to_break(self, x: int, y: int, direction: str) -> bool:
        """Check whether removing a wall would violate maze constraints.

        Temporarily removes the wall between (x, y) and its neighbour in
        `direction`, then checks that the neighbour is in-bounds, is not
        part of the '42' pattern, and that no 3x3 fully-open area would
        result. The wall is always restored before returning.

        Args:
            x: Column index of the cell whose wall would be removed.
            y: Row index of the cell whose wall would be removed.
            direction: Cardinal direction ('N', 'S', 'E', 'W') of the
                wall to test.

        Returns:
            True if removing the wall is safe, False otherwise.
        """
        dx, dy = 0, 0
        if direction == "N":
            dy = -1
        elif direction == "S":
            dy = 1
        elif direction == "E":
            dx = 1
        elif direction == "W":
            dx = -1

        nx, ny = x + dx, y + dy

        if not (0 <= nx < self.width and 0 <= ny < self.height):
            return False

        pattern_cells = set(self._pattern_cells)

        if (nx, ny) in pattern_cells:
            return False

        self.grid[y][x].walls[direction] = False
        opposite = {"N": "S", "S": "N", "E": "W", "W": "E"}[direction]
        self.grid[ny][nx].walls[opposite] = False

        is_safe = True

        for cy in range(max(0, min(y, ny) - 2), min(max(y, ny) + 1,
                                                    self.height - 2)):
            for cx in range(max(0, min(x, nx) - 2), min(max(x, nx) + 1,
                                                        self.width - 2)):
                area_is_fully_open = True

                for i in range(3):
                    for j in range(3):
                        cell_y = cy + i
                        cell_x = cx + j

                        if j < 2 and self.grid[cell_y][cell_x].walls["E"]:
                            area_is_fully_open = False
                            break
                        if i < 2 and self.grid[cell_y][cell_x].walls["S"]:
                            area_is_fully_open = False
                            break
                    if not area_is_fully_open:
                        break
                if area_is_fully_open:
                    is_safe = False
                    break

            if not is_safe:
                break

        self.grid[y][x].walls[direction] = True
        self.grid[ny][nx].walls[opposite] = True

        return is_safe

    def _remove_dead_ends(self) -> None:
        """Repeatedly break a wall on every dead-end cell until none remain.

        A dead-end is a non-pattern cell with exactly three closed walls
        (a single opening). For each dead-end, one of its breakable walls
        is removed at random, provided doing so is safe (see
        `_is_safe_to_break`). The process repeats until a full pass makes
        no further changes.
        """
        opposite_walls = {
                    "N": "S",
                    "S": "N",
                    "E": "W",
                    "W": "E",
                }
        pattern_cells = set(self._pattern_cells)

        while True:
            changed = False

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

                    if len(closed_walls) != 3:
                        continue

                    breakable_walls = []

                    if "N" in closed_walls and y > 0:
                        breakable_walls.append("N")
                    if "S" in closed_walls and y < self.height - 1:
                        breakable_walls.append("S")
                    if "E" in closed_walls and x < self.width - 1:
                        breakable_walls.append("E")
                    if "W" in closed_walls and x > 0:
                        breakable_walls.append("W")

                    safe_walls = [
                        wall
                        for wall in breakable_walls
                        if self._is_safe_to_break(x, y, wall)
                    ]

                    if not safe_walls:
                        continue

                    wall_to_break = random.choice(safe_walls)

                    cell.walls[wall_to_break] = False

                    if wall_to_break == "N":
                        neighbor = self.grid[y - 1][x]

                    elif wall_to_break == "S":
                        neighbor = self.grid[y + 1][x]

                    elif wall_to_break == "E":
                        neighbor = self.grid[y][x + 1]

                    else:
                        neighbor = self.grid[y][x - 1]

                    neighbor.walls[
                        opposite_walls[wall_to_break]
                        ] = False

                    changed = True

            if not changed:
                break

    def _add_loops(self, minimum_loops: int = 2) -> None:
        """Add independent loops to the maze by breaking extra walls.

        Collects every wall whose removal would be safe (see
        `_is_safe_to_break`), shuffles the candidates, and breaks the
        first `minimum_loops` of them that are still valid at the time
        they are processed.

        Args:
            minimum_loops: The number of loops to attempt to add.
                Defaults to 2, matching the project's requirement of at
                least two independent routes.
        """
        pattern_cells = set(self._pattern_cells)

        directions = [
            ("N", 0, -1, "S"),
            ("S", 0, 1, "N"),
            ("E", 1, 0, "W"),
            ("W", -1, 0, "E"),
        ]

        candidates = []

        for y in range(self.height):
            for x in range(self.width):
                if (x, y) in pattern_cells:
                    continue

                cell = self.grid[y][x]

                for direction, dx, dy, opposite in directions:
                    nx = x + dx
                    ny = y + dy

                    if not (0 <= nx < self.width and 0 <= ny < self.height):
                        continue

                    if (nx, ny) in pattern_cells:
                        continue

                    if not cell.walls[direction]:
                        continue

                    if self._is_safe_to_break(x, y, direction):
                        candidates.append(
                            (x, y, direction, nx, ny, opposite)
                        )

        random.shuffle(candidates)

        loops_added = 0

        for x, y, direction, nx, ny, opposite in candidates:
            if loops_added >= minimum_loops:
                break

            if not self.grid[y][x].walls[direction]:
                continue

            if not self._is_safe_to_break(x, y, direction):
                continue

            self.grid[y][x].walls[direction] = False
            self.grid[ny][nx].walls[opposite] = False

            loops_added += 1

    def _close_cell_completely(self, x: int, y: int) -> None:
        """Seal a cell off from all of its neighbours.

        Sets all four walls of the target cell to closed, and updates
        each existing neighbour so the shared wall is closed on both
        sides.

        Args:
            x: Column index of the cell to seal.
            y: Row index of the cell to seal.
        """
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
        """Fully wall off every cell belonging to the '42' pattern.

        Ensures the pattern is rendered as a visible block of closed
        cells, isolated from the surrounding maze, as required by the
        project specification.
        """
        if not self._pattern_cells:
            return

        for x, y in self._pattern_cells:
            self._close_cell_completely(x, y)

    def solve_maze(self, start: Tuple[int, int],
                   end: Tuple[int, int]) -> List[str]:
        """Find the shortest path between two cells via breadth-first search.

        Args:
            start: (x, y) coordinates of the starting cell.
            end: (x, y) coordinates of the target cell.

        Returns:
            A list of cardinal direction letters ('N', 'E', 'S', 'W')
            describing the shortest path from `start` to `end`, in
            order. Returns an empty list if no path exists.
        """
        start_x, start_y = start
        exit_x, exit_y = end

        start_cell = self.grid[start_y][start_x]

        queue = deque([start_cell])
        visited = set()
        visited.add((start_x, start_y))

        parent_map: Dict[Tuple[int, int], Tuple[Tuple[int, int], str]] = {}

        while queue:
            current_cell = queue.popleft()

            if current_cell.x == exit_x and current_cell.y == exit_y:
                break

            directions = [
                (0, -1, 'N', 'N'),
                (0, 1, 'S', 'S'),
                (1, 0, 'E', 'E'),
                (-1, 0, 'W', 'W')
            ]

            for dx, dy, wall_dir, out_dir in directions:
                if not current_cell.walls[wall_dir]:
                    nx, ny = current_cell.x + dx, current_cell.y + dy

                    if 0 <= nx < self.width and 0 <= ny < self.height:
                        if (nx, ny) not in visited:
                            visited.add((nx, ny))
                            queue.append(self.grid[ny][nx])
                            parent_map[(nx, ny)] = ((current_cell.x,
                                                     current_cell.y), out_dir)
        path = []
        curr = (exit_x, exit_y)

        while curr != (start_x, start_y):
            if curr not in parent_map:
                return []

            prev_coords, direction = parent_map[curr]
            path.append(direction)
            curr = prev_coords
        path.reverse()

        return path

    def _open_pacman_special_cells(self) -> None:
        """Ensure the four corners and the centre cell are open.

        For each special cell (the four corners and the grid centre,
        skipping any that fall inside the '42' pattern), walls are
        broken one at a time until fewer than three remain closed, so
        each of these cells ends up with at least two openings.
        """
        center_x = self.width // 2
        center_y = self.height // 2

        special_cells = [
            (0, 0),
            (self.width - 1, 0),
            (0, self.height - 1),
            (self.width - 1, self.height - 1),
            (center_x, center_y)
        ]

        opposite_walls = {"N": "S", "S": "N", "E": "W", "W": "E"}

        for x, y in special_cells:
            if (x, y) in self._pattern_cells:
                continue

            cell = self.grid[y][x]
            closed_walls = [direction for direction, is_closed in
                            cell.walls.items() if is_closed]

            while len(closed_walls) >= 3:
                breakable_walls = []

                if "N" in closed_walls and y > 0:
                    breakable_walls.append("N")
                if "S" in closed_walls and y < self.height - 1:
                    breakable_walls.append("S")
                if "E" in closed_walls and x < self.width - 1:
                    breakable_walls.append("E")
                if "W" in closed_walls and x > 0:
                    breakable_walls.append("W")

                safe_walls = [w for w in breakable_walls if
                              self._is_safe_to_break(x, y, w)]

                if not safe_walls:
                    break
                wall_to_break = random.choice(safe_walls)
                cell.walls[wall_to_break] = False

                nx, ny = x, y
                if wall_to_break == "N":
                    ny -= 1
                elif wall_to_break == "S":
                    ny += 1
                elif wall_to_break == "E":
                    nx += 1
                elif wall_to_break == "W":
                    nx -= 1

                self.grid[ny][nx].walls[opposite_walls[wall_to_break]] = False
                closed_walls = [direction for direction, is_closed
                                in cell.walls.items()
                                if is_closed]
