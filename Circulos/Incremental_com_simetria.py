import math
from time import sleep


def incremental_com_simetria(app, centro, extremidade, velocidade, cor='red'):
    """
    Desenha um círculo utilizando um algoritmo incremental otimizado com simetria,
    desenhando os pixels diretamente na tela em tempo real.

    :param app: Objeto onde os pixels serão desenhados.
    :param centro: Tupla (xc, yc) representando o centro do círculo.
    :param extremidade: Tupla com a coordenada do ponto na extremidade.
    :param velocidade: Controle da velocidade de desenho (0 a 100).
    :param cor: Cor do círculo.
    """

    # Coordenadas da extremidade
    x_ext, y_ext = extremidade

    # Coordenadas do centro
    xc, yc = centro

    # Calcula o raio (r) usando a distância Euclidiana entre os dois pontos
    raio = int(math.sqrt((x_ext - xc) ** 2 + (y_ext - yc) ** 2))

    # Inicializa as coordenadas (primeiro ponto do círculo, no topo)
    x = 0
    y = raio

    # Inicializa a variável de decisão
    d = 1 - raio

    # Enquanto os pontos ainda estiverem no primeiro oitante (x <= y)
    while x <= y:
        # Desenha os pontos diretamente (8 octantes)
        desenhar_pontos_simetricos(app, xc, yc, x, y, cor)

        # Atraso baseado no controle de velocidade
        if velocidade < 100 and velocidade > 0:
            delay = (100 - velocidade) / 10000  # Quanto menor a velocidade, maior o atraso
            sleep(delay)

        # Atualiza o parâmetro de decisão `d` e os valores de x e y
        if d < 0:
            # Escolhe o próximo ponto horizontal (E)
            d += 2 * x + 3
        else:
            # Escolhe o próximo ponto diagonal (SE)
            d += 2 * (x - y) + 5
            y -= 1  # Reduz y ao escolher o ponto diagonal

        x += 1  # Incrementa x ao avançar


def desenhar_pontos_simetricos(app, xc, yc, x, y, cor):
    """
    Desenha diretamente os 8 pontos simétricos de um círculo dados xc, yc, x, y.

    :param app: Objeto onde os pixels serão desenhados.
    :param xc: Coordenada x do centro do círculo.
    :param yc: Coordenada y do centro do círculo.
    :param x: Coordenada x de um ponto no primeiro oitante.
    :param y: Coordenada y de um ponto no primeiro oitante.
    :param cor: Cor para desenhar os pontos.
    """
    # Primeiro oitante
    app.color_pixel(xc + x, yc + y, cor)
    # Segundo oitante
    app.color_pixel(xc + y, yc + x, cor)
    # Terceiro oitante
    app.color_pixel(xc - y, yc + x, cor)
    # Quarto oitante
    app.color_pixel(xc - x, yc + y, cor)
    # Quinto oitante
    app.color_pixel(xc - x, yc - y, cor)
    # Sexto oitante
    app.color_pixel(xc - y, yc - x, cor)
    # Sétimo oitante
    app.color_pixel(xc + y, yc - x, cor)
    # Oitavo oitante
    app.color_pixel(xc + x, yc - y, cor)