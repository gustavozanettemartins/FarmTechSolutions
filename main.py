from data import *
from utils import extract_numbers


def test_menu():
    while True:
        try:
            print(f"\n----MENU PLANTAS--------------------\n1. Add Planta\n2. Del Planta\n0. Voltar")
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
        while True:
            try:
                print(f"\n----MENU PRINCIPAL--------------------\n1. Plantas\n0. Sair")
                response = input("Digite a opção: ")

                if extract_numbers(response).replace(' ', '') != "":
                    option = extract_numbers(response).replace(' ', '')

                    if option == "1":
                        test_menu()
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
