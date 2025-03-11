import tkinter as tk
import sys
from tkinter import ttk

# Import dos algoritmos e da interface
from interface import MatrizDeRasterizacao
from Sutherland import sutherland_hodgman_clip, desenhar_poligono

# Define os pontos para gerar a janela de corte e o poligono
janela = []
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
            obj=MatrizDeRasterizacao, altura=Vertical, largura=Horizontal, titulo="Algoritmo: FRecorte",
            algoritmo=sutherland
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
        global janela
        # salva os primeiros 2 pontos como as quinas da janela
        if len(janela) < 2:
            # Adiciona o ponto clicado
            janela.append([coluna, linha])
            # Atualiza a interface mostrando o ponto clicado
            self.coord_label.config(text=f"Vértices capturados: {len(Vertices)}\nQuinas da janela: ({coluna}, {linha})")
            # Pinta o pixel clicado de vermelho
            app.color_pixel(coluna, linha, "red")

            if len(janela) == 2:
                # Pega as coordenadas dos dois pontos clicados
                x1, y1 = janela[0]
                x2, y2 = janela[1]

                # Calcula os pontos do retângulo com base nas coordenadas mínimas e máximas
                min_x = min(x1, x2)
                max_x = max(x1, x2)
                min_y = min(y1, y2)
                max_y = max(y1, y2)

                # Define as quinas do retângulo e ordena em sequencia
                janela = [(min_x, min_y), (max_x, min_y), (max_x, max_y), (min_x, max_y)]

            # Verifica se a lista janela tem as 4 quinas antes de tentar acessar os índices
            if len(janela) >= 4:
                # Atualiza a interface com todas as quinas da janela
                self.coord_label.config(text=f"Vértices capturados: {len(Vertices)}\nQuinas da janela: "
                                             f"({janela[0][0]}, {janela[0][1]})\n({janela[1][0]}, {janela[1][1]})\n"
                                             f"({janela[2][0]}, {janela[2][1]})\n({janela[3][0]}, {janela[3][1]})")

                # Pinta os pixels das outras quinas de vermelho
                app.color_pixel(janela[2][0], janela[2][1], "red")
                app.color_pixel(janela[3][0], janela[3][1], "red")

                # Desenha o polígono conectando as quinas
                desenhar_poligono(app, janela, cor='red')

        else:
            # Adiciona o ponto clicado à lista de vértices (caso esteja capturando mais pontos)
            Vertices.append([coluna, linha])
            # Atualiza a interface mostrando todos os pontos já capturados
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
        global janela
        janela = []
        Vertices = []

        # limpa as matrizes
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
def sutherland(app):
    sutherland_hodgman_clip(app, Vertices, janela, velocidade_algoritmo)




# Executa o aplicativo principal
if __name__ == "__main__":
    raiz = tk.Tk()
    app = MainApplication(raiz)
    raiz.mainloop()