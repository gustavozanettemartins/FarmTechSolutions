from data import *


def main():
    print(get_data())
    adicionar_planta("Melancia", {"esp_planta": 0.9, "esp_linha": 0.8, "tipo_figura_geom": ["quadrado"]})
    print(get_data())
    remover_planta("Melancia")
    print(get_data())

if __name__ == '__main__':
    main()
