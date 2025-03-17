import os
from time import sleep
from data import get_data, remover_planta, update_data
from utils import extract_numbers

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

        name = plantas[int(extract_numbers(response))]
        remover_planta(name)

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

def select_planta(show_info=False):
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
                if not show_info:
                    edit_planta(plantas[response], get_data().get("plantas").get(plantas[response]))
                else:
                    name = plantas[response]
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
    ...

def rm_insumo():
    ...

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

def select_insumo(show_info=False):
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
                if not show_info:
                    edit_insumo(insumos[response], get_data().get("insumos").get(insumos[response]))
                else:
                    name = insumos[response]
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

def layout_menu():
    from utils import extract_numbers

    while True:
        try:
            limpar_tela()
            print(f"\n----MENU CÁLCULO--------------------\n1. Iniciar\n0. Voltar")
            response = input("Digite a opção: ")

            if extract_numbers(response).replace(' ', '') != "":
                option = extract_numbers(response).replace(' ', '')

                if option == "1":
                    ...
                elif option == "2":
                    ...
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
