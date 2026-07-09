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

    required_keys = ['WIDTH', 'HEIGHT', 'ENTRY', 'EXIT', 'OUTPUT_FILE',
                     'PERFECT']

    for key in required_keys:
        if key not in raw_config:
            raise ValueError(f"Hata: '{key}' ayarı dosyada bulunamadı!")

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

        raise ValueError(f"Hata: Ayar dosyasında geçersiz tip var! {e}")

    return valid_config
