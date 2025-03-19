from time import sleep
import numpy as np


def subdivision(pontos_controle):
    """
    Divide uma curva de Bézier em duas subcurvas usando o método de De Casteljau.
    A subdivisão ocorre calculando pontos médios entre pares consecutivos.
    """
    if len(pontos_controle) == 1:
        return pontos_controle

    novos_pontos = []  # Lista para armazenar os novos pontos gerados na subdivisão

    # Percorre todos os pontos de controle e calcula o ponto médio entre pares consecutivos
    for i in range(len(pontos_controle) - 1):
        media = (pontos_controle[i] + pontos_controle[i + 1]) / 2
        novos_pontos.append(media)

    # Recursivamente, retorna os pontos da primeira metade, o ponto central e os da segunda metade
    return [pontos_controle[0]] + subdivision(novos_pontos) + [pontos_controle[-1]]


def desenhar_curva_casteljau(app, pontos_controle, num_pontos=100, velocidade=100, cor='red', curva=None):
    """
    Desenha uma curva de Bézier utilizando recursão e subdivisões sucessivas pelo método de De Casteljau.

    Parâmetros:
    - app: Objeto que contém o método `color_pixel` para desenhar os pontos.
    - pontos_controle: Lista de pontos que definem a curva de Bézier.
    - num_pontos: Número de pontos desejado na curva final.
    - velocidade: Controla a velocidade de desenho (0 = mais rápido, 100 = mais lento).
    - cor: Cor dos pontos desenhados.
    - curva: Lista de pontos da curva acumulados pela recursão.

    Retorna:
    - Lista de pontos que representam a curva desenhada.
    """
    if len(pontos_controle) < 2:
        raise ValueError("São necessários pelo menos dois pontos de controle para desenhar a curva.")

    if curva is None:
        curva = []

    # Aplica a subdivisão para gerar mais pontos
    nova_curva = subdivision([np.array(pt) for pt in pontos_controle])

    # Adiciona os novos pontos gerados à curva final
    curva.extend(nova_curva)

    # Critério de parada: se já tivermos pontos suficientes, finaliza a recursão
    if len(curva) >= num_pontos:
        # Desenha cada ponto da curva final após as subdivisões
        for ponto in curva:
            app.color_pixel(int(ponto[0]), int(ponto[1]), cor)  # Desenha o ponto no objeto `app`

            # Controla a velocidade do desenho
            if velocidade < 100:
                sleep((100 - velocidade) / 10000)

        return curva

    # Chama a função recursivamente para continuar a subdivisão
    return desenhar_curva_casteljau(app, nova_curva, num_pontos, velocidade, cor, curva)