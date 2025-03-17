import os
import math
from time import sleep
from datetime import datetime
from data import get_data, remover_planta, update_data
from utils import extract_numbers
import numpy as np

REGISTROS = {}
BASE, ALTURA = 0, 0
PLANTA_SELECIONADA = None
INSUMOS_SELECIONADOS = list()
INSUMOS_DATA = dict()
NUM_LINHAS, NUM_PLANTAS_LINHA = 0, 0

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def add_planta():
    from data import adicionar_planta

    name = input("Digite o nome da planta, ou 0 para voltar: ").lower()

    if name == "0":
        return

    esp_linhas = input("Digite o espaçamento entre linhas: ")
    esp_plantas = input("Digite o espaçamento entre plantas: ")
    tipo_figura_geom = input("Digite o tipo de figura geométrica: ")
    values = {"esp_linhas": esp_linhas, "esp_plantas": esp_plantas, "tipo_figura_geom": [tipo_figura_geom]}

    try:
        adicionar_planta(name, values)
        print(get_data())
    except Exception as e:
        print(e)

def rm_planta():
    try:
        print(f"\n----REMOVER PLANTA--------------------\n")

        plantas = [k for k in get_data().get("plantas")]
        for i in range(len(plantas)):
            print(f"{i + 1}. {plantas[i]}")
        print(f"0. Voltar")

        response = input("Digite a opção: ")

        if response == "0":
            return

        response = int(extract_numbers(response)) - 1
        name = plantas[response]

        if 0 <= response < len(plantas):
            remover_planta(name)
        else:
            print("Opção inválida!")
            sleep(1)

    except Exception as e:
        print(e)

def edit_planta(name: str, planta: dict):
    while True:
        try:
            limpar_tela()
            if planta != get_data().get("plantas").get(name):
                planta = get_data().get("plantas").get(name)
                print("Planta Atualizada")
                sleep(1)

            print(f"\n----EDITAR '{name.upper()}'--------------------\n")
            print(f"1. Nome: {name}\n"
                  f"2. Espaçamento entre linhas: {planta.get('esp_linha')}\n"
                  f"3. Espaçamento entre plantas: {planta.get('esp_planta')}\n"
                  f"4. Figura Geométrica: {planta.get('tipo_figura_geom')}")
            print(f"0. Voltar\n")
            response = input("Digite a opção: ")

            if response == "0":
                return

            elif response == "1":
                value = input(f"Digite o nome: ")

                if not get_data().get("plantas").get(value):
                    get_data()["plantas"][value] = get_data()["plantas"].pop(name)
                    name = value
                    print(f"Nome atualizado com sucesso!")
                    sleep(1)
                else:
                    raise ValueError("Planta com este nome já existe")

            elif response == "2":
                value = input(f"Espaçamento entre linhas: ")
                if extract_numbers(value).replace(" ", "").isnumeric():
                    planta["esp_linha"] = float(extract_numbers(value))
                else:
                    raise ValueError("Precisa ser um número")

            elif response == "3":
                value = input(f"Espaçamento entre plantas: ")
                if extract_numbers(value).replace(" ", "").isnumeric():
                    planta["esp_planta"] = float(extract_numbers(value))
                else:
                    raise ValueError("Precisa ser um número")

            elif response == "4":
                value = input(f"Figura Geométrica(quadrado, retangulo ou triangulo): ")
                if value in ["quadrado", "retangulo", "triangulo"]:
                    planta["tipo_figura_geom"] = value
                else:
                    raise ValueError("Figura não permitida")

        except Exception as e:
            print(e)
            sleep(1)

def select_planta(show_info=False, get_planta=False):
    try:
        while True:
            limpar_tela()
            print(f"\n----SELECIONAR PLANTA--------------------\n")

            plantas = [k for k in get_data().get("plantas")]
            for i in range(len(plantas)):
                print(f"{i + 1}. {plantas[i]}")
            print(f"0. Voltar\n")

            response = input("Digite a opção: ")

            if response == "0":
                return
            response = int(extract_numbers(response)) - 1
            if 0 <= response < len(plantas):
                if not show_info and not get_planta:
                    edit_planta(plantas[response], get_data().get("plantas").get(plantas[response]))
                else:
                    name = plantas[response]
                    if get_planta:
                        return name
                    planta = get_data().get("plantas").get(plantas[response])
                    print(f"\n1. Nome: {name}\n"
                          f"2. Espaçamento entre linhas: {planta.get('esp_linha')}\n"
                          f"3. Espaçamento entre plantas: {planta.get('esp_planta')}\n"
                          f"4. Figura Geométrica: {planta.get('tipo_figura_geom')}")
                    input("\nPressione Enter para continuar...")
            else:
                print("Opção inválida!")
                sleep(1)
    except Exception as e:
        print(e)

def plantas_menu():
    from utils import extract_numbers

    while True:
        try:
            limpar_tela()
            print(f"\n----MENU PLANTAS--------------------\n\n"
                  f"1. Adicionar Planta\n"
                  f"2. Remover Planta\n"
                  f"3. Alterar Planta\n"
                  f"4. Plantas Cadastradas\n"
                  f"0. Voltar\n")

            response = input("Digite a opção: ")

            if extract_numbers(response).replace(' ', '') != "":
                option = extract_numbers(response).replace(' ', '')

                if option == "1":
                    add_planta()
                elif option == "2":
                    rm_planta()
                elif option == "3":
                    select_planta()
                elif option == "4":
                    select_planta(True)
                elif option == "0":
                    break
            else:
                raise ValueError("A entrada precisa ser um número.")

        except Exception as e:
            print(e)
            sleep(1)

def add_insumo():
    from data import adicionar_insumo

    name = input("Digite o nome do insumo, ou 0 para voltar: ").lower()

    if name == "0":
        return

    comp = input("Digite a composição: ")
    quantidade = input("Digite a quantidade (%) em número decimal: ")
    input_values = input("Digite o nome da planta e a recomendação mínima entre vírgula. Ex: milho, 60: ")
    input_values = input_values.split(", ")

    if len(input_values) > 2:
        raise ValueError("Formato recomendação mínima errado!")

    elif not extract_numbers(input_values[1]).replace(" ", "").isnumeric():
        raise ValueError("Valor precisa ser um número!")

    else:
        values = {
            "comp": comp,
            "quantidade": quantidade,
            "min": {input_values[0]: float(extract_numbers(input_values[1]))}
        }

    try:
        adicionar_insumo(name, values)

    except Exception as e:
        print(e)
        sleep(1)

def rm_insumo():
    from data import remover_insumo

    try:
        print(f"\n----REMOVER INSUMO--------------------\n")

        insumos = [k for k in get_data().get("insumos")]
        for i in range(len(insumos)):
            print(f"{i + 1}. {insumos[i]}")
        print(f"0. Voltar")

        response = input("Digite a opção: ")

        if response == "0":
            return

        response = int(extract_numbers(response)) - 1
        name = insumos[response]

        if 0 <= response < len(insumos):
            remover_insumo(name)
        else:
            print("Opção inválida!")
            sleep(1)

    except Exception as e:
        print(e)

def edit_insumo(name: str, insumo: dict):
    while True:
        try:
            limpar_tela()
            if insumo != get_data().get("insumos").get(name):
                insumo = get_data().get("insumos").get(name)
                print("Insumos Atualizado")
                sleep(1)

            print(f"\n----EDITAR '{name.upper()}'--------------------\n")
            print(f"1. Nome: {name}\n"
                  f"2. Composição: {insumo.get('comp')}\n"
                  f"3. Quantidade (%): {insumo.get('quantidade')}\n"
                  f"4. Recomendação Mínima (kg/ha): {insumo.get('min')}")
            print(f"0. Voltar\n")
            response = input("Digite a opção: ")

            if response == "0":
                return

            elif response == "1":
                value = input(f"Digite o nome: ")

                if not get_data().get("insumos").get(value):
                    get_data()["insumos"][value] = get_data()["insumos"].pop(name)
                    name = value
                    print(f"Nome atualizado com sucesso!")
                    sleep(1)
                else:
                    raise ValueError("Insumo com este nome já existe")

            elif response == "2":
                value = input(f"Composição: ")
                insumo["comp"] = value

            elif response == "3":
                print("OBS: Quantidade deve ser em número decimal, ex: 18% = 0.18")
                value = input(f"Quantidade (%): ")
                if extract_numbers(value).replace(" ", "").isnumeric():
                    if float(extract_numbers(value)) > 1:
                        insumo["quantidade"] = float(extract_numbers(value)) / 100
                    else:
                        insumo["quantidade"] = float(extract_numbers(value))
                else:
                    raise ValueError("Precisa ser um número")

            elif response == "4":
                try:
                    while True:
                        limpar_tela()

                        print(f"\n----EDITAR QTD MIN--------------------\n")
                        plantas = [k for k in insumo.get("min")]
                        for i in range(len(plantas)):
                            print(f"{i + 1}. {plantas[i]}")
                        print(f"0. Voltar\n")

                        response = input("Digite a opção: ")

                        if response == "0":
                            break
                        response = int(extract_numbers(response)) - 1
                        if 0 <= response < len(plantas):
                            value = input(f"Recomendação Mínima (kg/ha): ")
                            if extract_numbers(value).replace(" ", "").isnumeric():
                                insumo["min"][plantas[response]] = float(extract_numbers(value))
                                break
                            else:
                                raise ValueError("Precisa ser um número")
                        else:
                            print("Opção inválida!")
                            sleep(1)
                except Exception as e:
                    print(e)
                    sleep(1)

        except Exception as e:
            print(e)
            sleep(1)

def select_insumo(show_info=False, get_insumo=False):
    try:
        while True:
            limpar_tela()
            print(f"\n----SELECIONAR INSUMO--------------------\n")

            insumos = [k for k in get_data().get("insumos")]
            for i in range(len(insumos)):
                print(f"{i + 1}. {insumos[i]}")
            print(f"0. Voltar\n")

            response = input("Digite a opção: ")

            if response == "0":
                return
            response = int(extract_numbers(response)) - 1
            if 0 <= response < len(insumos):
                if not show_info and not get_insumo:
                    edit_insumo(insumos[response], get_data().get("insumos").get(insumos[response]))
                else:
                    name = insumos[response]
                    if get_insumo:
                        return name
                    insumo = get_data().get("insumos").get(insumos[response])
                    print(f"\n1. Nome: {name}\n"
                          f"2. Composição: {insumo.get('comp')}\n"
                          f"3. Quantidade (%): {insumo.get('quantidade')}\n"
                          f"4. Recomendação Mínima (kg/ha): {insumo.get('min')}")
                    input("\nPressione Enter para continuar...")
            else:
                print("Opção inválida!")
                sleep(1)
    except Exception as e:
        print(e)

def insumos_menu():
    from utils import extract_numbers

    while True:
        try:
            limpar_tela()
            print(f"\n----MENU INSUMOS--------------------\n\n"
                  f"1. Adicionar Insumo\n"
                  f"2. Remover Insumo\n"
                  f"3. Alterar Insumo\n"
                  f"4. Insumos Cadastrados\n"
                  f"0. Voltar\n")

            response = input("Digite a opção: ")

            if extract_numbers(response).replace(' ', '') != "":
                option = extract_numbers(response).replace(' ', '')

                if option == "1":
                    add_insumo()
                elif option == "2":
                    rm_insumo()
                elif option == "3":
                    select_insumo()
                elif option == "4":
                    select_insumo(True)
                elif option == "0":
                    break
            else:
                raise ValueError("A entrada precisa ser um número.")

        except Exception as e:
            print(e)
            sleep(1)

def get_ha_area(x, y):
    try:
        area = x * y
        return area / 10000

    except Exception as e:
        print(e)

def converter_g_m_para_ml_m(fertilizante_g_m, densidade_g_ml):
    """
    Converte a quantidade de fertilizante de g/m para ml/m.
    :param fertilizante_g_m: Quantidade de fertilizante em gramas por metro linear (g/m).
    :param densidade_g_ml: Densidade do fertilizante em gramas por mililitro (g/mL).
    :return: Quantidade de fertilizante em mililitros por metro linear (mL/m).
    """
    if densidade_g_ml > 0:
        return fertilizante_g_m / densidade_g_ml
    else:
        return 0

def calcular_fertilizante_por_metro():
    global INSUMOS_DATA

    try:
        for k, v in INSUMOS_DATA.items():
            fertilizante_g = v["kg/ha"] * 1000
            total_plantas = NUM_LINHAS * NUM_PLANTAS_LINHA
            if total_plantas > 0:
                fertilizante_por_planta = fertilizante_g / total_plantas
            else:
                fertilizante_por_planta = 0
            comprimento_total_linhas = NUM_LINHAS * ALTURA
            if comprimento_total_linhas > 0:
                fertilizante_por_metro_linear = fertilizante_g / comprimento_total_linhas
            else:
                fertilizante_por_metro_linear = 0

            INSUMOS_DATA[k]["g_por_planta (g)"] = fertilizante_por_planta
            INSUMOS_DATA[k]["g_por_metro_linear (g/m)"] = fertilizante_por_metro_linear
            INSUMOS_DATA[k]["ml_por_metro_linear (mL/m)"] = converter_g_m_para_ml_m(
                fertilizante_por_metro_linear, get_data().get("insumos").get(k).get("densidade")
            )
    except Exception as e:
        print(e)
        sleep(1)

def get_insumo_kg():
    global INSUMOS_DATA

    try:
        if BASE > 0 and ALTURA > 0 and PLANTA_SELECIONADA is not None and len(INSUMOS_SELECIONADOS) > 0:
            data = dict()
            for i in INSUMOS_SELECIONADOS:
                insumo = get_data().get("insumos").get(i)
                qtd_min, qtd_comp = insumo.get("min").get(PLANTA_SELECIONADA), insumo.get("quantidade")
                ha = get_ha_area(BASE, ALTURA)
                qtd_insumo = qtd_min * ha

                data[i] = {"kg/ha": qtd_insumo / qtd_comp}

            INSUMOS_DATA = data
            calcular_fertilizante_por_metro()
    except Exception as e:
        print(e)
        sleep(1)

def add_registro(_data):
    global REGISTROS

    try:
        if len(REGISTROS) == 0:
            REGISTROS[PLANTA_SELECIONADA] = {0: {"time": datetime.now(), "data": _data}}
        else:
            if not REGISTROS.get(PLANTA_SELECIONADA):
                REGISTROS[PLANTA_SELECIONADA] = {0: {"time": datetime.now(), "data": _data}}
            else:
                REGISTROS[PLANTA_SELECIONADA][len(REGISTROS[PLANTA_SELECIONADA])] = {
                    "time": datetime.now(), "data": _data
                }
    except Exception as e:
        print(e)

def get_vetores():
    global NUM_LINHAS, NUM_PLANTAS_LINHA
    try:
        if PLANTA_SELECIONADA and BASE > 0 and ALTURA > 0:
            _data = get_data().get("plantas").get(PLANTA_SELECIONADA)
            esp_l, esp_p = _data.get("esp_linha"), _data.get("esp_planta")

            NUM_LINHAS = int(ALTURA // esp_l)
            NUM_PLANTAS_LINHA = int(BASE // esp_p)
            x_vals = np.arange(0, NUM_PLANTAS_LINHA + 1) * esp_p
            y_vals = np.arange(0, NUM_LINHAS + 1) * esp_l

            x_items, y_items = np.meshgrid(x_vals, y_vals)  # shapes: (num_linhas, num_plantas_por_linha)

            graph_layout_data = np.column_stack((x_items.ravel(), y_items.ravel()))
            add_registro(graph_layout_data)
            get_insumo_kg()
    except Exception as e:
        print(e)

def iniciar_calc():
    try:
        global BASE, ALTURA, PLANTA_SELECIONADA, INSUMOS_SELECIONADOS

        limpar_tela()
        print(f"\n----INICIAR CÁLCULO--------------------\n")

        base = input("Digite a base (m): ")
        if extract_numbers(base).replace(' ', '').isdigit():
            if abs(float(base)) > 0:
                BASE = abs(float(base))
            else:
                raise ValueError("Base precisa ser maior que 0")
        else:
            raise ValueError("Base precisa ser um número")

        altura = input("Digite a altura (m): ")
        if extract_numbers(altura).replace(' ', '').isdigit():
            if abs(float(altura)) > 0:
                ALTURA = abs(float(altura))
            else:
                raise ValueError("Altura precisa ser maior que 0")
        else:
            raise ValueError("Altura precisa ser um número")

        PLANTA_SELECIONADA = select_planta(get_planta=True)
        if PLANTA_SELECIONADA is None:
            raise ValueError("Planta precisa ser selecionada")
        insumos = list()

        while True:
            insumo = select_insumo(get_insumo=True)
            if insumo not in insumos and insumo is not None:
                insumos.append(insumo)

            limpar_tela()
            if len(insumos) < len(get_data().get("insumos")):
                print(f"\n------> Insumos Adicionados: {insumos} <--------")
                print("\nAdicionar mais insumos?\n\n1. Sim\n0. Não\n")
                response = input("Digite a opção: ")
                if response == "0":
                    break
            else:
                break

        INSUMOS_SELECIONADOS = insumos
        get_vetores()

    except Exception as e:
        print(e)
        sleep(1)

def select_registros():
    try:
        print(REGISTROS)
        print(NUM_LINHAS, NUM_PLANTAS_LINHA)
        input("\nPressione Enter para continuar...")
    except Exception as e:
        print(e)

def get_globals():
    try:
        print(BASE, ALTURA, PLANTA_SELECIONADA, INSUMOS_SELECIONADOS, INSUMOS_DATA, NUM_LINHAS, NUM_PLANTAS_LINHA)
        calcular_fertilizante_por_metro()
        input("\nPressione Enter para continuar...")
    except Exception as e:
        print(e)

def layout_menu():
    from utils import extract_numbers

    while True:
        try:
            limpar_tela()
            print(f"\n----MENU CÁLCULO--------------------\n\n1. Iniciar")
            if len(REGISTROS) > 0:
                print(f"2. Resultados Anteriores")
                print(f"3. Variáveis Globais")
            print(f"0. Voltar\n")
            response = input("Digite a opção: ")

            if extract_numbers(response).replace(' ', '') != "":
                option = extract_numbers(response).replace(' ', '')

                if option == "1":
                    iniciar_calc()
                elif option == "2" and len(REGISTROS) > 0:
                    select_registros()
                elif option == "3" and len(REGISTROS) > 0:
                    get_globals()
                elif option == "0":
                    break
            else:
                raise ValueError("A entrada precisa ser um número.")

        except Exception as e:
            print(e)

def main_menu():
    from utils import extract_numbers

    while True:
        try:
            limpar_tela()
            print(f"\n----MENU PRINCIPAL--------------------\n\n"
                  f"1. Plantas\n"
                  f"2. Insumos\n"
                  f"3. Cálculo Plantio\n"
                  f"9. Salvar Dados\n"
                  f"0. Sair\n")
            response = input("Digite a opção: ")

            if extract_numbers(response).replace(' ', '') != "":
                option = extract_numbers(response).replace(' ', '')

                if option == "1":
                    plantas_menu()
                elif option == "2":
                    insumos_menu()
                elif option == "3":
                    layout_menu()
                elif option == "9":
                    update_data()
                    print("Dados Salvos!")
                    sleep(1)
                elif option == "0":
                    break
            else:
                raise ValueError("A entrada precisa ser um número.")
        except Exception as e:
            print(e)

def main():
    print(f"Bem vindo ao Sistema FarmTechSolutions")
    main_menu()



if __name__ == '__main__':
    main()
