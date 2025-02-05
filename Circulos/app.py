import sys
import os

# Adiciona o diretório pai ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import tkinter as tk
from tkinter import ttk

from Equacao_parametrica import equacao_parametrica
from Incremental_com_simetria import incremental_com_simetria
from bresenham_circunferencia import bresenham_circunferencia

# Import dos algoritmos e da interface
from interface import MatrizDeRasterizacao

# Define os pontos para gerar as retas
ponto1, ponto2 = [], []

# Define tamanho das matrizes
Vertical = 400
Horizontal = 400
pixel = 1

# Variável global para definir a velocidade do algoritmo
velocidade_algoritmo = 100  # 0 significa tempo real


class MainApplication:
    def __init__(self, raiz):
        """Configura a janela principal."""
        self.raiz = raiz
        self.raiz.title("Comparação de Algoritmos de Rasterização de Circunferências")

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

        # Exemplo inicial com algoritmos específicos
        self.adicionar_nova_tela(
            obj=MatrizDeRasterizacao, altura=Vertical, largura=Horizontal, titulo="Algoritmo: Equação Paramétrica",
            algoritmo=eq_parametrica
        )
        self.adicionar_nova_tela(
            obj=MatrizDeRasterizacao, altura=Vertical, largura=Horizontal, titulo="Algoritmo: Incremental com Simetria",
            algoritmo=incremento_simetrico
        )
        self.adicionar_nova_tela(
            obj=MatrizDeRasterizacao, altura=Vertical, largura=Horizontal, titulo="Algoritmo: Bresenham", algoritmo=bresenham
        )

    def adicionar_nova_tela(self, obj, altura=64, largura=64, titulo="Nova Tela", algoritmo=None):
        """Adiciona uma nova janela de exibição ao contêiner."""
        app = obj(self.container, altura=altura, largura=largura, pixel_size=pixel, titulo=titulo, algoritmo=algoritmo)
        self.pixel_apps.append(app)

        # Adiciona o evento de clique nas células da matriz
        app.canvas.bind("<Button-1>", lambda evento, app=app: self.capturar_clique_matriz(evento, app))

    def capturar_clique_matriz(self, evento, app):
        """Captura o clique no canvas e atualiza as coordenadas selecionadas.

        :param evento: Evento de clique no canvas.
        :param app: Instância da janela onde ocorreu o clique.
        """
        # Calcula o pixel clicado com base no tamanho dos pixels
        tamanho_pixel = app.pixel_size
        linha = evento.y // tamanho_pixel
        coluna = evento.x // tamanho_pixel

        global ponto1, ponto2

        # Verifica qual ponto salvar
        if not ponto1:  # Caso `ponto1` não esteja definido (primeiro clique)
            ponto1.extend([coluna, linha])  # Salva as coordenadas no primeiro ponto
            self.coord_label.config(text=f"Primeiro ponto: ({coluna}, {linha})")  # Atualiza na interface
        elif not ponto2:  # Caso `ponto1` já exista, salva as coordenadas no segundo ponto
            ponto2.extend([coluna, linha])  # Salva as coordenadas no segundo ponto
            self.coord_label.config(
                text=f"Primeiro ponto: ({ponto1[1]}, {ponto1[0]})\nSegundo ponto: ({linha}, {coluna})")
        else:
            # Se ambos já estiverem definidos, avisa o usuário (ou pode substituir)
            self.coord_label.config(text="Ambos os pontos já estão definidos. Reinicie para redefinir.")

        # Pinta o pixel clicado de azul
        app.color_pixel(coluna, linha, "blue")

    def iniciar_todos(self):
        """Inicia o algoritmo em todas as janelas."""
        for app in self.pixel_apps:
            app.iniciar()  # Usa o método iniciar() de cada instância

    def reiniciar_todos(self):
        """Reinicia todas as janelas."""
        global ponto1, ponto2
        ponto1 = []
        ponto2 = []
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
def eq_parametrica(app):
    equacao_parametrica(app, ponto1, ponto2, velocidade_algoritmo)


def incremento_simetrico(app):
    incremental_com_simetria(app, ponto1, ponto2, velocidade_algoritmo)

def bresenham(app):
    bresenham_circunferencia(app, ponto1, ponto2, velocidade_algoritmo)

# Executa o aplicativo principal
if __name__ == "__main__":
    raiz = tk.Tk()
    app = MainApplication(raiz)
    raiz.mainloop()