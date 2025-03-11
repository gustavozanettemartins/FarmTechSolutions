__all__ = ['load_json', ]

import json

def load_json(path: str):
    """Carrega os dados de um arquivo JSON."""
    try:
        with open(path, "r", encoding="utf-8") as arquivo:
            data = json.load(arquivo)
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"Arquivo {path} não encontrado.")


def save_json(path: str, data: dict):
    """Salva os dados no arquivo JSON."""
    with open(path, "w", encoding="utf-8") as arquivo:
        json.dump(data, arquivo, indent=4, ensure_ascii=False)

def update_json(path: str, new_data: dict):
    """
    Atualiza um arquivo JSON adicionando ou modificando os valores existentes.

    :param path: Caminho do arquivo JSON.
    :param new_data: Dicionário com os novos dados a serem adicionados/modificados.
    """
    try:
        data = load_json(path)  # Carregar os dados existentes
    except FileNotFoundError:
        data = {}  # Se não existir, cria um dicionário vazio

    # Mescla os novos dados com os antigos
    data.update(new_data)

    save_json(path, data)  # Salva as alterações