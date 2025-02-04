import tkinter as tk
from tkinter import ttk
import threading
import time


class MatrizDeRasterizacao:
    def __init__(self, pai, altura=64, largura=64, pixel_size=5, titulo="Tela", algoritmo=None):
        """
        Inicializa o objeto MatrixDeRasterizacao.

        :param pai: Container pai onde a tela será embutida.
        :param altura: Número de linhas da matriz.
        :param largura: Número de colunas da matriz.
        :param pixel_size: Tamanho de cada pixel (em pixels).
        :param titulo: Título que identifica esta tela.
        :param algoritmo: Função do algoritmo a ser executado, passada como callback.
        """
        self.pai = pai
        self.altura = altura
        self.largura = largura
        self.pixel_size = pixel_size
        self.executando = False  # Controla a execução do algoritmo
        self.algoritmo = algoritmo  # Define a função do algoritmo a ser usado
        self.pixel_map = {}

        if self.algoritmo is None:
            raise ValueError("É necessário passar uma função 'algoritmo' para a execução.")

        # Moldura que contém a tela
        self.moldura = ttk.Frame(pai, padding=5)
        self.moldura.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Nome/título da tela
        self.rotulo = ttk.Label(self.moldura, text=titulo, font=("Arial", 12, "bold"))
        self.rotulo.pack(pady=5)

        # Matriz (Canvas) onde os pixels são desenhados
        self.canvas = tk.Canvas(self.moldura, width=largura * pixel_size, height=altura * pixel_size, bg="white")
        self.canvas.pack()

        self.imagem = tk.PhotoImage(width=self.altura * pixel_size, height=self.largura * pixel_size)
        self.canvas.create_image((0, 0), image=self.imagem, anchor=tk.NW)

        # Rótulo do cronômetro logo abaixo
        self.rotulo_cronometro = ttk.Label(self.moldura, text="Tempo decorrido: 0.00s", font=("Arial", 12),
                                           anchor="center")
        self.rotulo_cronometro.pack(fill=tk.X, padx=10, pady=5)


        # # Rótulo do Consumo de CPU logo abaixo
        # self.rotulo_cpu = ttk.Label(self.moldura, text="Consumo de CPU: 0 %", font=("Arial", 12),
        #                                    anchor="center")
        # self.rotulo_cpu.pack(fill=tk.X, padx=10, pady=5)
        # # Rótulo do Consumo de Memoria logo abaixo
        # self.rotulo_memoria = ttk.Label(self.moldura, text="Consumo de Memoria: 0 Mb", font=("Arial", 12),
        #                             anchor="center")
        # self.rotulo_memoria.pack(fill=tk.X, padx=10, pady=5)

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

        # Atualiza o texto do cronômetro associado a esta tela
        self.rotulo_cronometro.config(text=f"Tempo decorrido: {tempo_decorrido:.8f}s")

        ## ------------------------------ requer paralelismo para coletar estas informações ----------------------------
        # #Coleta os dados de CPU e memória
        # processo = psutil.Process(os.getpid())  # Pega informações do processo atual
        # uso_cpu = processo.cpu_percent(interval=0.1)  # % de CPU usado
        # uso_memoria = processo.memory_info().rss / (1024 * 1024)  # Memória em MB
        #
        # # Atualiza o texto na tela
        # self.rotulo_cpu.config(text=f"Consumo de CPU: {uso_cpu} %")
        # self.rotulo_memoria.config(text=f"Consumo de Memoria: {uso_memoria} MB")
        ## -------------------------------------------------------------------------------------------------------------

        # Continua atualizando enquanto o algoritmo da tela ainda estiver em execução
        if self.executando:
            # Repete a atualização após 100 ms
            self.rotulo_cronometro.after(100, self._atualizar_cronometro)

    def reiniciar(self):
        """Interrompe a execução e limpa o ambiente."""
        if self.executando:  # Verifica se a thread está em execução
            print("Interrompendo a thread...")
            self.executando = False  # Sinaliza à thread que deve parar

            if self.thread:  # Garante que há uma thread em execução
                self.thread.join()  # Aguarda o término seguro da thread

        # Limpeza ou reinicialização de outros elementos
        self.canvas.delete("all")
        print(f"Tela reiniciada: {self.rotulo['text']}")


    def color_pixel(self, x, y, cor):
        """
        Desenha um pixel ampliado no Canvas.

        :param x: Coordenada lógica (coluna).
        :param y: Coordenada lógica (linha).
        :param cor: Cor em formato hexadecimal, exemplo: "#FF0000".
        """
        tamanho = self.pixel_size
        # Define as coordenadas do retângulo que representa o pixel ampliado
        x1 = x * tamanho
        y1 = y * tamanho
        x2 = x1 + tamanho
        y2 = y1 + tamanho

        # Desenha o retângulo no Canvas usando as coordenadas calculadas
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=cor, outline=cor)
        # salva o pixel
        self.pixel_map[(x, y)] = cor

    def get_pixel(self, x, y):
        """
        Verifica a cor pintada no Canvas em uma posição (x, y).
        """
        return self.pixel_map.get((x, y), "white")  # Branco como padrão
