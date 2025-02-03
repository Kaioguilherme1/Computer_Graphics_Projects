def draw_line_analytic(app, x1, y1, x2, y2, color='red'):
    """
    Desenha uma linha utilizando o método analítico (equação da reta).
    
    :param app: Instância/ferramenta que permite desenhar um pixel (`app.color_pixel`).
    :param x1: Coordenada x do primeiro ponto.
    :param y1: Coordenada y do primeiro ponto.
    :param x2: Coordenada x do segundo ponto.
    :param y2: Coordenada y do segundo ponto.
    """
    # Verifica se a inclinação é indefinida ou se é necessário percorrer pelo eixo Y
    if x1 == x2:  # Linha vertical
        for y in range(min(y1, y2), max(y1, y2) + 1):
            app.color_pixel(y, x1, color)  # Desenha na mesma coluna para variar no Y
    else:
        # Calcula a inclinação (m) e o intercepto (b) da equação da linha
        m = (y2 - y1) / (x2 - x1)
        b = y1 - m * x1

        # Iteramos no intervalo de x menor para x maior
        for x in range(min(x1, x2), max(x1, x2) + 1):
            y = round(m * x + b)  # Encontra o valor de y correspondente e arredonda
            app.color_pixel(y, x, "red")  # Desenha o pixel correspondente