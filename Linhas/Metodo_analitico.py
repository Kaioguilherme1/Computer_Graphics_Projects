import time
from time import sleep

def desenhar_linha_analitica(app, ponto1, ponto2, velocidade=100, cor="red"):
    """
    Desenha uma linha utilizando o método analítico (equação da reta).

    :param app: Instância/ferramenta que permite desenhar um pixel (`app.color_pixel`).
    :param ponto1: Lista [x, y] especificando o ponto inicial.
    :param ponto2: Lista [x, y] especificando o ponto final.
    :param cor: Cor da linha (padrão: "red").
    :param velocidade: Tempo (em segundos) entre cada iteração do desenho (padrão: 0 = sem pausa).
    """
    # Extraindo as coordenadas dos pontos
    x1, y1 = ponto1
    x2, y2 = ponto2

    # Verifica se a inclinação é indefinida ou se a linha é vertical
    if x1 == x2:  # Caso de linha vertical
        for y in range(min(y1, y2), max(y1, y2) + 1):
            app.color_pixel(x1, y, cor)  # Desenha na mesma coluna, variando apenas no eixo Y
            # Adiciona atraso baseado na velocidade (quanto menor, mais lento)
            if velocidade < 100:
                sleep((100 - velocidade) / 10000)
    else:
        # Calcula a inclinação (m) e o intercepto (b) da equação da linha
        m = (y2 - y1) / (x2 - x1)  # Inclinação
        b = y1 - m * x1  # Intercepto da reta (quando x = 0)

        # Iteramos pelo intervalo de menor x até o maior x
        for x in range(min(x1, x2), max(x1, x2) + 1):
            y = round(m * x + b)  # Calcula o valor de y correspondente e arredonda
            app.color_pixel(x, y, cor)  # Desenha o pixel no ponto [y, x]
            # Adiciona atraso baseado na velocidade (quanto menor, mais lento)
            if velocidade < 100:
                sleep((100 - velocidade) / 10000)