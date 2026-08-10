import sys
from typing import Dict, Any
from mazegen.maze_generator import MazeGenerator
from mazegen.maze import save_maze_to_file

def read_config(filepath: str) -> Dict[str, Any]:
    config_data: Dict[str, Any] = {}

    try:
        with open(filepath, 'r') as file:
            for line in file:
                line = line.strip()

                if not line:
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
    valid_config: Dict[str, Any] = {}
    required_keys = ['WIDTH', 'HEIGHT', 'ENTRY', 'EXIT', 'OUTPUT_FILE', 'PERFECT']
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

    except ValueError as e:
        raise ValueError(f"Error: Invalid type found in settings file! {e}")
    except IndexError:
        raise ValueError("Error: ENTRY and EXIT coordinates must be formatted with a comma (e.g., 'x,y')!")
    except Exception as e:
        raise ValueError(f"Error: An unexpected configuration error occurred! {e}")

    return valid_config


def main() -> None:
    if len(sys.argv) != 2:
        print("Error: The usage should be 'python3 a_maze_ing.py <config.txt>'.")
        sys.exit(1)
    
    config_file = sys.argv[1]
    
    try:
        raw_config = read_config(config_file)
        if not raw_config:
            sys.exit(1)
            
        config = validate_config(raw_config)
        
        # 1. Generator'ı başlat
        # (Eğer MazeGenerator __init__ fonksiyonuna perfect parametresi eklemediysen
        # sadece width ve height gönder. Eklediysen perfect=config['PERFECT'] yaz.)
        generator = MazeGenerator(
            width=config['WIDTH'], 
            height=config['HEIGHT']
        )
        
        # 2. "42" desenini ekle ve labirenti üret
        generator.add_42()
        if config['PERFECT']:
            generator.generate_perfect_maze()
        else:
            generator.generate_pacman_maze()
        
        # 3. Geçici Çözüm Yolu (Dummy Path)
        # Gerçek BFS algoritmasını yazana kadar test için sahte bir yol gönderiyoruz.
        # Bu sayede dosya hatasız oluşturulacak.
        dummy_path = ["E", "E", "S", "W"] 
        
        # 4. Dosyaya kaydet
        save_maze_to_file(
            maze_grid=generator.grid, 
            filepath=config['OUTPUT_FILE'], 
            entry=config['ENTRY'], 
            exit=config['EXIT'], 
            path=dummy_path
        )

    except ValueError as e:
        print(e)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
