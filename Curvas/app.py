import tkinter as tk
import os
import sys
from tkinter import ttk

# Adiciona o diretório pai ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import dos algoritmos e da interface
from interface import MatrizDeRasterizacao
from parametrica import desenhar_curva_bezier

# Define os Pontos para gerar a curva
Pontos = []

# Define tamanho das matrizes
Vertical = 500
Horizontal = 500
pixel = 1

# Variável global para definir a velocidade do algoritmo
velocidade_algoritmo = 100  # 0 significa tempo real
besie = 0
num_pontos = 100
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
        self.slider_label = ttk.Label(self.lateral_frame, text="Velocidade do Algoritmo:1 %")
        self.slider_label.pack(padx=10, pady=5)
        self.velocidade_slider = ttk.Scale(self.lateral_frame, from_=1, to=100, orient="horizontal",
                                           command=self.atualizar_velocidade)
        self.velocidade_slider.set(100)  # Inicia no valor 0 (tempo real)
        self.velocidade_slider.pack(fill=tk.X, padx=10, pady=5)

        # Slider para controle da Curva de Besie que varia de 0.00 a 1 (100%)
        self.besie_label = ttk.Label(self.lateral_frame, text="Curva de Besie:0 %")
        self.besie_label.pack(padx=10, pady=5)
        self.besie_slider = ttk.Scale(self.lateral_frame, from_=0, to=100, orient="horizontal",
                                           command=self.atualizar_besie)
        self.besie_slider.set(0)  # Inicia no valor 0 (tempo real)
        self.besie_slider.pack(fill=tk.X, padx=10, pady=5)

        #Slider para Numero de pontos do Algoritimo Parametrico
        self.pontos_label = ttk.Label(self.lateral_frame, text="Pontos:100")
        self.pontos_label.pack(padx=10, pady=5)
        self.pontos_slider = ttk.Scale(self.lateral_frame, from_=0, to=1000, orient="horizontal",
                                           command=self.atualizar_pontos)
        self.pontos_slider.set(100)  # Inicia no valor 0 (tempo real)
        self.pontos_slider.pack(fill=tk.X, padx=10, pady=5)

        # Botão para "Iniciar Todos"
        self.iniciar_btn = ttk.Button(self.lateral_frame, text="Iniciar Todos", command=self.iniciar_todos)
        self.iniciar_btn.pack(fill=tk.X, padx=10, pady=5)

        # Botão para "Reiniciar Todos"
        self.reiniciar_btn = ttk.Button(self.lateral_frame, text="Reiniciar Todos", command=self.reiniciar_todos)
        self.reiniciar_btn.pack(fill=tk.X, padx=10, pady=5)

        # Lista de instâncias criadas
        self.pixel_apps = []

        self.adicionar_nova_tela(
            obj=MatrizDeRasterizacao, altura=Vertical, largura=Horizontal, titulo="Algoritmo: Bezier Equação Parametrica",
            algoritmo=parametrica
        )

    def adicionar_nova_tela(self, obj, altura=64, largura=64, titulo="Nova Tela", algoritmo=None):
        """Adiciona uma nova janela de exibição ao contêiner."""
        app = obj(self.container, altura=altura, largura=largura, pixel_size=pixel, titulo=titulo, algoritmo=algoritmo)
        self.pixel_apps.append(app)

        # Adiciona o evento de clique nas células da matriz
        app.canvas.bind("<Button-1>", lambda evento, app=app: self.capturar_clique_matriz(evento, app))

    def capturar_clique_matriz(self, evento, app):
        """Captura o clique no canvas e armazena os Pontos clicados em uma lista global `Vertices`.

        :param evento: Evento de clique no canvas.
        :param app: Instância da janela onde ocorreu o clique.
        """
        # Calcula o pixel clicado com base no tamanho dos pixels
        tamanho_pixel = app.pixel_size
        linha = evento.y // tamanho_pixel
        coluna = evento.x // tamanho_pixel

        global Pontos

        # Adiciona o ponto clicado à lista de vértices
        Pontos.append([coluna, linha])

        # Atualiza a interface mostrando os Pontos já capturados
        self.coord_label.config(text=f"Vértices capturados: {len(Pontos)}\nÚltimo Vértice: ({coluna}, {linha})")

        # Pinta o pixel clicado de azul
        app.color_pixel(coluna, linha, "blue")

    def iniciar_todos(self):
        """Inicia o algoritmo em todas as janelas."""
        for app in self.pixel_apps:
            app.iniciar()  # Usa o método iniciar() de cada instância

    def reiniciar_todos(self):
        """Reinicia todas as janelas."""
        global Pontos
        Pontos = []
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

    def atualizar_besie(self, valor):
        """Atualiza a constante t do algoritmo com o valor do slider.

        :param valor: Valor do slider (string passada pelo evento do slider)
        """
        global besie
        global num_pontos
        global velocidade_algoritmo
        besie = int(float(valor))  # Converte para inteiro
        self.besie_label.config(text=f"Besie Atual: {besie} %")
        print(f"Besie do algoritmo ajustada para: {besie} %")

        if velocidade_algoritmo == 100:
            # atualiza o desenho da tela
            for app in self.pixel_apps:
                app.reiniciar()  # Usa o método reiniciar() para limpar a matriz

            desenhar_curva_bezier(app, pontos_controle=Pontos, constante_t=besie, num_pontos=num_pontos, velocidade=velocidade_algoritmo)
        else:
            # Exbibe uma mensagem de aviso
            self.coord_label.config(text="A velocidade do algoritmo deve ser 100%\n para atualizar o desenho.")

    def atualizar_pontos(self, valor):
        """Atualiza a o numero de pontos do algoritmo parametrico com o valor do slider.

        :param valor: Valor do slider (string passada pelo evento do slider)
        """
        global besie
        global num_pontos
        global velocidade_algoritmo
        num_pontos = int(float(valor))  # Converte para inteiro
        self.pontos_label.config(text=f"Num Pontos Atual: {num_pontos} %")

        if velocidade_algoritmo == 100:
            # atualiza o desenho da tela
            for app in self.pixel_apps:
                app.reiniciar()  # Usa o método reiniciar() para limpar a matriz

            desenhar_curva_bezier(app, pontos_controle=Pontos, num_pontos=num_pontos, velocidade=velocidade_algoritmo)
        else:
            # Exbibe uma mensagem de aviso
            self.coord_label.config(text="A velocidade do algoritmo deve ser 100%\n para atualizar o desenho.")
# Funções dos algoritmos conectadas à interface principal
def parametrica(app):
    desenhar_curva_bezier(app, pontos_controle=Pontos, constante_t=besie,num_pontos=num_pontos, velocidade=velocidade_algoritmo)

# Executa o aplicativo principal
if __name__ == "__main__":
    raiz = tk.Tk()
    app = MainApplication(raiz)
    raiz.mainloop()