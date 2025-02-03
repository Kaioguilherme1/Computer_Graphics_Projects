import math
from time import sleep

def equacao_parametrica(app, centro, extremidade, velocidade, cor='red'):
    """
    Desenha um círculo usando a equação parametrica:
    x = xc + raio * cos(π * t / 180)
    y = yc + raio * sin(π * t / 180)

    :param centro: Tupla (xc, yc) representando o centro do círculo.
    :param extremidade: Tupla (x, y) representando um ponto na extremidade do círculo.
    :param cor: Cor fictícia para os "pixels".
    :return: Lista de pontos calculados.
    """
    # Coordenadas do centro (xc, yc)
    xc, yc = centro

    # Coordenadas da extremidade (x, y)
    x_ext, y_ext = extremidade

    # Calcula o raio (r) usando a distância Euclidiana entre os dois pontos
    raio = math.sqrt((x_ext - xc) ** 2 + (y_ext - yc) ** 2)

    x = round(xc + raio)
    y = yc
    # Loop para t de 1 até 360 graus (ângulo em graus)
    for t in range(1, 361):
        # Converte t para radianos
        angulo = math.pi * t / 180  # π * t / 180

        app.color_pixel(x, y, cor)
        # Calcula x e y usando a equação paramétrica
        x = round(xc + raio * math.cos(angulo))
        y = round(yc + raio * math.sin(angulo))
        if velocidade < 100:
            sleep((100 - velocidade)/10000)

