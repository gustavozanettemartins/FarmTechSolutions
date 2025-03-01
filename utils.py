def load_json(path: str):
    import json

    try:
        with open(path, "r", encoding="utf-8") as arquivo:
            data = json.load(arquivo)
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"Arquivo {path} não encontrado.")