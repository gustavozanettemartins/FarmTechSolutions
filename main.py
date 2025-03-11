from data import get_data, remover_planta, update_data


def add_planta():
    from data import adicionar_planta

    name = input("Digite o nome da planta: ")
    values = dict()

    try:
        adicionar_planta(name, values)
        print(get_data())
    except Exception as e:
        print(e)

def rm_planta():
    from data import adicionar_planta

    name = input("Digite o nome da planta: ").lower()

    try:
        remover_planta(name)
        print(get_data())
    except Exception as e:
        print(e)

def test_menu():
    from utils import extract_numbers

    while True:
        try:
            print(f"\n----MENU PLANTAS--------------------\n1. Add Planta\n2. Del Planta\n0. Voltar")
            response = input("Digite a opção: ")

            if extract_numbers(response).replace(' ', '') != "":
                option = extract_numbers(response).replace(' ', '')

                if option == "1":
                    add_planta()
                elif option == "2":
                    rm_planta()
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
            print(f"\n----MENU PRINCIPAL--------------------\n1. Plantas\n9. Salvar Dados\n0. Sair")
            response = input("Digite a opção: ")

            if extract_numbers(response).replace(' ', '') != "":
                option = extract_numbers(response).replace(' ', '')

                if option == "1":
                    test_menu()
                elif option == "9":
                    update_data()
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
