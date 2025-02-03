def draw_line_dda(app, x1, y1, x2, y2, color="red"):
    """
    Implementação do Método DDA (Digital Differential Analyzer), utilizando if-else.
    Desenha uma linha no espaço discreto entre dois pontos (x1, y1) e (x2, y2).

    :param app: Objeto gráfico com o método `color_pixel` para desenhar pixels
    :param x1: Coordenada x do ponto inicial
    :param y1: Coordenada y do ponto inicial
    :param x2: Coordenada x do ponto final
    :param y2: Coordenada y do ponto final
    :param color: Cor da linha (por padrão, "red")
    """
    # Calcula as diferenças (dx e dy)
    dx = x2 - x1
    dy = y2 - y1

    # Verifica se o delta dominante é horizontal ou vertical
    if abs(dx) > abs(dy):  # Caso |x2 - x1| > |y2 - y1| (incremento principal no eixo x)
        steps = abs(dx)  # Passos a serem percorridos no eixo x
        increment_y = dy / dx  # Incremento proporcional no eixo y
        increment_x = 1 if dx > 0 else -1  # Determina a direção do incremento em x

        # Começa nos valores iniciais
        x = x1
        y = y1

        # Loop principal para rasterizar a linha
        for _ in range(steps + 1):
            app.color_pixel(round(y), round(x), color)  # Desenha o pixel
            x += increment_x  # Incremento em x
            y += increment_y  # Incremento em y proporcional
    else:  # Caso contrário, |y2 - y1| >= |x2 - x1| (incremento principal no eixo y)
        steps = abs(dy)  # Passos a serem percorridos no eixo y
        increment_x = dx / dy  # Incremento proporcional no eixo x
        increment_y = 1 if dy > 0 else -1  # Determina a direção do incremento em y

        # Começa nos valores iniciais
        x = x1
        y = y1

        # Loop principal para rasterizar a linha
        for _ in range(steps + 1):
            app.color_pixel(round(y), round(x), color)  # Desenha o pixel
            x += increment_x  # Incremento em x proporcional
            y += increment_y  # Incremento em y
