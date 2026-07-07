from typing import Dict, Any


def read_config(filepath: str) -> Dict[str, Any]:
    config_data:Dict[str, Any] = {}

    try:
        with open(filepath,'r') as file:
            for line in file:
                line = line.strip()

            if not line:
                continue

            if '=' in line:
                key,value = line.split('=',1)
                config_data[key.strip()] = value.strip()
            
