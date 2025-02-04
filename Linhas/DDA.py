from time import sleep


def desenhar_linha_dda(app, ponto1, ponto2, velocidade=100, cor="red"):
    """
    Implementação do Método DDA (Digital Differential Analyzer), utilizando if-else.
    Desenha uma linha no espaço discreto entre dois pontos especificados por suas coordenadas.

    :param app: Objeto gráfico com o método `color_pixel` para desenhar pixels.
    :param ponto1: Lista [x, y] especificando o ponto inicial.
    :param ponto2: Lista [x, y] especificando o ponto final.
    :param cor: Cor da linha (por padrão, "red").
    :param velocidade: Valor de 0-100 para controlar a velocidade (100 = mais rápido).
    """
    # Extraindo as coordenadas dos pontos
    x1, y1 = ponto1
    x2, y2 = ponto2

    # Calcula as diferenças (dx e dy)
    dx = x2 - x1
    dy = y2 - y1

    # Verifica se o delta dominante é horizontal ou vertical
    if abs(dx) > abs(dy):  # Caso |x2 - x1| > |y2 - y1| (incremento principal no eixo x)
        passos = abs(dx)  # Número de passos no eixo x
        incremento_y = dy / abs(dx)  # Incremento proporcional no eixo y
        incremento_x = 1 if dx > 0 else -1  # Direção do incremento em x

        # Começa nos valores iniciais
        x = x1
        y = y1

        # Loop principal para rasterizar a linha
        for _ in range(passos + 1):
            app.color_pixel(round(x), round(y), cor)  # Desenha o pixel
            x += incremento_x  # Incremento em x
            y += incremento_y  # Incremento proporcional em y
            # Adiciona atraso baseado na velocidade
            if velocidade < 100:
                sleep((100 - velocidade) / 10000)

    else:  # Caso contrário, |y2 - y1| >= |x2 - x1| (incremento principal no eixo y)
        passos = abs(dy)  # Número de passos no eixo y
        incremento_x = dx / abs(dy)  # Incremento proporcional no eixo x
        incremento_y = 1 if dy > 0 else -1  # Direção do incremento em y

        # Começa nos valores iniciais
        x = x1
        y = y1

        # Loop principal para rasterizar a linha
        for _ in range(passos + 1):
            app.color_pixel(round(x), round(y), cor)  # Desenha o pixel
            x += incremento_x  # Incremento proporcional em x
            y += incremento_y  # Incremento em y
            # Adiciona atraso baseado na velocidade
            if velocidade < 100:
                sleep((100 - velocidade) / 10000)