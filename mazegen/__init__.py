"""Public API for the mazegen package.

Exposes the maze generation class and the file-saving helper so they
can be imported directly as ``from mazegen import MazeGenerator``.
"""

from mazegen.maze_generator import MazeGenerator
from mazegen.maze import save_maze_to_file


__all__ = ["MazeGenerator", "save_maze_to_file"]
