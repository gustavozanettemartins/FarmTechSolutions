__all__ = ['get_plantas']

DATA_PATH = "data.json"

def get_plantas():
    from ..utils import load_json

    return load_json(DATA_PATH)
