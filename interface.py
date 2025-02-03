import tkinter as tk
from tkinter import ttk
import threading
import time


class MatrixDeRasterizacao:
    def __init__(self, pai, altura=64, largura=64, tamanho_pixel=5, titulo="Tela", algoritmo=None):
        """
        Inicializa o objeto MatrixDeRasterizacao.

        :param pai: Container pai onde a tela será embutida.
        :param altura: Número de linhas da matriz.
        :param largura: Número de colunas da matriz.
        :param tamanho_pixel: Tamanho de cada pixel (em pixels).
        :param titulo: Título que identifica esta tela.
        :param algoritmo: Função do algoritmo a ser executado, passada como callback.
        """
        self.pai = pai
        self.altura = altura
        self.largura = largura
        self.tamanho_pixel = tamanho_pixel
        self.executando = False  # Controla a execução do algoritmo
        self.algoritmo = algoritmo  # Define a função do algoritmo a ser usado

        if self.algoritmo is None:
            raise ValueError("É necessário passar uma função 'algoritmo' para a execução.")

        # Moldura que contém a tela
        self.moldura = ttk.Frame(pai, padding=5)
        self.moldura.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Nome/título da tela
        self.rotulo = ttk.Label(self.moldura, text=titulo, font=("Arial", 12, "bold"))
        self.rotulo.pack(pady=5)

        # Matriz (Canvas) onde os pixels são desenhados
        self.canvas = tk.Canvas(self.moldura, width=largura * tamanho_pixel, height=altura * tamanho_pixel, bg="white")
        self.canvas.pack()

        self.imagem = tk.PhotoImage(width=self.altura * tamanho_pixel, height=self.largura * tamanho_pixel)
        self.canvas.create_image((0, 0), image=self.imagem, anchor=tk.NW)

        # Preenche a imagem com branco inicialmente
        # self.preencher_imagem_com_cor("#FFFFFF")

        # Rótulo do cronômetro logo abaixo
        self.rotulo_cronometro = ttk.Label(self.moldura, text="Tempo decorrido: 0.00s", font=("Arial", 12),
                                           anchor="center")
        self.rotulo_cronometro.pack(fill=tk.X, padx=10, pady=5)

    def preencher_imagem_com_cor(self, cor):
        """Preenche toda a imagem com a cor especificada."""
        for x in range(self.altura):
            for y in range(self.largura):
                self.imagem.put(cor, (x, y))  # Define a cor de cada pixel

    def iniciar(self):
        """Inicia o algoritmo associado diretamente"""
        if self.executando:
            return  # Não inicia se já estiver em execução

        print(f"Iniciando algoritmo para a tela: {self.rotulo['text']}")
        self.executando = True

        # Define o momento inicial para o cronômetro
        self.tempo_inicial = time.time()

        # Cria uma thread dedicada para a execução do algoritmo
        self.thread = threading.Thread(target=self._executar_com_monitor)
        self.thread.daemon = True
        self.thread.start()

        # Inicia o cronômetro abaixo da tela
        self._atualizar_cronometro()

    def _executar_com_monitor(self):
        """Executa o algoritmo e monitora seu término."""
        try:
            self.algoritmo(self)  # Executa o algoritmo
        finally:
            self.executando = False
            print(f"Algoritmo para a tela '{self.rotulo['text']}' finalizado.")

    def _atualizar_cronometro(self):
        """Atualiza o cronômetro enquanto o algoritmo estiver em execução."""
        # Calcula o tempo decorrido
        tempo_decorrido = time.time() - self.tempo_inicial
        tempo_formatado = f"Tempo decorrido: {tempo_decorrido:.8f}s"

        # Atualiza o texto do cronômetro associado a esta tela
        if hasattr(self, "rotulo_cronometro"):  # Verifica se `rotulo_cronometro` está configurado
            self.rotulo_cronometro.config(text=tempo_formatado)

        # Continua atualizando enquanto o algoritmo da tela ainda estiver em execução
        if self.executando:
            # Repete a atualização após 100 ms
            self.rotulo_cronometro.after(100, self._atualizar_cronometro)

    def reiniciar(self):
        """Reinicia a matriz para o estado inicial de Pixels (branco)."""
        self.executando = False
        self.canvas.delete("all")
        print(f"Tela reiniciada: {self.rotulo['text']}")

    def color_pixel(self, x, y, cor):
        """
        Desenha um pixel ampliado no Canvas.

        :param x: Coordenada lógica (coluna).
        :param y: Coordenada lógica (linha).
        :param cor: Cor em formato hexadecimal, exemplo: "#FF0000".
        """
        tamanho = self.tamanho_pixel
        # Define as coordenadas do retângulo que representa o pixel ampliado
        x1 = x * tamanho
        y1 = y * tamanho
        x2 = x1 + tamanho
        y2 = y1 + tamanho

        # Desenha o retângulo no Canvas usando as coordenadas calculadas
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=cor, outline=cor)