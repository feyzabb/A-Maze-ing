a_maze_ing_project/
├── a_maze_ing.py          # Ana çalıştırılabilir dosya (Entry point)
├── Makefile               # Otomasyon komutları (install, run, debug, clean, lint)
├── config.txt             # Varsayılan yapılandırma dosyası
├── README.md              # Proje dokümantasyonu (Özel başlık ve yönergelerle)
├── LICENSE.md             # Modül için açık kaynak lisans dosyası
├── display.py             # Görselleştirme ve kullanıcı etkileşimi (Terminal veya MLX)
└── mazegen/               # Yeniden kullanılabilir labirent üretim paketi
    ├── __init__.py
    ├── generator.py       # MazeGenerator sınıfı ve ana algoritmalar
    └── solver.py          # BFS/A* ile en kısa yol bulma algoritmaları
    