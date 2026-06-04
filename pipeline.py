from logging import root
from tkinter import *
from tkinter  import ttk,Frame
class Application:
    def __init__(self, master=None):
        self.fontePadrao = ("Arial", "10")
        self.primeiroContainer = Frame(master)
        self.primeiroContainer["pady"] = 10
        self.primeiroContainer.pack()

        self.segundoContainer = Frame(master)
        self.segundoContainer["padx"] = 10
        self.segundoContainer.pack()

        self.terceiroContainer = Frame(master)
        self.terceiroContainer["padx"] = 20
        self.terceiroContainer.pack()

        self.quartoContainer = Frame(master)
        self.quartoContainer["pady"] = 20
        self.quartoContainer.pack()

        self.quintoContainer = Frame(master)
        self.quintoContainer["pady"] = 20
        self.quintoContainer.pack()

        self.titulo = Label(self.primeiroContainer, text="Novo Pipeline", font=self.fontePadrao)
        self.titulo["font"] = ("Arial", "10", "bold")
        self.titulo.pack()

        self.qtdCelulaLabel = Label(self.segundoContainer,text="Qtd de Células", font=self.fontePadrao)
        self.qtdCelulaLabel.pack(side=LEFT)

        self.qtd_celulas = Entry(self.segundoContainer)
        self.qtd_celulas["width"] = 15
        self.qtd_celulas["font"] = self.fontePadrao
        self.qtd_celulas.pack(side=LEFT)

        self.celulaLabel = Label(self.terceiroContainer, text="Celula:", font=self.fontePadrao)
        self.celulaLabel.pack(side=LEFT)

        self.nomeCelula = Entry(self.terceiroContainer)
        self.nomeCelula["width"] = 30
        self.nomeCelula["font"] = self.fontePadrao
        self.nomeCelula.pack(side=LEFT)

        self.NovaCelular = Button(self.quartoContainer)
        self.NovaCelular["text"] = "Nova Célula"
        self.NovaCelular["font"] = ("Calibri", "8")
        self.NovaCelular["width"] = 12
        self.NovaCelular["command"] = self.NovaCelula
        self.NovaCelular.pack()

        self.TextoPipeline = Text(self.quintoContainer, height=10, width=40)
        self.TextoPipeline.pack()

        self.pipeline = {"qtd_celulas": 0, "celulas": []}
        self.lstcelula = []
        self.mensagem = Label(self.quartoContainer, text="", font=self.fontePadrao)
        self.mensagem.pack()
        
    #Método verificar senha
    def NovaCelula(self):
        qtdCelulas = self.obterQtdCelulas()
        celula = self.nomeCelula.get()
        if qtdCelulas >= len(self.pipeline['celulas']):
             self.mensagem["text"] = "A quantidade de células já foi atingida. Não é possível adicionar mais células."  
        elif qtdCelulas != "" and  celula != "":
            self.lstcelula.append(celula)
            self.pipeline["qtd_celulas"] = qtdCelulas
            self.pipeline["celulas"] = self.lstcelula
            self.mensagem["text"] = "Nova célula criada com sucesso!"
            # Função para inserir texto no final
            self.TextoPipeline.delete("1.0", "end")  
            self.TextoPipeline.insert("end", f"\n Quantidade de Células: {self.pipeline['qtd_celulas']}")
            self.TextoPipeline.insert("end", f"\n Células: {', '.join(self.pipeline['celulas'])}")
        else:
            self.mensagem["text"] = "Erro na Criação da célula. Verifique os campos e tente novamente."
    def obterQtdCelulas(self):
        return self.qtd_celulas.get()