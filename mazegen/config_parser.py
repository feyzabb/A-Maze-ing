from typing import Dict, Any


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
                    print(f"Hatalı satır! -> {line}")
    except FileNotFoundError:
        print(f"Hata:'{filepath}' dosyası bulunamadı!"
              f"Varsayılan ayarlar kullanılacak")

    return config_data


def validate_config(raw_config: Dict[str, Any]) -> Dict[str, Any]:
    valid_config: Dict[str, Any] = {}
    required_keys = ['WIDTH', 'HEIGHT', 'ENTRY']

