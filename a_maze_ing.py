"""Command-line entry point for the A-Maze-ing project.

Reads a KEY=VALUE configuration file, generates a maze using the
`mazegen` package, writes it to disk, and launches the interactive
terminal display.
"""

import sys
import random
from typing import Dict, Any
from mazegen.maze_generator import MazeGenerator
from mazegen.maze import save_maze_to_file
from display import MazeDisplay


def read_config(filepath: str) -> Dict[str, Any]:
    """Parse a KEY=VALUE configuration file into a dictionary.

    Blank lines and lines starting with '#' are ignored. Lines without
    an '=' are reported to stdout and skipped rather than raising an
    error.

    Args:
        filepath: Path to the configuration file to read.

    Returns:
        A dictionary mapping each key to its raw string value. Returns
        an empty dictionary if the file cannot be found.
    """
    config_data: Dict[str, Any] = {}

    try:
        with open(filepath, 'r') as file:
            for line in file:
                line = line.strip()

                if not line or line.startswith('#'):
                    continue

                if '=' in line:
                    key, value = line.split('=', 1)
                    config_data[key.strip()] = value.strip()
                else:
                    print(f"Incorrect line! -> {line}")
    except FileNotFoundError:
        print(f"Error:'{filepath}' is not found!"
              f"Default settings will be used.")

    return config_data


def validate_config(raw_config: Dict[str, Any]) -> Dict[str, Any]:
    """Validate and type-convert a raw configuration dictionary.

    Checks that all mandatory keys are present, converts values to
    their expected types, and enforces the project's maze constraints
    (positive dimensions, entry/exit within bounds and distinct from
    each other).

    Args:
        raw_config: Dictionary of raw string values as returned by
            `read_config`.

    Returns:
        A dictionary with validated and converted values: WIDTH and
        HEIGHT as ints, ENTRY and EXIT as (x, y) int tuples, PERFECT as
        a bool, OUTPUT_FILE as a str, and SEED as an int or None.

    Raises:
        ValueError: If a mandatory key is missing, a value has the
            wrong type or format, or a maze constraint (positive
            dimensions, in-bounds and distinct entry/exit) is violated.
    """
    valid_config: Dict[str, Any] = {}
    required_keys = ['WIDTH', 'HEIGHT', 'ENTRY', 'EXIT', 'OUTPUT_FILE',
                     'PERFECT']
    for key in required_keys:
        if key not in raw_config:
            raise ValueError(f"Error: '{key}' could not be found in the file!")

    try:

        valid_config['WIDTH'] = int(raw_config['WIDTH'])
        valid_config['HEIGHT'] = int(raw_config['HEIGHT'])

        entry_parts = raw_config['ENTRY'].split(',')
        valid_config['ENTRY'] = (int(entry_parts[0].strip()),
                                 int(entry_parts[1].strip()))

        exit_parts = raw_config['EXIT'].split(',')
        valid_config['EXIT'] = (int(exit_parts[0].strip()),
                                int(exit_parts[1].strip()))

        valid_config['PERFECT'] = raw_config['PERFECT'].lower() == 'true'
        valid_config['OUTPUT_FILE'] = raw_config['OUTPUT_FILE']
        if 'SEED' in raw_config:
            valid_config['SEED'] = int(raw_config['SEED'])
        else:
            valid_config['SEED'] = None
    except ValueError as e:
        raise ValueError(f"Error: Invalid type found in settings file! {e}")
    except IndexError:
        raise ValueError("Error: ENTRY and EXIT coordinates must be formatted "
                         "with a comma (e.g., 'x,y')!")
    except Exception as e:
        raise ValueError(f"Error: An unexpected configuration error occurred! "
                         f"{e}")

    if valid_config['WIDTH'] <= 0 or valid_config['HEIGHT'] <= 0:
        raise ValueError("Error: WIDTH and HEIGHT must be greater than zero!")

    entry_x, entry_y = valid_config['ENTRY']
    if (
        not (0 <= entry_x < valid_config['WIDTH'])
        or not (0 <= entry_y < valid_config['HEIGHT'])
    ):
        raise ValueError("Error: ENTRY coordinates are out of maze bounds!")

    exit_x, exit_y = valid_config['EXIT']
    if (
        not (0 <= exit_x < valid_config['WIDTH'])
        or not (0 <= exit_y < valid_config['HEIGHT'])
    ):
        raise ValueError("Error: EXIT coordinates are out of maze bounds!")

    if valid_config['ENTRY'] == valid_config['EXIT']:
        raise ValueError("Error: ENTRY and EXIT must be different!")

    return valid_config


def main() -> None:
    """Parse arguments, generate a maze, save it, and launch the display.

    Expects exactly one command-line argument: the path to a
    configuration file. Reads and validates the configuration, generates
    a perfect or Pac-Man style maze accordingly, solves it, writes the
    result to the configured output file, and starts the interactive
    terminal display. Any expected error is caught, printed, and causes
    the program to exit with status 1 instead of crashing.
    """
    if len(sys.argv) != 2:
        print("Error: The usage should be 'python3 a_maze_ing.py "
              "<config.txt>'.")
        sys.exit(1)

    config_file = sys.argv[1]

    try:
        raw_config = read_config(config_file)
        if not raw_config:
            sys.exit(1)

        config = validate_config(raw_config)

        if config['SEED'] is not None:
            random.seed(config['SEED'])

        generator = MazeGenerator(
            width=config['WIDTH'],
            height=config['HEIGHT']
        )

        entry_x, entry_y = config['ENTRY']
        exit_x, exit_y = config['EXIT']

        if generator.is_pattern_cell(entry_x, entry_y):
            raise ValueError(
                "Error: ENTRY cannot be inside the 42 pattern!"
            )

        if generator.is_pattern_cell(exit_x, exit_y):
            raise ValueError(
                "Error: EXIT cannot be inside the 42 pattern!"
            )

        generator.mark_42_pattern_as_visited()

        generator.generate_perfect_maze()
        if not config['PERFECT']:
            generator.generate_pacman_maze()

        generator.add_42()
        shortest_path = generator.solve_maze(config['ENTRY'],
                                             config['EXIT'])

        if not shortest_path:
            raise ValueError(
                "Error: No valid path exists between ENTRY and EXIT!"
            )

        save_maze_to_file(
            maze_grid=generator.grid,
            filepath=config['OUTPUT_FILE'],
            entry=config['ENTRY'],
            exit=config['EXIT'],
            path=shortest_path
        )
        display = MazeDisplay(config['OUTPUT_FILE'])
        display.start_interactive_mode()

    except ValueError as e:
        print(e)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
