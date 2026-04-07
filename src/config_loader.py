import json
from pathlib import Path

def load_config(config_path: str):
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Config not found: {config_path}")
    with open(path, 'r') as f:
        config = json.load(f)
    # Validaciones básicas
    required = ['watch_folder', 'destination_base', 'rules']
    for r in required:
        if r not in config:
            raise ValueError(f"Missing required config key: {r}")
    return config