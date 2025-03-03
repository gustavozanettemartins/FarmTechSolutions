import sys
import os
import math
from operator import index
from typing import List
import json
import re
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QListWidgetItem
from PyQt6.QtWidgets import QMainWindow
import pandas as pd
import numpy as np
import pyqtgraph as pg
from data import *
from utils import *

DATA_PATH = "data/data.json"


# Efetuar mudança no cálculo para que ele coloque vetores também na linha 0, só está começando após o 0


class MainWindow(QMainWindow, Ui_FarmTechWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.plotWidget = None
        self.config_plot()
        self.but_calcular.clicked.connect(self.calculate_layout)
        self.cb_tipo_produto.currentIndexChanged.connect(self.tipo_produto_changed)
        self.total_plantas = 0
        self.but_insumo_add.clicked.connect(self.insumo_add)
        self.but_insumo_del.clicked.connect(self.insumo_del)
        self.cb_tipo_insumo_load()

    def cb_tipo_insumo_load(self):
        try:
            _data = load_json(DATA_PATH).get("insumos")
            for key, value in _data.items():
                item = f"{key.capitalize()} ({value.get("composicao")})"
                self.cb_tipo_insumo.addItem(item)
        except Exception as e:
            print(e)

    def insumo_add(self):
        try:
            if self.cb_tipo_insumo.currentIndex() != 0:
                total_itens = self.list_insumos.count()
                for i in range(total_itens):
                    item = self.list_insumos.item(i)
                    if item.text() == self.cb_tipo_insumo.currentText():
                        self.cb_tipo_insumo.setCurrentIndex(0)
                        return
                self.list_insumos.addItem(self.cb_tipo_insumo.currentText())
                self.cb_tipo_insumo.setCurrentIndex(0)
        except Exception as e:
            print(e)

    def insumo_del(self):
        try:
            item_selecionado = self.list_insumos.currentRow()
            if item_selecionado >= 0:
                self.list_insumos.takeItem(item_selecionado)
        except Exception as e:
            print(e)

    def config_plot(self):
        try:
            layout = QVBoxLayout(self.widget_graph)
            self.plotWidget = pg.PlotWidget(self.widget_graph)
            layout.addWidget(self.plotWidget)
            self.plotWidget.setTitle(f"Layout de Plantio")
            self.plotWidget.setLabel('bottom', 'Comprimento (m)')
            self.plotWidget.setLabel('left', 'Largura (m)')
        except Exception as e:
            print(e)

    def clear_graph(self):
        try:
            self.plotWidget.clear()
            self.plotWidget.setTitle(f"Layout de Plantio")
            self.le_largura.setText("")
            self.le_comprimento.setText("")

        except Exception as e:
                print(e)

    def tipo_produto_changed(self):
        try:
            self.clear_graph()

            if self.cb_tipo_produto.currentIndex() == 0:
                self.le_esp_l.setText("")
                self.le_esp_p.setText("")
            else:
                _data = load_json(DATA_PATH).get("plantas").get(self.cb_tipo_produto.currentText().lower())
                print(_data)
                self.le_esp_l.setText(str(_data.get("espacamento_linha")))
                self.le_esp_p.setText(str(_data.get("espacamento_planta")))
        except Exception as e:
            print(e)

    def get_list_insumos(self) -> list[str] | None:
        try:
            _data = list()
            total_itens = self.list_insumos.count()
            for i in range(total_itens):
                _data.append(self.list_insumos.item(i).text())
            return _data
        except Exception as e:
            print(e)

    @staticmethod
    def get_ha_area(x, y):
        try:
            area = x * y
            return area/10000
        except Exception as e:
            print(e)

    def get_insumo_kg(self, x, y, insumo):
        try:
            qtd_min, qtd_comp = (insumo.get('recomendacao_min').get(self.cb_tipo_produto.currentText().lower()),
                                 insumo.get('quantidade'))
            ha = self.get_ha_area(x, y)
            print(ha)
            qtd_insumo = qtd_min * ha
            return qtd_insumo / qtd_comp
        except Exception as e:
            print(e)

    def set_hud(self):
        try:
            # PARTE 1

            self.l_tipo_produto.setText(self.cb_tipo_produto.currentText())
            self.l_comprimento.setText(self.le_comprimento.text())
            self.l_largura.setText(self.le_largura.text())
            x, y = self.get_le_c_l()
            self.l_area.setText(str(x * y))
            _item = self.cb_tipo_produto.currentText().lower()
            _data = load_json(DATA_PATH).get("plantas").get(_item)
            esp_l, esp_p = self.get_le_esp()

            _comprimento, _largura = self.get_le_c_l()
            num_linhas = int(_largura // esp_l)
            self.l_esp_l.setText(str(esp_l))
            self.l_esp_p.setText(str(esp_p))
            self.l_qtd_linhas.setText(str(num_linhas))

            if self.total_plantas > 0:
                self.l_qtd_plantas.setText(str(self.total_plantas))

            # PARTE 2
            _data_insumos = self.get_list_insumos()
            if len(_data_insumos) > 0:
                _data = load_json(DATA_PATH).get("insumos")
                print(_data)
                _obj = {
                    0: [self.l_insumo_0, self.l_insumo_comp_0, self.l_insumo_min_0, self.l_insumo_qtd_0],
                    1: [self.l_insumo_1, self.l_insumo_comp_1, self.l_insumo_min_1, self.l_insumo_qtd_1]
                }
                for k, v in enumerate(_data_insumos):
                    _insumo = _data.get(re.match(r"\w+", v).group(0).lower())
                    _obj[k][0].setText(re.match(r"\w+", v).group(0).capitalize())
                    _obj[k][1].setText(f"{_insumo.get('composicao')} ({_insumo.get('quantidade') * 100}%)")
                    _obj[k][2].setText(str(
                        _insumo.get("recomendacao_min").get(self.cb_tipo_produto.currentText().lower())
                    ))
                    _obj[k][3].setText(str(round(self.get_insumo_kg(x, y, _insumo), 2)))

        except Exception as e:
            print(e)

    def plot_graph(self, value):
        try:
            self.plotWidget.setTitle(f"Layout de Plantio para {self.cb_tipo_produto.currentText().capitalize()}")
            self.set_hud()
        except:
            ...

    def get_le_c_l(self):
        try:
            if self.le_comprimento.text().replace(" ", "") == "" or self.le_largura.text().replace(" ", "") == "":
                raise ValueError("Comprimento ou largura vazio.")
            if float(self.le_comprimento.text()) > 0 and float(self.le_largura.text()) > 0:
                if float(self.le_comprimento.text()) <= 5000 and float(self.le_largura.text()) <= 5000:
                    return float(self.le_comprimento.text()), float(self.le_largura.text())
                else:
                    raise ValueError("Comprimento ou largura precisam ser menores que 5000.")
            else:
                raise ValueError("Comprimento ou largura inválido.")
        except Exception as e:
            return e

    def get_le_esp(self):
        try:
            if self.le_esp_p.text().replace(" ", "") == "" or self.le_esp_l.text().replace(" ", "") == "":
                raise ValueError("Espaçamento vazio.")
            if float(self.le_esp_p.text()) > 0 and float(self.le_esp_l.text()) > 0:
                if float(self.le_esp_l.text()) >= float(self.le_esp_p.text()):
                    return float(self.le_esp_p.text()), float(self.le_esp_l.text())
                else:
                    raise ValueError("Espaçamento linha maior ou igual ao espaçamento planta.")
            else:
                raise ValueError("Espaçamento inválido.")
        except Exception as e:
            print(e)

    def calculate_layout(self):
        try:
            if self.cb_tipo_produto.currentText() != "Selecionar":
                _item = self.cb_tipo_produto.currentText().lower()
                _data = load_json(DATA_PATH).get("plantas").get(_item)
                esp_l, esp_p = self.get_le_esp()

                _comprimento, _largura = self.get_le_c_l()
                num_linhas = int(_largura // esp_l)
                num_plantas_por_linha = int(_comprimento // esp_p)
                values = {
                    "num_linhas": num_linhas,
                    "num_plantas_por_linha": num_plantas_por_linha,
                    "esp_l": esp_l,
                    "esp_p": esp_p,
                    "produto": self.cb_tipo_produto.currentText(),
                    "comprimento": _comprimento,
                    "largura": _largura,
                    "cor": _data.get("cor")
                }
                self.th = GraphThread(self, values)
                self.th.finished.connect(self.plot_graph)
                self.th.start()

        except Exception as error:
            print(error)
            self.clear_graph()
            self.cb_tipo_produto.setCurrentIndex(0)


class GraphThread(QThread):
    finished = pyqtSignal(str)

    def __init__(self, _window: MainWindow, _data: dict):
        QThread.__init__(self)
        self.my_window = _window
        self.data = _data

    def export_csv(self, _data):
        from datetime import datetime

        try:
            df = pd.DataFrame(_data, columns=["x", "y"], index=range(len(_data)))
            df['linha'] = df['y'].astype('category').cat.codes + 1
            date_str = datetime.now().strftime('%Y%m%d%H%M%S')
            df.to_csv(
                f"layout_{self.my_window.cb_tipo_produto.currentText().lower()}_{date_str}.csv",
                index=False)

            print("Arquivo salvo com sucesso.")
        except Exception as e:
            print(e)

    def run(self):
        try:
            if self.my_window.plotWidget is not None:
                self.my_window.plotWidget.clear()
                num_plantas_por_linha = self.data.get("num_plantas_por_linha")
                num_linhas = self.data.get("num_linhas")
                esp_p = self.data.get("esp_p")  # Espaçamento entre plantas
                esp_l = self.data.get("esp_l")  # Espaçamento entre linhas

                # Gera os valores de x e y
                x_vals = np.arange(0, num_plantas_por_linha + 1) * esp_p
                y_vals = np.arange(0, num_linhas + 1) * esp_l

                # Cria as matrizes 2D de coordenadas
                x_items, y_items = np.meshgrid(x_vals, y_vals)  # shapes: (num_linhas, num_plantas_por_linha)

                # Verifica a quantidade total de pontos
                num_rows, num_cols = x_items.shape
                total_points = num_rows * num_cols

                self.my_window.total_plantas = total_points

                # Define o máximo de pontos desejado
                max_points = 100_000

                if total_points > max_points:
                    # Calcula fator de redução baseado na raiz quadrada da razão
                    # (pois estamos reduzindo em duas dimensões)
                    factor = int(math.ceil(math.sqrt(total_points / max_points)))

                    # Subamostra em cada dimensão para reduzir o total de pontos
                    x_items = x_items[::factor, ::factor]
                    y_items = y_items[::factor, ::factor]

                # Converte as matrizes 2D subamostradas em um array de pares (x, y), cada item é um vetor da planta
                graph_layout_data = np.column_stack((x_items.ravel(), y_items.ravel()))
                
                if self.my_window.cb_exportar.isChecked():
                    self.export_csv(graph_layout_data)

                # Se você quiser separar x e y, basta indexar as colunas
                x_coords, y_coords = graph_layout_data[:, 0], graph_layout_data[:, 1]

                self.my_window.plotWidget.setXRange(0, self.data.get("comprimento"))
                self.my_window.plotWidget.setYRange(0, self.data.get("largura"))
                scatter = pg.ScatterPlotItem(
                    x=x_coords,
                    y=y_coords,
                    pen=pg.mkPen(None),
                    brush=pg.mkBrush(self.data.get("cor")),
                    size=5,
                    name=self.data.get("produto")
                )

                self.my_window.plotWidget.addItem(scatter)
                self.my_window.plotWidget.showGrid(x=True, y=True)
                self.finished.emit("fim")
        except Exception as e:
            print(e)





def main() -> None:
    try:
        app = QApplication(sys.argv)
        app.setStyle('Fusion')
        gui = MainWindow()
        gui.show()
        sys.exit(app.exec())
    except Exception as e:
        # # logging.error(e)
        # err = ErrorDialog(e)
        # err.exec()
        print(e)


if __name__ == '__main__':
    main()