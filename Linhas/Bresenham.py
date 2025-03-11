from time import sleep


def desenhar_linha_bresenham(app, ponto1, ponto2, velocidade=0, cor="red"):
    """
    Implementação do Algoritmo de Bresenham para desenhar uma linha, adaptado para receber dois pontos.

    :param app: Objeto gráfico com método `color_pixel` para desenhar um pixel.
    :param ponto1: Coordenadas [x1, y1] do ponto inicial da linha.
    :param ponto2: Coordenadas [x2, y2] do ponto final da linha.
    :param cor: Cor da linha. Padrão: "red".
    :param velocidade: Velocidade do desenho (0-100). Padrão: 100 (mais rápido).
    """
    x1, y1 = ponto1
    x2, y2 = ponto2

    # Cálculo das diferenças Δx e Δy
    dx = x2 - x1
    dy = y2 - y1

    # Determinação das direções de incremento
    passo_x = 1 if dx > 0 else -1
    passo_y = 1 if dy > 0 else -1

    # Trabalha com valores absolutos para Δx e Δy
    dx = abs(dx)
    dy = abs(dy)

    # Inicializa o parâmetro de decisão
    if dx > dy:  # Caso inclinação da linha seja <= 1
        p = 2 * dy - dx  # Valor inicial do parâmetro, erro acumulado
        y = y1  # Começa no y inicial

        # Loop para rasterizar cada pixel
        for x in range(x1, x2 + passo_x, passo_x):  # Itera de x1 até x2
            app.color_pixel(x, y, cor)  # Desenha o pixel
            if p >= 0:  # Se o parâmetro indica um erro acumulado suficiente...
                y += passo_y  # Incrementa y (diagonal)
                p += 2 * (dy - dx)  # Atualiza o parâmetro para diagonal
            else:
                p += 2 * dy  # Atualiza o parâmetro lateral

            # Adiciona atraso baseado na velocidade (quanto menor, mais lento)
            if velocidade < 100:
                sleep((100 - velocidade) / 10000)

    else:  # Caso inclinação da linha seja > 1
        p = 2 * dx - dy  # Valor inicial do parâmetro
        x = x1  # Começa no x inicial

        # Loop para rasterizar cada pixel
        for y in range(y1, y2 + passo_y, passo_y):  # Itera de y1 até y2
            app.color_pixel(x, y, cor)  # Desenha o pixel
            if p >= 0:  # Se o parâmetro indica um erro acumulado suficiente...
                x += passo_x  # Incrementa x (diagonal)
                p += 2 * (dx - dy)  # Atualiza o parâmetro para diagonal
            else:
                p += 2 * dx  # Atualiza o parâmetro lateral

            # Adiciona atraso baseado na velocidade (quanto menor, mais lento)
            if velocidade < 100:
                sleep((100 - velocidade) / 10000)