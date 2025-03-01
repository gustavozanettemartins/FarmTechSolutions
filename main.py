import plotly.graph_objects as go


def calcular_ticks_eixo_x(comprimento):
    ...


def calcular_plantacao(cultura, comprimento, largura):
    """
    Calcula o layout da plantação com base no espaçamento recomendado para cada cultura.
    Retorna uma lista de coordenadas (x, y) representando a posição de cada planta.

    Espaçamentos recomendados (valores aproximados):
      Milho:  espaçamento entre linhas = 0.75 m, entre plantas = 0.20 m.
      Soja:   espaçamento entre linhas = 0.45 m, entre plantas = 0.075 m.
    """
    if cultura.lower() == 'milho':
        espacamento_linha = 0.75
        espacamento_planta = 0.20
    elif cultura.lower() == 'soja':
        espacamento_linha = 0.45
        espacamento_planta = 0.075
    else:
        print("Cultura não suportada para cálculo de plantação.")
        return []

    # Quantidade de linhas e de plantas por linha
    num_linhas = int(largura // espacamento_linha)
    num_plantas_por_linha = int(comprimento // espacamento_planta)

    layout = []
    # Gera as coordenadas (x, y) de cada planta
    for i in range(num_linhas):
        for j in range(num_plantas_por_linha):
            x = (j + 1) * espacamento_planta
            y = (i + 1) * espacamento_linha
            layout.append((x, y))
    return layout


def plotar_layout_plotly(layout, cultura, comprimento, largura):
    """
    Plota um scatter plot dos pontos de plantio usando Plotly.
    """
    # Extrai coordenadas X e Y
    print(len(layout))
    x_coords = [coord[0] for coord in layout]
    y_coords = [coord[1] for coord in layout]

    # Cria a figura
    fig = go.Figure()

    # Adiciona um trace de dispersão (scatter) somente com marcadores (sem linhas)
    fig.add_trace(go.Scatter(
        x=x_coords,
        y=y_coords,
        mode='markers',
        marker=dict(
            size=5,  # Ajuste o tamanho dos marcadores
            color='green'  # Cor dos marcadores
        ),
        name=f"Plantas de {cultura.capitalize()}"
    ))

    # Define o layout do gráfico (título, rótulos dos eixos etc.)
    fig.update_layout(
        title=f"Layout de Plantio para {cultura.capitalize()}",
        xaxis_title="Comprimento (m)",
        yaxis_title="Largura (m)",
        width=800,   # largura do gráfico em pixels
        height=600    # altura do gráfico em pixels
    )

    # Ajusta os limites dos eixos para refletir o tamanho da área
    fig.update_xaxes(range=[0, comprimento])
    fig.update_yaxes(range=[0, largura])

    # Se desejar remover a grid para destacar os pontos:
    # fig.update_xaxes(showgrid=False)
    # fig.update_yaxes(showgrid=False)

    # Exibe o gráfico
    fig.show()


def main():
    print("Cálculo do Layout da Plantação (usando Plotly)")
    cultura = input("Digite a cultura (milho ou soja): ").strip().lower()
    try:
        comprimento = float(input("Digite o comprimento da área (m): "))
        largura = float(input("Digite a largura da área (m): "))
    except ValueError:
        print("Valor inválido para as dimensões!")
        return

    layout = calcular_plantacao(cultura, comprimento, largura)
    if layout:
        print(f"\nForam calculadas {len(layout)} posições de plantas para a cultura '{cultura}'.")
        print("Exemplo das primeiras 5 coordenadas geradas:")
        for i, (x, y) in enumerate(layout[:5]):
            print(f"  Planta {i + 1}: x={x:.2f}, y={y:.2f}")

        # Gera o gráfico com Plotly
        plotar_layout_plotly(layout, cultura, comprimento, largura)
    else:
        print("Nenhuma posição de plantio calculada. Verifique os parâmetros.")


if __name__ == "__main__":
    main()
