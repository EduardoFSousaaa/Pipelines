from tkinter import *
from tkinter.ttk import Frame
from pipeline import Application
from clsPipeline import *

def main() -> None:
    app = Application()
    app.mainloop()
    """NovoPipeline = Pipeline(1,"TurnoManha", 5, 100, tempoDeProducao(180, 60))
    novoGrafo = Grafo()
    tamanhoPipeline = NovoPipeline.tamanho
    ListaDeEntradas = []
    ListaDeCelulas = []
    ListaDeequipes = []
    NovaCelula = celula("Célula 1", 
                        entrada(10, [0, 1], "Processo Padrão"),
                        integrantesCelula("Equipe 1",
                                           ["Operador 1", "Operador 2"],
                                           ["Máquina 1", "Máquina 2"]),
                        [Saida.Default])
    for i in range(tamanhoPipeline):
        if i < tamanhoPipeline-1:
            novoGrafo.adicionar_aresta(i, i+1)
    for i in range(tamanhoPipeline):
        NovaCelula.nome = f"Célula {i+1}"
        NovaCelula.entrada = entrada(10, [i, i+1], "Processo Padrão")
        NovaEquipe = integrantesCelula(f"Equipe {i+1}", [f"Operador {i*2+1}", f"Operador {i*2+2}"],
                                       [f"Máquina {i*2+1}", f"Máquina {i*2+2}"])
        ListaDeCelulas.append(NovaCelula)
        ListaDeequipes.append(NovaEquipe)
        ListaDeEntradas.append(NovaCelula.entrada)
    print("Programa iniciado!")
    """
#if __name__ == "__main__":
main()
