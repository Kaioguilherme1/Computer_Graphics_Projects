import tkinter as tk
from tkinter import ttk
from interface import PixelMatrixApp


class MainApplication:
    def __init__(self, root):
        """Configura a janela principal."""
        self.root = root
        self.root.title("Comparação de Algoritmos de Rasterização")

        # Contêiner para as telas
        self.container = ttk.Frame(root)
        self.container.pack(fill=tk.BOTH, expand=True)

        # Botão para criação de novas telas
        self.add_btn = ttk.Button(root, text="Adicionar Tela", command=self.add_new_screen)
        self.add_btn.pack(side=tk.BOTTOM, pady=10)

        # Lista das instâncias criadas
        self.pixel_apps = []

        # Exemplo inicial com algoritmos específicos
        self.add_new_screen(
            obj=PixelMatrixApp, rows=100, cols=100, title="Algoritmo: Preenchimento", algorithm=sample_algorithm_1
        )
        self.add_new_screen(
            obj=PixelMatrixApp, rows=100, cols=100, title="Algoritmo: Linha", algorithm=sample_algorithm_2
        )

    def add_new_screen(self, obj, rows=64, cols=64, title="Nova Tela", algorithm=None):
        """Adiciona uma nova tela/objeto ao container."""
        app = obj(self.container, rows=rows, cols=cols, title=title, algorithm=algorithm)
        self.pixel_apps.append(app)


# Algoritmos de exemplo que serão passados para a classe
def sample_algorithm_1(app):
    """Exemplo de algoritmo que preenche toda a matriz linha a linha."""
    for row in range(app.rows):
        for col in range(app.cols):
            if not app.running:  # Parar se solicitado
                return
            app.color_pixel(row, col, "red")
            # time.sleep(0.01)  # Simula o tempo do processamento


def sample_algorithm_2(app):
    """Exemplo de algoritmo que desenha uma linha diagonal."""
    for i in range(min(app.rows, app.cols)):
        if not app.running:  # Parar se solicitado
            return
        app.color_pixel(i, i, "blue")
        # time.sleep(0.05)  # Simula o tempo do processamento


if __name__ == "__main__":
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()

