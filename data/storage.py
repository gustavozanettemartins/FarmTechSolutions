__all__ = ['get_data', 'update_data', 'adicionar_planta', 'remover_planta', 'editar_planta', 'adicionar_insumo',
           'remover_insumo', 'editar_insumo']

import os
from typing import Dict
from utils import *


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, 'data.json')
DATA = load_json(DATA_PATH)

def get_data() -> dict:
    try:
        return DATA
    except Exception as e:
        print(e)
        return dict()

def update_data() -> Dict[str, Dict[str, int]]:
    try:
        return save_json(DATA_PATH, DATA)

    except Exception as e:
        print(e)
        return dict()


def adicionar_planta(name: str, values: dict):
    """
    Adiciona uma nova planta.

    :param name: Nome da planta.
    :param values: Dicionário contendo os dados da planta("esp_linha": float,
    "esp_planta": float, "tipo_figura_geom": list).
    :return: None
    """
    try:
        if isinstance(name, str):
            if name not in DATA.get("plantas"):
                DATA["plantas"][name] = values
            else:
                raise ValueError(f"Planta: {name} já existe!")
        else:
            raise ValueError(f"Planta: '{name}' precisa ser do tipo str!")

    except Exception as e:
        print(e)


def remover_planta(name: str):
    """
    Deleta uma planta.

    :param name: Nome da planta.
    :return: None
    """
    try:
        if isinstance(name, str):
            if name in DATA.get("plantas"):
                del DATA["plantas"][name]
            else:
                raise ValueError(f"Planta: {name} não existe!")
        else:
            raise ValueError(f"Planta: '{name}' precisa ser do tipo str!")

    except Exception as e:
        print(e)

def editar_planta(name: str, values: dict):
    """
        Edita uma planta.

        :param name: Nome da planta.
        :param values: Dicionário contendo os dados da planta a serem modificados.
        :return: None
        """
    try:
        print(name, values)
    except Exception as e:
        print(e)

def adicionar_insumo(name: str, values: dict):
    """
    Adiciona um novo insumo.

    :param name: Nome do insumo.
    :param values: Dicionário contendo os dados do insumo("comp": str,
    "quantidade": float, "min": dict).
    :return: None
    """
    try:
        if isinstance(name, str):
            if name not in DATA.get("insumos"):
                DATA["insumos"][name] = values
            else:
                raise ValueError(f"Insumo: {name} já existe!")
        else:
            raise ValueError(f"Insumo: '{name}' precisa ser do tipo str!")

    except Exception as e:
        print(e)


def remover_insumo(name: str):
    """
    Deleta um insumo.

    :param name: Nome do insumo.
    :return: None
    """
    try:
        if isinstance(name, str):
            if name in DATA.get("insumos"):
                del DATA["insumos"][name]
            else:
                raise ValueError(f"Insumo: {name} não existe!")
        else:
            raise ValueError(f"Insumo: '{name}' precisa ser do tipo str!")

    except Exception as e:
        print(e)

def editar_insumo(name: str, values: dict):
    """
        Edita um insumo.

        :param name: Nome do insumo.
        :param values: Dicionário contendo os dados do insumo a serem modificados.
        :return: None
        """
    try:
        print(name, values)
    except Exception as e:
        print(e)
