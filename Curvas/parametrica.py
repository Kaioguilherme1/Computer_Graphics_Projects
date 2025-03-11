from time import sleep

def bezier(t, pontos_controle):
    """
    Calcula a posição na curva de Bézier para um valor t utilizando a fórmula paramétrica.

    :param t: Valor paramétrico (0 <= t <= 1).
    :param pontos_controle: Lista de pontos de controle da curva.
    :return: Posição na curva de Bézier [x, y].
    """
    n = len(pontos_controle) - 1  # Ordem da curva (número de pontos de controle - 1)
    x = 0
    y = 0
    # Calcula a posição na curva usando a fórmula paramétrica de Bézier
    for i in range(n + 1):
        coeficiente = (fatorial(n) / (fatorial(i) * fatorial(n - i))) * ((1 - t) ** (n - i)) * (t ** i)
        x += coeficiente * pontos_controle[i][0]
        y += coeficiente * pontos_controle[i][1]
    return [int(x), int(y)]  # Retorna o ponto na curva de Bézier

def fatorial(n):
    """Calcula o fatorial de n."""
    if n == 0:
        return 1
    resultado = 1
    for i in range(1, n + 1):
        resultado *= i
    return resultado

def desenhar_curva_bezier(app, pontos_controle,constante_t=0, num_pontos=100, velocidade=100, cor='blue'):
    """
    Desenha a curva de Bézier utilizando a equação paramétrica, desenhando ponto a ponto.

    :param app: Instância do aplicativo onde os pixels serão desenhados.
    :param pontos_controle: Lista dos pontos de controle da curva de Bézier.
    :param num_pontos: Número de pontos para desenhar a curva.
    :param velocidade: Velocidade do desenho (0-100). Padrão 100 (mais rápido).
    """
    for i in range(num_pontos + 1):
        if constante_t == 0:
            t = i / num_pontos  # O valor de t varia de 0 a 1
        else:
            t = constante_t/100

        ponto = bezier(t, pontos_controle)  # Calcula o ponto na curva para o valor t
        # Desenha o ponto individualmente
        app.color_pixel(ponto[0], ponto[1], cor)  # Desenha o ponto na curva de Bézier com a cor azul

        # Adiciona atraso baseado na velocidade (quanto menor, mais lento)
        if velocidade < 100:
            sleep((100 - velocidade) / 10000)

    return pontos_controle  # Retorna os pontos de controle da curva
