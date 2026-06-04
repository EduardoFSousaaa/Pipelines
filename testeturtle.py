import tkinter as tk
from turtle import TurtleScreen, RawTurtle

def desenhar_quadrado():
    """Função chamada pelo botão da interface"""
    for _ in range(4):
        tartaruga.forward(10)
        tartaruga.right(90)

# 1. Configuração da Janela Principal
janela = tk.Tk()
janela.title("Interface com Turtle e Tkinter")
janela.geometry("600x500")

# 2. Área do Turtle (Canvas)
canvas = tk.Canvas(janela, width=500, height=400, bg="lightgrey")
canvas.pack(pady=10)

# 3. Integração do Turtle no Canvas do Tkinter
tela_turtle = TurtleScreen(canvas)
tartaruga = RawTurtle(tela_turtle)
tartaruga.shape("turtle")

# 4. Botões e Elementos da Interface
botao_desenhar = tk.Button(janela, text="Desenhar Quadrado", command=desenhar_quadrado)
botao_desenhar.pack(pady=10)

botao_limpar = tk.Button(janela, text="Limpar Tela", command=tartaruga.clear)
botao_limpar.pack()

# 5. Loop principal da interface
janela.mainloop()
