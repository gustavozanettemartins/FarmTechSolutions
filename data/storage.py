__all__ = ['get_plantas']

import os
from typing import Dict


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, 'data.json')


def get_plantas() -> Dict[str, Dict[str, int]]:
    from utils import load_json

    return load_json(DATA_PATH)
