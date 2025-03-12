from time import sleep


def casteljau(t, pontos_controle):
    """
    Calcula um ponto na curva de Bézier utilizando o algoritmo de De Casteljau.

    :param t: Valor paramétrico (0 <= t <= 1).
    :param pontos_controle: Lista de pontos de controle da curva.
    :return: Ponto interpolado na curva de Bézier [x, y].
    """
    pontos = pontos_controle[:]
    n = len(pontos) - 1  # Ordem da curva (grau da Bézier)

    # Aplicação do algoritmo de De Casteljau
    for r in range(1, n + 1):  # Percorre os níveis da interpolação
        for i in range(n - r + 1):  # Calcula os novos pontos intermediários
            # Interpolação linear entre dois pontos
            x = (1 - t) * pontos[i][0] + t * pontos[i + 1][0]
            y = (1 - t) * pontos[i][1] + t * pontos[i + 1][1]
            pontos[i] = [x, y]  # Atualiza o ponto interpolado

    return [int(pontos[0][0]), int(pontos[0][1])]  # Retorna o ponto final calculado


def desenhar_curva_casteljau(app, pontos_controle, num_pontos=100, constante_t=0, velocidade=100, cor='red'):
    """
    Desenha a curva de Bézier utilizando o algoritmo de De Casteljau.

    :param app: Instância do aplicativo onde os pixels serão desenhados.
    :param pontos_controle: Lista de pontos de controle da curva de Bézier.
    :param constante_t: Define um valor fixo de t (0 a 100) ou 0 para variação automática.
    :param velocidade: Velocidade do desenho (0-100). Padrão 100 (mais rápido).
    :param cor: Cor usada para rasterizar a curva.
    """
    curva = []
    for i in range(num_pontos + 1):
        if constante_t == 0:
            t = i / num_pontos  # Variação automática de t de 0 a 1
        else:
            t = constante_t / 100  # Usa o valor fixo de t fornecido

        ponto = casteljau(t, pontos_controle)  # Calcula o ponto na curva
        app.color_pixel(ponto[0], ponto[1], cor)  # Desenha o ponto na tela
        curva.append(ponto)
        # Adiciona um pequeno atraso baseado na velocidade para visualização do desenho
        if velocidade < 100:
            sleep((100 - velocidade) / 10000)

    return curva  # Retorna os pontos de controle da curva
