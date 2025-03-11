from time import sleep

from Linhas.Bresenham import desenhar_linha_bresenham

def desenhar_poligono(app, vertices, velocidade=100, cor='blue'):
    """
    Desenha o contorno do polígono ao conectar seus vértices, utilizando o algoritmo de Bresenham.

    :param app: Instância do aplicativo onde os pixels serão desenhados.
    :param vertices: Lista dos vértices que compõem o polígono. Cada vértice é representado por [x, y].
    :param cor: Cor usada para rasterizar o contorno.
    :param velocidade: Velocidade do desenho (0-100). Padrão 100 (mais rápido).
    """
    for i in range(len(vertices)):
        ponto1 = vertices[i]  # Vértice atual
        ponto2 = vertices[(i + 1) % len(vertices)]  # Próximo vértice (último conecta ao primeiro)

        # Conecta o vértice atual com o próximo utilizando o algoritmo de Bresenham
        desenhar_linha_bresenham(app, ponto1, ponto2, velocidade, cor)


def encontrar_ponto_interno(vertices):
    """
    Encontra um ponto interno garantido dentro do polígono.

    :param vertices: Lista de vértices que formam o polígono.
    :return: Um ponto interno [x, y].
    """
    # Estratégia simples: calcular o centroide (média das coordenadas dos vértices)
    x_medio = sum(v[0] for v in vertices) // len(vertices)
    y_medio = sum(v[1] for v in vertices) // len(vertices)
    return [x_medio, y_medio]

def flood_fill(app, posicao, velocidade=100, cor_alvo="white", nova_cor="red"):
    """
    Implementação recursiva simples do Flood Fill com base no pseudocódigo fornecido.
    :param app: Instância para acessar métodos de `get_pixel` e `color_pixel`.
    :param posicao: Lista/tupla contendo a posição inicial [x, y].
    :param velocidade: Não utilizado aqui, mas poderia ser usado para adicionar atrasos.
    :param cor_alvo: Cor original que será substituída.
    :param nova_cor: Nova cor usada para preencher.
    """
    x, y = posicao

    # Condição: Verificar se está dentro dos limites da matriz
    if not (0 <= x < app.largura and 0 <= y < app.altura):
        return

    # Condição: Verificar se o pixel tem a cor alvo ou a nova cor
    cor_atual = app.get_pixel(x, y)
    if cor_atual != cor_alvo:
        return

    if cor_atual == nova_cor:
        return

    cor_atual = None

    # Adiciona atraso baseado na velocidade (quanto menor, mais lento)
    if velocidade < 100:
        sleep((100 - velocidade) / 10000)

    # Preencher o pixel com a nova cor
    app.color_pixel(x, y, nova_cor)

    # Chamadas recursivas para os 4 vizinhos
    flood_fill(app, [x + 1, y], velocidade, cor_alvo, nova_cor)  # Direita
    flood_fill(app, [x - 1, y], velocidade, cor_alvo, nova_cor)  # Esquerda
    flood_fill(app, [x, y + 1], velocidade, cor_alvo, nova_cor)  # Abaixo
    flood_fill(app, [x, y - 1], velocidade, cor_alvo, nova_cor)  # Acima

