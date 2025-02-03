import math
from time import sleep


def bresenham_circunferencia(app, centro, extremidade, velocidade, cor='red'):
    """
    Algoritmo de rasterização de circunferência usando o método de Bresenham.
    Baseia-se na avaliação incremental com decisão baseada no parâmetro inicial.

    :param app: Instância da interface gráfica onde os pixels serão desenhados.
    :param centro: Coordenadas (xc, yc) do centro da circunferência.
    :param raio: Raio da circunferência.
    """

    xc, yc = centro

    # Coordenadas da extremidade (x, y)
    x_ext, y_ext = extremidade

    # Calcula o raio (r) usando a distância Euclidiana entre os dois pontos
    raio = math.sqrt((x_ext - xc) ** 2 + (y_ext - yc) ** 2)

    x = 0
    y = raio

    # Parâmetro inicial
    p = 1 - raio  # Correspondente a (5/4 - r) nos cálculos inteiros.

    # Desenhar os primeiros 8 pontos simétricos
    desenhar_pontos(app, xc, yc, x, y)

    # Enquanto x <= y (primeiro octante)
    while x < y:
        if p >= 0:
            # Caso em que o ponto está fora ou na mesma distância da circunferência
            y -= 1
            p = p + 2 * x - 2 * y + 5
        else:
            # Caso em que o ponto está dentro da circunferência
            p = p + 2 * x + 3
        x += 1

        # Desenhar os pontos baseados na simetria dos octantes
        desenhar_pontos(app, xc, yc, x, y)

        # Adicionar atraso baseado no controle da velocidade
        if velocidade < 100 and velocidade > 0:
            sleep((100 - velocidade) / 10000)  # Menor velocidade = maior atraso



def desenhar_pontos(app, xc, yc, x, y):
    """
    Desenha os oito pontos simétricos da circunferência, transladados para o centro.

    :param app: Instância da interface gráfica.
    :param xc: Coordenada X central da circunferência.
    :param yc: Coordenada Y central da circunferência.
    :param x: Coordenada X do ponto na borda.
    :param y: Coordenada Y do ponto na borda.
    """
    # Para cada ponto (x, y), desenhar os 8 simétricos
    app.color_pixel(xc + x, yc + y, 'red')  # Primeiro octante
    app.color_pixel(xc - x, yc + y, 'red')  # Segundo octante
    app.color_pixel(xc + x, yc - y, 'red')  # Terceiro octante
    app.color_pixel(xc - x, yc - y, 'red')  # Quarto octante
    app.color_pixel(xc + y, yc + x, 'red')  # Quinto octante
    app.color_pixel(xc - y, yc + x, 'red')  # Sexto octante
    app.color_pixel(xc + y, yc - x, 'red')  # Sétimo octante
    app.color_pixel(xc - y, yc - x, 'red')  # Oitavo octante