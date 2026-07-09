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
