__all__ = ['get_data', 'update_data']

import os
from typing import Dict


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, 'data.json')


def get_data() -> Dict[str, Dict[str, int]]:
    from utils import load_json

    return load_json(DATA_PATH)

def update_data(value) -> Dict[str, Dict[str, int]]:
    from utils import save_json

    return save_json(DATA_PATH, value)
