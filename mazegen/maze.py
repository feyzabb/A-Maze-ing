from typing import List, Tuple


class Cell:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

        self.walls = {
            'N': True,
            'E': True,
            'S': True,
            'W': True
        }

    def get_hex_value(self) -> str:
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

        print(f"Başarılı:Labirent {filepath} dosyasına kaydedildi!")
    except Exception as e:
        print(f"Hata: Dosya kaydedilemedi! {e}")
