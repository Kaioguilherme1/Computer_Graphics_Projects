from time import sleep

def varredura_geometrica(app, poligono, velocidade=100, cor="red"):
    """
    Algoritmo de Varredura com Análise Geométrica para preenchimento linha por linha.
    :param app: Instância com métodos `get_pixel` e `color_pixel` para manipular pixels.
    :param poligono: Lista de vértices do polígono [(x1, y1), (x2, y2), ...].
    :param velocidade: Atraso opcional para visualização (não utilizado diretamente aqui).
    :param cor_alvo: Cor da área a ser preenchida.
    :param nova_cor: Nova cor que substituirá o alvo.
    """

    # 1º Passo: Montar a tabela de lados
    arestas = montar_tabela_lados(poligono)

    # Identificar os limites de varredura
    y_min = min(v[1] for v in poligono)
    y_max = max(v[1] for v in poligono)

    # 2º Passo: Realizar a varredura linha por linha (scan-line)
    for y_varredura in range(y_min, y_max + 1):
        # Encontrar interseções com a linha de varredura
        intersecoes = encontrar_intersecoes(arestas, y_varredura)

        # Ordenar os pontos de interseção em X
        intersecoes.sort()

        # 3º Passo: Aplicar a regra de paridade para determinar as áreas a preencher
        for i in range(0, len(intersecoes) - 1, 2):
            x_inicio = int(intersecoes[i])
            x_fim = int(intersecoes[i + 1])

            # 4º Passo: Colorir os pixels no intervalo
            for x in range(x_inicio, x_fim + 1):
                # Preencher apenas se a cor for a cor alvo

                # Adiciona atraso baseado na velocidade (quanto menor, mais lento)
                if velocidade < 100:
                    sleep((100 - velocidade) / 10000)

                app.color_pixel(x, y_varredura, cor)


def montar_tabela_lados(poligono):
    """
    Monta a Tabela de Lados (TL) a partir do polígono.
    Cada aresta é representada com valores:
    Xmin, Ymin, Ymax, m (declividade).
    """
    arestas = []
    n = len(poligono)

    for i in range(n):
        # Coordenadas dos dois vértices da aresta
        x1, y1 = poligono[i]
        x2, y2 = poligono[(i + 1) % n]  # Conectar ao próximo vértice, ou ao primeiro se for o último

        # Ignorar arestas horizontais
        if y1 == y2:
            continue

        # Garantir que (Ymin, Xmin) seja o ponto de menor Y
        if y1 > y2:
            x1, y1, x2, y2 = x2, y2, x1, y1

        # Calcular a declividade (m = Δx/Δy)
        m = (x2 - x1) / (y2 - y1)

        # Adicionar dados da aresta
        arestas.append({
            "Xmin": x1,
            "Ymin": y1,
            "Ymax": y2,
            "m": m  # Declividade inversa usada no cálculo de interseções
        })

    return arestas


def encontrar_intersecoes(arestas, y_varredura):
    """
    Encontra as interseções (X_interseção) das arestas com a linha de varredura.
    """
    intersecoes = []

    for aresta in arestas:
        # Apenas considerar arestas cuja linha de varredura cruza
        if aresta["Ymin"] <= y_varredura < aresta["Ymax"]:
            # Usar a equação da reta para calcular a interseção X
            x_intersecao = aresta["Xmin"] + (y_varredura - aresta["Ymin"]) * aresta["m"]
            intersecoes.append(x_intersecao)

    return intersecoes


