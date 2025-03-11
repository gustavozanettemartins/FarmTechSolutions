__all__ = ['DATA', 'update_data', 'adicionar_planta', 'remover_planta']

import os
from typing import Dict
from utils import *


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, 'data.json')
DATA = load_json(DATA_PATH)


def update_data() -> Dict[str, Dict[str, int]]:
    try:
        return save_json(DATA_PATH, DATA)
    except Exception as e:
        print(e)
        return dict()


def adicionar_planta(name: str, values: Dict):
    """Adiciona uma nova planta ao JSON.

    :param name: Nome da planta.
    :param values: Dicionário contendo os dados da planta("esp_linha": float,
    "esp_planta": float, "tipo_figura_geom": list).
    """
    try:
        if isinstance(name, str):
            if name not in DATA.get("plantas"):
                DATA["plantas"][name] = values
                print(f"✅ Planta '{name}' adicionada com sucesso!")
                print(DATA)
            else:
                raise ValueError(f"Planta: {name} já existe!")
        else:
            raise ValueError(f"Planta: '{name}' precisa ser do tipo str!")

    except Exception as e:
        print(e)


def remover_planta(nome: str):
    try:
        """Remove uma planta do JSON."""
        data = load_json(DATA_PATH)

        if "plantas" in data and nome in data["plantas"]:
            del data["plantas"][nome]  # Remove a planta
            save_json(DATA_PATH, data)  # Salva as alterações
            print(f"❌ Planta '{nome}' removida com sucesso!")
        else:
            print(f"⚠️ Planta '{nome}' não encontrada.")
    except Exception as e:
        print(e)
