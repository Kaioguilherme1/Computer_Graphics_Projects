import tkinter as tk
import sys
from tkinter import ttk

# Import dos algoritmos e da interface
from interface import MatrizDeRasterizacao
from flood_fill import flood_fill, desenhar_poligono, encontrar_ponto_interno
from varredura_preenchimento_algo import varredura_geometrica



# feito isto para o algoritimo Flood_fill para matrizes maiores que 64 x 64
print('Limite de recursão anterior: ',sys.getrecursionlimit())  #
sys.setrecursionlimit(50000)  # Altere 2000 para o novo limite desejado
print('Limite de recursão Atual: ',sys.getrecursionlimit())  #



# Define os pontos para gerar as retas
Vertices = []

# Define tamanho das matrizes
Vertical = 500
Horizontal = 500
pixel = 1

# Variável global para definir a velocidade do algoritmo
velocidade_algoritmo = 100  # 0 significa tempo real


class MainApplication:
    def __init__(self, raiz):
        """Configura a janela principal."""
        self.raiz = raiz
        self.raiz.title("Comparação de Algoritmos de preenchimento")

        # Contêiner para as telas
        self.container = ttk.Frame(raiz)
        self.container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Frame lateral para os controles e informações
        self.lateral_frame = ttk.Frame(raiz, width=200)
        self.lateral_frame.pack(side=tk.RIGHT, fill=tk.Y)

        # Adicionar um título na seção lateral
        titulo_label = ttk.Label(self.lateral_frame, text="Controles", font=("Arial", 12))
        titulo_label.pack(pady=10)

        # Coordenadas clicadas
        self.coord_label = ttk.Label(self.lateral_frame, text="Coordenadas: Nenhum clique", font=("Arial", 16),
                                     relief="sunken", anchor="center", background="white")
        self.coord_label.pack(fill=tk.X, padx=10, pady=5)

        # Slider para controle da velocidade
        self.slider_label = ttk.Label(self.lateral_frame, text="Velocidade do Algoritmo:0 %")
        self.slider_label.pack(padx=10, pady=5)
        self.velocidade_slider = ttk.Scale(self.lateral_frame, from_=0, to=100, orient="horizontal",
                                           command=self.atualizar_velocidade)
        self.velocidade_slider.set(100)  # Inicia no valor 0 (tempo real)
        self.velocidade_slider.pack(fill=tk.X, padx=10, pady=5)

        # Botão para "Iniciar Todos"
        self.iniciar_btn = ttk.Button(self.lateral_frame, text="Iniciar Todos", command=self.iniciar_todos)
        self.iniciar_btn.pack(fill=tk.X, padx=10, pady=5)

        # Botão para "Reiniciar Todos"
        self.reiniciar_btn = ttk.Button(self.lateral_frame, text="Reiniciar Todos", command=self.reiniciar_todos)
        self.reiniciar_btn.pack(fill=tk.X, padx=10, pady=5)

        # Lista de instâncias criadas
        self.pixel_apps = []

        self.adicionar_nova_tela(
            obj=MatrizDeRasterizacao, altura=Vertical, largura=Horizontal, titulo="Algoritmo: Flood Fill",
            algoritmo=Flood_Fill
        )

        self.adicionar_nova_tela(
            obj=MatrizDeRasterizacao, altura=Vertical, largura=Horizontal, titulo="Algoritmo: Varredura com análise Geométrica",
            algoritmo=Analise_Geometrica
        )


    def adicionar_nova_tela(self, obj, altura=64, largura=64, titulo="Nova Tela", algoritmo=None):
        """Adiciona uma nova janela de exibição ao contêiner."""
        app = obj(self.container, altura=altura, largura=largura, pixel_size=pixel, titulo=titulo, algoritmo=algoritmo)
        self.pixel_apps.append(app)

        # Adiciona o evento de clique nas células da matriz
        app.canvas.bind("<Button-1>", lambda evento, app=app: self.capturar_clique_matriz(evento, app))

    def capturar_clique_matriz(self, evento, app):
        """Captura o clique no canvas e armazena os pontos clicados em uma lista global `Vertices`.

        :param evento: Evento de clique no canvas.
        :param app: Instância da janela onde ocorreu o clique.
        """
        # Calcula o pixel clicado com base no tamanho dos pixels
        tamanho_pixel = app.pixel_size
        linha = evento.y // tamanho_pixel
        coluna = evento.x // tamanho_pixel

        global Vertices

        # Adiciona o ponto clicado à lista de vértices
        Vertices.append([coluna, linha])

        # Atualiza a interface mostrando os pontos já capturados
        self.coord_label.config(text=f"Vértices capturados: {len(Vertices)}\nÚltimo Vértice: ({coluna}, {linha})")

        # Pinta o pixel clicado de azul
        app.color_pixel(coluna, linha, "blue")

    def iniciar_todos(self):
        """Inicia o algoritmo em todas as janelas."""
        for app in self.pixel_apps:
            app.iniciar()  # Usa o método iniciar() de cada instância

    def reiniciar_todos(self):
        """Reinicia todas as janelas."""
        global Vertices
        Vertices = []
        for app in self.pixel_apps:
            app.reiniciar()  # Usa o método reiniciar() para limpar a matriz

    def atualizar_velocidade(self, valor):
        """Atualiza a velocidade global do algoritmo com o valor do slider.

        :param valor: Valor do slider (string passada pelo evento do slider)
        """
        global velocidade_algoritmo
        velocidade_algoritmo = int(float(valor))  # Converte para inteiro
        self.slider_label.config(text=f"Velocidade Atual: {velocidade_algoritmo} %")
        print(f"Velocidade do algoritmo ajustada para: {velocidade_algoritmo} %")


# Funções dos algoritmos conectadas à interface principal
def Flood_Fill(app):
    desenhar_poligono(app, Vertices)
    flood_fill(app, encontrar_ponto_interno(Vertices), velocidade_algoritmo)

def Analise_Geometrica(app):
    varredura_geometrica(app, Vertices, velocidade_algoritmo)



# Executa o aplicativo principal
if __name__ == "__main__":
    raiz = tk.Tk()
    app = MainApplication(raiz)
    raiz.mainloop()