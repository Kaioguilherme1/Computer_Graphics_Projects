from time import sleep
from Linhas.Bresenham import desenhar_linha_bresenham

def sutherland_hodgman_clip(app, poligono, janela_recorte, velocidade=100):
    """
    Recorta um polígono arbitrário contra uma janela de recorte convexa usando o algoritmo Sutherland-Hodgman,
    desenhando progressivamente à medida que o recorte ocorre.

    :param app: Instância do aplicativo onde os pixels serão desenhados.
    :param poligono: Lista de vértices do polígono original. Cada vértice é representado por [x, y].
    :param janela_recorte: Lista de vértices que definem a janela de recorte convexa.
    :param velocidade: Velocidade do desenho (0-100). Padrão 100 (mais rápido).
    :return: Lista de vértices do polígono recortado.
    """
    def dentro(ponto, aresta):
        """ Verifica se um ponto está dentro da borda de recorte. """
        (x1, y1), (x2, y2) = aresta
        return (x2 - x1) * (ponto[1] - y1) - (y2 - y1) * (ponto[0] - x1) >= 0

    def intersecao(ponto1, ponto2, aresta):
        """ Calcula a interseção entre a aresta do polígono e a borda de recorte. """
        (x1, y1), (x2, y2) = aresta
        dx, dy = ponto2[0] - ponto1[0], ponto2[1] - ponto1[1]
        dx_aresta, dy_aresta = x2 - x1, y2 - y1
        num = (x1 - ponto1[0]) * dy_aresta - (y1 - ponto1[1]) * dx_aresta
        den = dx * dy_aresta - dy * dx_aresta
        if den == 0:
            return ponto1  # Se paralelo, retorna o próprio ponto
        t = num / den
        return [int(ponto1[0] + t * dx), int(ponto1[1] + t * dy)]

    lista_saida = poligono
    print(velocidade)
    for i in range(len(janela_recorte)):
        lista_entrada = lista_saida
        lista_saida = []
        aresta = (janela_recorte[i], janela_recorte[(i + 1) % len(janela_recorte)])
        # Adiciona atraso baseado na velocidade e desenha o progresso
        if velocidade < 100:
            sleep((100 - velocidade) / 100)
        app.limpar()
        desenhar_poligono(app, janela_recorte, cor='red')
        desenhar_poligono(app, lista_saida, cor='blue')

        for j in range(len(lista_entrada)):
            ponto1, ponto2 = lista_entrada[j], lista_entrada[(j + 1) % len(lista_entrada)]
            ponto1_dentro = dentro(ponto1, aresta)
            ponto2_dentro = dentro(ponto2, aresta)


            if ponto1_dentro and ponto2_dentro:
                lista_saida.append(ponto2)  # CASO 1: Ambos os pontos estão dentro, adiciona ponto2
            elif ponto1_dentro and not ponto2_dentro:
                lista_saida.append(intersecao(ponto1, ponto2, aresta))  # CASO 2: Adiciona a interseção
            elif not ponto1_dentro and ponto2_dentro:
                lista_saida.append(intersecao(ponto1, ponto2, aresta))  # CASO 4: Adiciona a interseção
                lista_saida.append(ponto2)  # CASO 4: Adiciona ponto2 pois está dentro
            # CASO 3: Ambos os pontos estão fora, nenhum é adicionado

        app.limpar()
        desenhar_poligono(app, janela_recorte, cor='red')
        desenhar_poligono(app, lista_saida, cor='blue')
    return lista_saida

def desenhar_poligono(app, vertices, cor='blue'):
    """
    Desenha o contorno do polígono ao conectar seus vértices.

    :param app: Instância do aplicativo onde os pixels serão desenhados.
    :param vertices: Lista dos vértices que compõem o polígono.
    :param cor: Cor usada para rasterizar o contorno.
    """
    for i in range(len(vertices)):
        ponto1 = vertices[i]
        ponto2 = vertices[(i + 1) % len(vertices)]
        desenhar_linha_bresenham(app, ponto1, ponto2,velocidade=100, cor=cor)


