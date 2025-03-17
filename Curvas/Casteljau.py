from time import sleep
import numpy as np


def subdivision(P0, P1, P2, P3):
    """
    Calcula os pontos intermediários da curva de Bézier usando o método de De Casteljau.
    Retorna os novos pontos para subdivisão.
    """
    P0xD1 = (P0 + P1) / 2
    P1xD1 = (P1 + P2) / 2
    P2xD1 = (P2 + P3) / 2

    P0xD2 = (P0xD1 + P1xD1) / 2
    P1xD2 = (P1xD1 + P2xD1) / 2

    P0xD3 = (P0xD2 + P1xD2) / 2

    return P0xD1, P2xD1, P0xD2, P1xD2, P0xD3


def casteljau_recursivo(pontos_controle, t, curve_points):
    """
    Algoritmo de De Casteljau recursivo para calcular pontos da curva de Bézier para um número dinâmico de pontos.
    """
    if len(pontos_controle) == 1:
        curve_points.append(pontos_controle[0])
        return
    novos_pontos = [(1 - t) * pontos_controle[i] + t * pontos_controle[i + 1] for i in range(len(pontos_controle) - 1)]
    casteljau_recursivo(novos_pontos, t, curve_points)


def desenhar_curva_casteljau(app, pontos_controle, num_pontos=100, constante_t=0, velocidade=100, cor='red'):
    """
    Desenha a curva de Bézier utilizando o algoritmo de De Casteljau.
    """
    if len(pontos_controle) < 2:
        raise ValueError("São necessários pelo menos dois pontos de controle para desenhar a curva.")

    curva = []
    for i in range(num_pontos + 1):
        t = i / num_pontos if constante_t == 0 else constante_t / 100
        casteljau_recursivo([np.array(pt) for pt in pontos_controle], t, curva)

    for ponto in curva:
        app.color_pixel(int(ponto[0]), int(ponto[1]), cor)
        curva.append(ponto)
        if velocidade < 100:
            sleep((100 - velocidade) / 10000)

    return curva
