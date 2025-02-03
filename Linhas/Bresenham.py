def draw_line_bresenham(app, x1, y1, x2, y2, color="red"):
    """
    Implementação do Algoritmo de Bresenham para desenhar uma linha.
    
    :param app: Objeto gráfico com método `color_pixel` para desenhar um pixel
    :param x1: Coordenada x do ponto inicial
    :param y1: Coordenada y do ponto inicial
    :param x2: Coordenada x do ponto final
    :param y2: Coordenada y do ponto final
    :param color: Cor da linha. Padrão: "red".
    """
    # Cálculo das diferenças Δx e Δy
    dx = x2 - x1
    dy = y2 - y1

    # Determinação das direções de incremento
    step_x = 1 if dx > 0 else -1
    step_y = 1 if dy > 0 else -1

    # Trabalha com valores absolutos para Δx e Δy
    dx = abs(dx)
    dy = abs(dy)

    # Inicializa o parâmetro de decisão
    if dx > dy:  # Caso inclinação da linha seja <= 1
        p = 2 * dy - dx  # Valor inicial do parâmetro
        y = y1  # Começa no y inicial

        # Loop para rasterizar cada pixel
        for x in range(x1, x2 + step_x, step_x):  # Itera de x1 até x2
            app.color_pixel(y, x, color)  # Desenha o pixel
            if p >= 0:  # Se o parâmetro indica um erro acumulado suficiente...
                y += step_y  # Incrementa y (diagonal)
                p += 2 * (dy - dx)  # Atualiza o parâmetro para diagonal
            else:
                p += 2 * dy  # Atualiza o parâmetro (mesma linha)
    else:  # Caso inclinação da linha seja > 1
        p = 2 * dx - dy  # Valor inicial do parâmetro
        x = x1  # Começa no x inicial

        # Loop para rasterizar cada pixel
        for y in range(y1, y2 + step_y, step_y):  # Itera de y1 até y2
            app.color_pixel(y, x, color)  # Desenha o pixel
            if p >= 0:  # Se o parâmetro indica um erro acumulado suficiente...
                x += step_x  # Incrementa x (diagonal)
                p += 2 * (dx - dy)  # Atualiza o parâmetro para diagonal
            else:
                p += 2 * dx  # Atualiza o parâmetro (mesma linha)