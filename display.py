"""[ Başlangıç / Girdi ]
       │
       ▼
[ Dosya Okuma ve Ayrıştırma (Parsing) ]
  ├── Labirent Matrisi (Grid / Hex Değerleri)
  ├── Giriş (Entry) ve Çıkış (Exit) Koordinatları[cite: 1]
  └── En Kısa Yol (N, E, S, W Adımları)[cite: 1]
       │
       ▼
[ Çekirdek Sınıf / Yapı (MazeDisplay) ]
  ├── Terminal Kurulumu (Alternatif Ekran & İmleç Gizleme)
  └── "42" Desen Tespiti (Tam Kapalı Hücreler)[cite: 1]
       │
       ▼
[ Görselleştirme Motoru (Rendering Engine) ]
  ├── Duvar Bitlerinin Çözümlenmesi (Kuzey, Doğu, Güney, Batı)[cite: 1]
  ├── Siberpunk Blok Karakterleri ve Renk Paleti Uygulaması[cite: 2]
  └── En Kısa Yolun Harita Üzerine İşlenmesi[cite: 2]
       │
       ▼
[ Etkileşim ve Olay Döngüsü (Event Loop) ]
  ├── R Tuşu: Yeniden Üret (Regenerate)[cite: 2]
  ├── P Tuşu: Yolu Göster / Gizle (Path Toggle)[cite: 2]
  ├── C Tuşu: Renk Değiştir (Color Rotation)[cite: 2]
  └── Q Tuşu: Güvenli Çıkış (Quit)"""

"""MazeDisplay
│
├── __init__()
│
├── load_file()
│
├── parse_grid()
│
├── parse_footer()
│
├── analyze_cell()
│
├── find_42_pattern()
│
└── draw()"""

"""Dosyayı oku
        │
        ▼
grid_lines oluştu
footer_lines oluştu
        │
        ▼
parse_grid(...)
parse_coordinates(...)
parse_path(...)
        │
        ▼
self.grid
self.entry
self.exit
self.path dolduruldu"""

from typing import List


class MazeDisplay():
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.grid: List[List[int]] = []
        self.path: List[str] = []
        self.entry = None
        self.exit = None
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
        self.grid: List[List[int]] = []

        for line in grid_lines:
            row: List[int] = []
            for char in line:
                row.append(int(char, 16))
            self.grid.append(row)


    def parse_coordinates(self, footer_lines: List[str]) -> None:
        entry_parts = footer_lines[0].split(',')
        entry_parts = (int(entry_parts[0]), int(entry_parts[1]))
        self.entry = entry_parts

        exit_parts = footer_lines[1].split(',')
        exit_parts = (int(exit_parts[0]), int(exit_parts[1]))
        self.exit = exit_parts


    def parse_paths(self, footer_lines: List[str]) -> None:
        self.path = []
        path = footer_lines[2]

        for direction in path:
            if direction not in "EWSN":
                raise ValueError(f"Invalid direction: '{direction}'")
            self.path.append(direction)
