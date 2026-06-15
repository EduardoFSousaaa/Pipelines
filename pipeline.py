from tkinter import *
from tkinter import ttk, Frame
# Certifique-se de que seu arquivo grafo.py está na mesma pasta
# pois a importação abaixo permanece necessária:
from grafo import * 
from clsPipeline import *

# 1. Fazendo a Application herdar corretamente de tk.Tk
class Application(Tk): 
    def __init__(self):
        super().__init__() # Inicializa a fiação interna do Tkinter corretamente
        
        # Definições de tamanho e centralização da Janela Principal
        largura = 800
        altura = 800
        largura_tela = self.winfo_screenwidth()
        altura_tela = self.winfo_screenheight()
        
        posicao_x = int((largura_tela / 2) - (largura / 2))
        posicao_y = int((altura_tela / 2.5) - (altura / 2.5))
        
        self.title("Pipeline Manager v1.0")
        self.geometry(f"{largura}x{altura}+{posicao_x}+{posicao_y}")
        
        # Passamos 'self' como o master dos widgets agora!
        self.fontePadrao = ("Arial", "10")
        
        self.barra_topo = Frame(self, bg="#f0f0f0")
        self.barra_topo.pack(side="left", fill="x", anchor="nw")
        
        self.btnMenu1 = Button(self.barra_topo, bg="violet")
        self.btnMenu1["text"] = "Nova Equipe"
        self.btnMenu1["font"] = ("Calibri", "8")
        self.btnMenu1["width"] = 12
        self.btnMenu1["command"] = self.abrir_janelaEquipes 
        self.btnMenu1.pack(side=LEFT ,anchor="w",fill="x", padx=2, pady=0)

        self.btnMenu2 = Button(self.barra_topo, bg="violet")
        self.btnMenu2["text"] = "Processamento de imagem"
        self.btnMenu2["font"] = ("Calibri", "8")
        self.btnMenu2["width"] = 12
        self.btnMenu2["command"] = self.abrir_janelaProcessamentoPipeline 
        self.btnMenu2.pack(anchor="w",fill="x", padx=2, pady=0)
        
        self.primeiroContainer = Frame(self, bg="blue")
        self.primeiroContainer["pady"] = 20
        self.primeiroContainer["padx"] = 5
        self.primeiroContainer.pack(side=LEFT, anchor=NW, padx=2, pady=0)
        
        self.SegundoContainer = Frame(self, bg="red")
        self.SegundoContainer["pady"] = 10
        self.SegundoContainer.pack(anchor=W)
        
        self.titulo = Label(self.primeiroContainer, text="Novo Pipeline", font=self.fontePadrao)
        self.titulo["font"] = ("Arial", "10", "bold")
        self.titulo.pack(side="left", anchor="w")
        
        self.qtdCelulaLabel = Label(self.SegundoContainer, text="Qtd de Células: ", font=self.fontePadrao)
        self.qtdCelulaLabel.pack(side="left")
        
        self.qtd_celulas = Entry(self.SegundoContainer, textvariable=StringVar(value="10"))
        self.qtd_celulas["width"] = 15
        self.qtd_celulas["font"] = self.fontePadrao
        self.qtd_celulas.pack(side=BOTTOM, anchor="e", padx=10, pady=10)
        
        self.terceiroContainer = Frame(self, bg="black")
        self.terceiroContainer["padx"] = 5
        self.terceiroContainer["pady"] = 5
        self.terceiroContainer.pack(side="top", anchor="w", padx=0)
        
        self.celulaLabel = Label(self.terceiroContainer, text="Celula:", font=self.fontePadrao)
        self.celulaLabel.pack(side="left", anchor=E)
        
        self.nomeCelula = Entry(self.terceiroContainer, textvariable=StringVar(value="A"))
        self.nomeCelula["width"] = 15
        self.nomeCelula["font"] = self.fontePadrao
        self.nomeCelula.pack(side="left", anchor=E)
        
        self.verticeLabel = Label(self.terceiroContainer, text="vertice:", font=self.fontePadrao)
        self.verticeLabel["width"] = 15
        self.verticeLabel.pack(side="left", anchor=W)
        
        self.vertice = Entry(self.terceiroContainer, textvariable=StringVar(value="B"))
        self.vertice["width"] = 15
        self.vertice["font"] = self.fontePadrao
        self.vertice.pack(side="left", anchor=W)
        
        self.quartoContainer = Frame(self, bg="violet")
        self.quartoContainer["pady"] = 20
        self.quartoContainer.pack(side=TOP, anchor="nw")
        
        self.btnNovaCelular = Button(self.terceiroContainer, bg="violet")
        self.btnNovaCelular["text"] = "Nova Célula"
        self.btnNovaCelular["font"] = ("Calibri", "8")
        self.btnNovaCelular["width"] = 12
        self.btnNovaCelular["command"] = self.NovaCelula
        self.btnNovaCelular.pack(anchor="e", padx=50, pady=0)
        
        self.mensagemTitulo = Label(self.quartoContainer, text="Mensageiro:", font=self.fontePadrao)
        self.mensagemTitulo.pack(side="top", anchor=CENTER)
        
        self.mensagem = Label(self.quartoContainer, text="", font=self.fontePadrao)
        self.mensagem.pack(side="top")
        
        self.quintoESQContainer = Frame(self)
        self.quintoESQContainer["pady"] = 25
        self.quintoESQContainer.pack(side=TOP, anchor="nw")
        
        self.quintoDIRContainer = Frame(self)
        self.quintoDIRContainer["pady"] = 25
        self.quintoDIRContainer.pack(side=LEFT, anchor="ne")
        
        self.CelulasLabel = Label(self.quintoESQContainer, text="Celulas:", font=self.fontePadrao, bg="lightblue")
        self.CelulasLabel.pack(side=LEFT, anchor="nw")
        
        self.TextoPipeline = Text(self.quintoESQContainer, height=15, width=40)
        self.TextoPipeline.pack(side=LEFT)
        
        self.GrafoLabel = Label(self.quintoDIRContainer, text="Grafo:", font=self.fontePadrao, bg="lightblue")
        self.GrafoLabel.pack(side=LEFT, anchor="ne")
        
        self.TextoGrafo = Text(self.quintoDIRContainer, height=15, width=40)
        self.TextoGrafo.pack(side=LEFT)
        
        self.pipeline = {"qtd_celulas": 0, "celulas": []}
        self.lstcelula = []
        self.Grafo = Grafo()
        self.equipes_cadastradas = {}
        self.dados_para_enviar = {"lstcelula": [], "grafo": self.Grafo.grafo,"equipes_cadastradas":self.equipes_cadastradas}
        
    def NovaCelula(self):
        qtdCelulas = self.obterQtdCelulas()
        celula = self.nomeCelula.get()
        vertice = self.vertice.get()
        if qtdCelulas == "" and not qtdCelulas.isnumeric():
            self.mensagem["text"] = "A quantidade de células é obrigatória. Por favor, preencha o campo com um numero."
        elif self.pipeline["celulas"].count(celula) >= 1:
            if self.Grafo.grafo.get(celula) is not None:
                # Modificado para evitar quebras se a estrutura interna do seu grafo variar
                self.addVertice(celula, vertice)
                self.mensagem["text"] = "Vértice processado na célula!"
        elif int(qtdCelulas) + 1 <= len(self.lstcelula) + 1 and celula not in ("0", 0, ""):
            self.mensagem["text"] = "A quantidade de células já foi atingida. Não é possível adicionar mais células."
        elif qtdCelulas != "" and (celula != "" or vertice != "" ):
            self.lstcelula.append(celula)
            self.pipeline["qtd_celulas"] = qtdCelulas
            self.addVertice(celula, vertice)
            strmensagem = "Nova célula criada com sucesso!"
            if vertice not in self.lstcelula:
                self.lstcelula.append(vertice)
                self.addVertice("",vertice)
                strmensagem += " O vertice virou uma nova celula TBM!"
            self.pipeline["celulas"] = self.lstcelula
            self.mensagem["text"] = strmensagem
            
            if self.pipeline["celulas"].count(self.vertice.get()) < 1:
                self.pipeline["celulas"].append(self.vertice.get())
        else:
            self.mensagem["text"] = "Erro na Criação da célula. Verifique os campos e tente novamente."
            
        self.TextoPipeline.delete("1.0", "end")
        self.TextoPipeline.insert("end", f"\n Quantidade de Células: {self.pipeline['qtd_celulas']}")
        self.TextoPipeline.insert("end", f"\n Células: {', '.join(self.pipeline['celulas'])}")
        
        self.TextoGrafo.delete("1.0", "end")
        #self.TextoGrafo.insert("end",self.pipeline['celulas'])
        self.TextoGrafo.insert("end", f"\n Grafo: {f'\n'.join(f'{key[0]}: {key[1]}' for key in self.Grafo.grafo.items())}")
        
        # Atualiza o dicionário mapeado corretamente com chaves string
        self.dados_para_enviar = {"lstcelula": self.lstcelula, "grafo": self.Grafo.grafo,"equipes_cadastradas":self.equipes_cadastradas}
        
    def obterQtdCelulas(self):
        return self.qtd_celulas.get()

    def addVertice(self, celula: str, vertice: str):
        dictGrafo = self.Grafo.grafo
        if celula != "" and celula not in dictGrafo:
            self.Grafo.adicionar_vertice(celula)
        if vertice != "" and vertice not in dictGrafo:
            self.Grafo.adicionar_vertice(vertice)
        if vertice != "" and celula != "":
            self.Grafo.adicionar_aresta(celula, vertice)

    def abrir_janelaEquipes(self):
        JanelaEquipes(self, self.dados_para_enviar,self.receber_dados_equipe)

    def abrir_janelaProcessamentoPipeline(self):
        JanelaProcessamentoDados(self,any,any)

    def receber_dados_equipe(self, nome_equipe, celula, operadores, maquinas):
        """Este método é chamado pela JanelaEquipes quando o usuário finaliza"""
        self.mensagem["text"] = f"Janela Principal recebeu: {nome_equipe} para a célula {celula}"
        
        # 1. Salva os dados no escopo da aplicação principal
        self.equipes_cadastradas[nome_equipe] = {
            "celula": celula,
            "operadores": operadores,
            "maquinas": maquinas
        }
        
        # 2. Exemplo: Atualiza seu painel de texto ou log na tela principal
        self.TextoPipeline.insert("end", f"\n-> Equipe {nome_equipe} alocada na Célula {celula}\n-> Operadores {operadores} \n-> maquinas {maquinas}")
class JanelaEquipes(Toplevel):
    def __init__(self, master, dicionario_objetos,callback_salvar):
        super().__init__(master)
        self.title("Montagem de Equipes")
        self.geometry("1000x800")
         # Passamos 'self' como o master dos widgets agora!
        self.fontePadrao = ("Arial", "10")
        self.callback_salvar = callback_salvar
        
        # INTERCEPTA O "X" DA JANELA: Quando o usuário clicar no X, chama o método self.ao_fechar
        self.protocol("WM_DELETE_WINDOW", self.ao_fechar)

        # Acessando via CHAVES STRINGS do seu dicionário estruturado
        self.lista_celulas = dicionario_objetos["lstcelula"]
        dados_grafo = dicionario_objetos["grafo"]
        self.DictEquipes_cadastradas = dicionario_objetos["equipes_cadastradas"]
        
        lbl1 = Label(self, text=f"Grafo ativo com {len(dados_grafo)} vértices.", font=("Arial", 11))
        lbl1.pack(pady=10)

        
        # Exibindo e montando os seletores baseados nas células
        if len(self.lista_celulas) > 0:
            self.PrimeiroContainer = Frame(self, bg="green")
            self.PrimeiroContainer["pady"] = 10
            self.PrimeiroContainer.pack(anchor=W)

            self.titulo = Label(self.PrimeiroContainer, text="Equipes Cadastradas:", font= self.fontePadrao)
            self.titulo["font"] = ("Arial", "10", "bold")
            self.titulo.pack(side="left", anchor="w")
            
            self.equipesCadastradas = Text(self.PrimeiroContainer,font= self.fontePadrao,width=40,height=10,state="disabled")
            self.equipesCadastradas["font"] = ("Arial", "10", "bold")
            self.texto_formatado = ""
            if self.DictEquipes_cadastradas!={}:
                for eq, dados in self.DictEquipes_cadastradas.items():
                    self.texto_formatado = f"Equipe: {eq}\n"
                    self.texto_formatado += f"  └─ Célula: {dados['celula']}\n"
                    self.texto_formatado += f"  └─ Operadores: {', '.join(dados['operadores'])}\n"
                    self.texto_formatado += f"  └─ Máquinas: {', '.join(dados['maquinas'])}\n"
                    self.texto_formatado += "-----------------------------\n"
            else: self.texto_formatado = str(dicionario_objetos)
            # Inserindo o texto formatado no final do componente
            self.equipesCadastradas.insert(END, self.texto_formatado)
            self.equipesCadastradas.pack(side="left", anchor="w")

            lbl2 = Label(self, text="Selecione uma Célula no Pipeline:", font=("Arial", 11, "bold"))
            lbl2.pack(anchor="w", padx=20, pady=5)
            
            # Valor padrão inicial do Radiobutton pega o primeiro elemento da lista
            self.opcao_selecionada = StringVar(value=str(self.lista_celulas[0]))
            
            # Corrigido: Desenhando os Radiobuttons dentro de 'self' (a janela Toplevel)
            for item_celula in self.lista_celulas:
                rb = Radiobutton(self, text=f"Célula {item_celula}", variable=self.opcao_selecionada, value=str(item_celula))
                rb.pack(anchor="w", padx=40, pady=2)
            
            self.SegundoContainer = Frame(self, bg="red")
            self.SegundoContainer["pady"] = 10
            self.SegundoContainer.pack(anchor=W)
            
            self.nomeEquipeLabel = Label(self.SegundoContainer, text="Nome da equipe: ", font=self.fontePadrao)
            self.nomeEquipeLabel.pack(side="left")
            
            self.nomeEquipe = Entry(self.SegundoContainer, textvariable=StringVar(value="Equipe 1"))
            self.nomeEquipe["width"] = 15
            self.nomeEquipe["font"] = self.fontePadrao
            self.nomeEquipe.pack(side=LEFT, anchor="e", padx=10, pady=10)
            
            self.capacidadeDeProducaoLabel = Label(self.SegundoContainer, text="Capacidade de Produção da equipe: ", font=self.fontePadrao)
            self.capacidadeDeProducaoLabel.pack(side="left")

            self.capacidadeDeProducao = Entry(self.SegundoContainer, textvariable=StringVar(value="50"))
            self.capacidadeDeProducao["width"] = 15
            self.capacidadeDeProducao["font"] = self.fontePadrao
            self.capacidadeDeProducao.pack(side=BOTTOM, anchor="e", padx=10, pady=10)

            self.terceiroContainer = Frame(self, bg="black")
            self.terceiroContainer["padx"] = 5
            self.terceiroContainer["pady"] = 5
            self.terceiroContainer.pack(side="top", anchor="w", padx=0)
            
            self.NovoOperadorLabel = Label(self.terceiroContainer, text="Novo Operador:", font=self.fontePadrao)
            self.NovoOperadorLabel.pack(side="left", anchor=E)
            
            self.NovoOperador = Entry(self.terceiroContainer, textvariable=StringVar(value="Operador 1"))
            self.NovoOperador["width"] = 15
            self.NovoOperador["font"] = self.fontePadrao
            self.NovoOperador.pack(side="left", anchor=E)
            
            self.NovaMaquinaLabel = Label(self.terceiroContainer, text="NovaMaquina:", font=self.fontePadrao)
            self.NovaMaquinaLabel["width"] = 15
            self.NovaMaquinaLabel.pack(side="left", anchor=W)
            
            self.NovaMaquina = Entry(self.terceiroContainer, textvariable=StringVar(value="B"))
            self.NovaMaquina["width"] = 15
            self.NovaMaquina["font"] = self.fontePadrao
            self.NovaMaquina.pack(side="left", anchor=W)
            
            self.quartoContainer = Frame(self,bg="violet")
            self.quartoContainer["pady"] = 20
            self.quartoContainer.pack(side=TOP, anchor="nw")
            
            self.lstoperadores = []
            self.lstMaquinas = []

            # BOTÃO 1: Apenas acumula nas listas e limpa os campos
            self.btnAdicionar = Button(self.terceiroContainer, text="Adicionar", bg="lightgreen", command=self.adicionar_integrante)
            self.btnAdicionar.pack(side="left", padx=10)
            
            # --- CONTAINER VISUAL (LISTA DE QUEM JÁ FOI ACUMULADO) ---
            self.containerLista = Frame(self)
            self.containerLista.pack(fill="both", expand=True, padx=10, pady=5)
            
            Label(self.containerLista, text="Integrantes Acumulados:", font=("Arial", 10, "bold")).pack(anchor="w")
            
            # Caixa de texto para o usuário ver quem ele já adicionou
            self.txtVisor = Text(self.containerLista, height=8, width=50, font=self.fontePadrao)
            self.txtVisor.pack(fill="x", pady=5)
            
            # BOTÃO 2: Envia a lista acumulada final para o grafo/sistema
            self.btnFinalizar = Button(self, text="Montar Equipe Final", bg="violet", font=("Arial", 11, "bold"), command=self.finalizar_equipe)
            self.btnFinalizar.pack(fill="x", padx=10, pady=10)
        else:
            lbl2 = Label(self, text="Sem Células registradas no Pipeline.", font=("Arial", 11))
            lbl2.pack(pady=15)

    def ao_fechar(self):
        if len(self.lista_celulas) > 0:
            nome_equipe = self.nomeEquipe.get().strip()
            celula = self.opcao_selecionada.get()
            # Só envia se o usuário pelo menos digitou um nome de equipe
            if nome_equipe:
                # Dispara o callback passando o que foi acumulado até agora
                self.callback_salvar(nome_equipe, celula, self.lstoperadores, self.lstMaquinas)
            else:
                print("Janela fechada sem nome de equipe. Nada foi enviado.")
            self.destroy()
        else: 
            self.callback_salvar(None, None, [], [])
            self.destroy()
    def adicionar_integrante(self):
        """Método focado estritamente em acumular os dados nas listas da instância"""
        operador = self.NovoOperador.get().strip()
        maquina = self.NovaMaquina.get().strip()
        
        # Acumula se o campo não estiver vazio e evita duplicados na memória
        if operador and (operador not in self.lstoperadores):
            self.lstoperadores.append(operador)
            
        if maquina and (maquina not in self.lstMaquinas):
            self.lstMaquinas.append(maquina)
            
        # Limpa os campos de texto para a próxima digitação
        self.NovoOperador.delete(0, END)
        self.NovaMaquina.delete(0, END)
        
        # Atualiza a tela para mostrar quem já está acumulado por referência
        self.txtVisor.delete("1.0", END)
        self.txtVisor.insert(END, f"Operadores: {', '.join(self.lstoperadores)}\n")
        self.txtVisor.insert(END, f"Máquinas: {', '.join(self.lstMaquinas)}\n")
    
    def finalizar_equipe(self):
       """Aproveita a mesma lógica de salvamento do método ao_fechar"""
       self.ao_fechar()
       
class JanelaProcessamentoDados(Toplevel):
    
    def __init__(self, master, dicionario_objetos,callback_salvar):
        from PIL import ImageFile
        from PIL import Image
        from PIL import Image, ImageTk
        super().__init__(master)
        self.title("Montagem de Equipes")
        self.geometry("1000x800")
        # Passamos 'self' como o master dos widgets agora!
        self.fontePadrao = ("Arial", "10")

        self.EntradaConteiner = Frame(self)
        self.EntradaConteiner["pady"] = 10
        self.EntradaConteiner.pack(side=LEFT,anchor=W)

        self.EntradaDeMateriais = StringVar(value=50)
        Label(self.EntradaConteiner,text="Entrada de materias(qtd)",).pack(side="left")
        Entry(self.EntradaConteiner,textvariable = self.EntradaDeMateriais).pack(side="left")
        Button(self.EntradaConteiner,text="Processar Entrada", width=15,command=self.btnProcessar).pack(side="left")
        lblMensagem = Label(self.EntradaConteiner,text="",)
        
        
    def btnProcessar(self):
        from PIL import ImageFile
        from PIL import Image
        from PIL import Image, ImageTk

        self.PrimeiroContainer = Frame(self)
        self.PrimeiroContainer["pady"] = 10
        self.PrimeiroContainer.pack(side=LEFT,anchor=W)
        
        # 1. Abre a imagem original (substitua pelo nome correto do seu arquivo)
        imagem_original = Image.open("triangulos.png")

        # 2. Define a altura fixa e a largura de cada bloco
        altura = 26
        largura_bloco = 35

        # 3. Faz o recorte de cada triângulo usando as coordenadas (esquerda, topo, direita, baixo)
        verde = imagem_original.crop((0, 0, largura_bloco, altura))
        amarelo = imagem_original.crop((largura_bloco, 0, largura_bloco * 2, altura))
        vermelho = imagem_original.crop((largura_bloco * 2, 0, largura_bloco * 3, altura))
        
        verde = ImageTk.PhotoImage(verde)
        amarelo = ImageTk.PhotoImage(amarelo)
        vermelho = ImageTk.PhotoImage(vermelho)
        self.frame_matriz = Frame(self.PrimeiroContainer, bg="lightgray")
        self.frame_matriz.pack(fill="both") 
        if int(self.EntradaDeMateriais.get()) > 0:
            # 3. For duplo para criar a matriz 5x10 (5 linhas e 10 colunas)
            entradaA= entrada(int(self.EntradaDeMateriais.get()),['a','b','c'],"ProcessoPadrão",{"A": {'A': 'A', 'vizinhos': ['B']}, "B": {'B': 'B', 'vizinhos': ['A', 'C']},"C": {'C': 'C', 'vizinhos': ['B']}})
            listaDeSaidas= entradaA.processaEmUnicoLote(celula)
            lstTuplesaidasContadas = Saida.ContarTipoDeSaida(listaDeSaidas)
            
            # Converte as divisões para inteiros usando '//'
            COLUNAS_MATRIZ = 5
            for i,saida in enumerate(listaDeSaidas):
                linha = i // COLUNAS_MATRIZ
                coluna = i % COLUNAS_MATRIZ
                imagem_definida = None

                if saida == Saida.PecaAcabada:
                    imagem_definida = verde
                elif saida == Saida.PontasDeEstoque:
                    imagem_definida = amarelo
                elif saida == Saida.Reciclagem:
                    imagem_definida = vermelho

                if imagem_definida:
                    # Criamos um único objeto Label genérico
                    label = Label(self.frame_matriz, image=imagem_definida, bd=0, padx=0, pady=0)
                    
                    # Posiciona dinamicamente usando a linha e coluna atuais do loop
                    label.grid(row=linha, column=coluna)
                    
                    # O SEGREDO DA REFERÊNCIA: Salva a imagem escolhida diretamente na propriedade interna do widget criado
                    label.image = imagem_definida   

            self.SegundoContainer = Frame(self)
            self.SegundoContainer["pady"] = 10
            self.SegundoContainer.pack(side="left",anchor="center")

            for tuple in lstTuplesaidasContadas:
                if tuple[0] == Saida.PecaAcabada.name and tuple[1] > 0:
                    Label(self.SegundoContainer, image=verde, bd=0, padx=0, pady=0).pack(side="left",anchor=W)
                    Label(self.SegundoContainer, text=" = " + str(tuple[1]), font=self.fontePadrao).pack(side="left",anchor=W)
                if tuple[0] == Saida.PontasDeEstoque.name and tuple[1] > 0:
                    Label(self.SegundoContainer, image=amarelo, bd=0, padx=0, pady=0).pack(side="left",anchor=W)
                    Label(self.SegundoContainer, text=" = " +str(tuple[1]), font=self.fontePadrao).pack(side="left",anchor=W)                
                if tuple[0] == Saida.Reciclagem.name and tuple[1] > 0:
                    Label(self.SegundoContainer, image=vermelho, bd=0, padx=0, pady=0).pack(side="left",anchor=W)
                    Label(self.SegundoContainer, text=" = " + str(tuple[1]), font=self.fontePadrao).pack(side="left",anchor=W)
        else:
            self.lblMensagem[Text]="Insira um numero maior que zero"
            self.lblMensagem.pack(side=LEFT)
            
            

