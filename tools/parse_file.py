from pathlib import Path
from typing import Dict

import yaml


def parse_yaml(file_path: Path) -> Dict:
    with open(file_path, mode="r", encoding="utf-8") as file:
        return yaml.safe_load(file)
