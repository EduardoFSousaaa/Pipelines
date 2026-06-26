from tkinter import *
from tkinter import ttk, Frame
# Certifique-se de que seu arquivo grafo.py está na mesma pasta
# pois a importação abaixo permanece necessária:
from grafo import * 
from clsPipeline import *
from copy import deepcopy

# aplicação, tela Principal
class Application(Tk): 
    def __init__(self):
        super().__init__() # Inicializa a fiação interna do Tkinter corretamente
        
        # Definições de tamanho e centralização da Janela Principal
        largura = 850
        altura = 850
        largura_tela = self.winfo_screenwidth()
        altura_tela = self.winfo_screenheight()
        
        posicao_x = int((largura_tela / 2) - (largura / 2))
        posicao_y = int((altura_tela / 2.5) - (altura / 2.5))
        
        self.title("Pipeline Manager v1.0")
        self.geometry(f"{largura}x{altura}+{posicao_x}+{posicao_y}")
        self.minsize(750, 750)
        # Passamos 'self' como o master dos widgets agora!
        self.fontePadrao = ("Arial", "10")
        
        # 1. CRIAÇÃO DO CONTAINER PRINCIPAL (Mestre de todos)
        self.MasterFrame = Frame(self)
        self.MasterFrame.pack(fill=BOTH, expand=True)

        # 2. CRIAÇÃO DA SCROLLBAR VERTICAL
        self.ScrollbarJanela = Scrollbar(self.MasterFrame, orient=VERTICAL)
        self.ScrollbarJanela.pack(side=RIGHT, fill=Y)

        # 3. CRIAÇÃO DO CANVAS (Área rolável)
        self.CanvasJanela = Canvas(
            self.MasterFrame, 
            yscrollcommand=self.ScrollbarJanela.set,
            highlightthickness=0
        )
        self.CanvasJanela.pack(side=LEFT, fill=BOTH, expand=True)

        # Conecta a barra de rolagem ao movimento do Canvas
        self.ScrollbarJanela.config(command=self.CanvasJanela.yview)

        # 4. O FRAME CONTEÚDO (Onde você vai colocar seus containers e widgets)
        self.ConteudoJanela = Frame(self.CanvasJanela)

        # Insere o Frame de conteúdo dentro do Canvas
        self.CanvasWindowID = self.CanvasJanela.create_window(
            (0, 0), 
            window=self.ConteudoJanela, 
            anchor="nw"
        )

        # 5. CONFIGURAÇÃO DOS EVENTOS DE REDIMENSIONAMENTO
        # Atualiza a área de rolagem sempre que novos widgets forem adicionados
        def configurar_scroll(event):
            self.CanvasJanela.configure(scrollregion=self.CanvasJanela.bbox("all"))

        self.ConteudoJanela.bind("<Configure>", configurar_scroll)

        # Garante que o frame interno tenha a mesma largura do Canvas
        def configurar_largura(event):
            self.CanvasJanela.itemconfig(self.CanvasWindowID, width=event.width)

        self.CanvasJanela.bind("<Configure>", configurar_largura)

        # Suporte para Windows e MacOS (Roda do mouse)
        def _on_mousewheely(event):
            # No Windows o evento usa .delta, no Linux usa botões específicos
            self.CanvasJanela.yview_scroll(int(-1*(event.delta/120)), "units")

        # Vincula o scroll do mouse à janela inteira
        self.CanvasJanela.bind_all("<MouseWheel>", _on_mousewheely)
        
        self.barra_topo = Frame(self.ConteudoJanela, bg="#f0f0f0")
        self.barra_topo.pack(side="top", fill="x", anchor="nw")
        
        self.btnMenu1 = Button(self.barra_topo, bg="violet")
        self.btnMenu1["text"] = "Nova Equipe"
        self.btnMenu1["font"] = ("Calibri", "8")
        self.btnMenu1["width"] = 20
        self.btnMenu1["command"] = self.abrir_janelaEquipes 
        self.btnMenu1.pack(side=LEFT ,anchor="w",fill="x", padx=2, pady=0)

        self.btnMenu2 = Button(self.barra_topo, bg="violet")
        self.btnMenu2["text"] = "Processamento de imagem"
        self.btnMenu2["font"] = ("Calibri", "8")
        self.btnMenu2["width"] = 20
        self.btnMenu2["command"] = self.abrir_janelaProcessamentoPipeline 
        self.btnMenu2.pack(side=LEFT ,anchor="w",fill="x", padx=2, pady=0)
        
        self.frame_titulo = Frame(self.ConteudoJanela, bg="#f4f4f4")
        self.frame_titulo.pack(side=TOP, fill=BOTH, expand=False, padx=5, pady=5)

        self.titulo = Label(self.frame_titulo, text="Novo Pipeline", font=self.fontePadrao)
        self.titulo["font"] = ("Arial", "10", "bold")
        self.titulo.pack(anchor="center")

        self.frame_conteudo = Frame(self.ConteudoJanela, bg="#f4f4f4")
        self.frame_conteudo.pack(side=TOP, fill=None, expand=True, padx=10, pady=10)

        self.primeiroContainer = Frame(self.frame_conteudo, bg="red")
        self.primeiroContainer["pady"] = 20
        self.primeiroContainer["padx"] = 5
        self.primeiroContainer.pack(side="top",fill="both", anchor=W, padx=2, pady=0)
        
        self.qtdCelulaLabel = Label(self.primeiroContainer, text="Qtd de Células: ", font=self.fontePadrao)
        self.qtdCelulaLabel.pack(side="left")
        
        self.qtd_celulas = Entry(self.primeiroContainer, textvariable=StringVar(value="3"))
        self.qtd_celulas["width"] = 15
        self.qtd_celulas["font"] = self.fontePadrao
        self.qtd_celulas.pack(side="left", anchor="e", padx=10, pady=10)

        self.btnCaminhosPipeline = Button(self.primeiroContainer, bg="violet")
        self.btnCaminhosPipeline["text"] = "Criar Caminhos de pipeline"
        self.btnCaminhosPipeline["font"] = ("Calibri", "8")
        self.btnCaminhosPipeline["width"] = 30
        self.btnCaminhosPipeline["command"] = self.ConfigureCaminhos
        self.btnCaminhosPipeline.pack(anchor="e", padx=50, pady=0)

        self.SegundoContainer = Frame(self.frame_conteudo, bg="red")
        self.SegundoContainer["pady"] = 10
        self.SegundoContainer.pack(anchor=W,fill="both")

        self.celulaStartLabel = Label(self.SegundoContainer, text="Inicio Pipeline:", font=self.fontePadrao)
        self.celulaStartLabel.pack(side="left", anchor=E)
        
        self.celulaStart = Entry(self.SegundoContainer, textvariable=StringVar(value="A"))
        self.celulaStart["width"] = 15
        self.celulaStart["font"] = self.fontePadrao
        self.celulaStart.pack(side="left", anchor=E)
        
        self.celulaEndLabel = Label(self.SegundoContainer, text="Final Pipeline:", font=self.fontePadrao)
        self.celulaEndLabel["width"] = 15
        self.celulaEndLabel.pack(side="left", anchor=W)
        
        self.CelulaEnd = Entry(self.SegundoContainer, textvariable=StringVar(value="B"))
        self.CelulaEnd["width"] = 15
        self.CelulaEnd["font"] = self.fontePadrao
        self.CelulaEnd.pack(side="left", anchor=W)
        
        self.terceiroContainer = Frame(self.frame_conteudo, bg="black")
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
        
        self.quartoContainer = Frame(self.frame_conteudo, bg="violet")
        self.quartoContainer["pady"] = 20
        self.quartoContainer.pack(side=TOP,fill="both", anchor="nw")
        
        self.btnNovaCelular = Button(self.terceiroContainer, bg="violet")
        self.btnNovaCelular["text"] = "Nova Célula"
        self.btnNovaCelular["font"] = ("Calibri", "8")
        self.btnNovaCelular["width"] = 12
        self.btnNovaCelular["command"] = self.NovaCelula
        self.btnNovaCelular.pack(anchor="e", padx=50, pady=0)
        
        self.mensagemTitulo = Label(self.quartoContainer, text="Mensageiro:", font=self.fontePadrao)
        self.mensagemTitulo.pack(side="top", fill="both", anchor=CENTER)
        
        self.mensagem = Label(self.quartoContainer, text="", font=self.fontePadrao)
        self.mensagem.pack(side="top")
        
        self.quintoESQContainer = Frame(self.frame_conteudo)
        self.quintoESQContainer["pady"] = 25
        self.quintoESQContainer.pack(side=TOP, anchor="nw")
        
        self.quintoDIRContainer = Frame(self.frame_conteudo)
        self.quintoDIRContainer["pady"] = 25
        self.quintoDIRContainer.pack(side=LEFT, anchor="ne")
        
        self.CelulasLabel = Label(self.quintoESQContainer, text="Celulas:", font=self.fontePadrao, bg="lightblue")
        self.CelulasLabel.pack(side=LEFT, anchor="nw")
        
        self.TextoPipeline = Text(self.quintoESQContainer, height=20, width=60)
        self.TextoPipeline.pack(side=LEFT)
        
        self.GrafoLabel = Label(self.quintoDIRContainer, text="Grafo:", font=self.fontePadrao, bg="lightblue")
        self.GrafoLabel.pack(side=LEFT, anchor="ne",expand=TRUE)
        
        self.TextoGrafo = Text(self.quintoDIRContainer, height=20, width=80)
        self.TextoGrafo.pack(side=LEFT,expand=TRUE)
        
        self.pipeline = {"qtd_celulas": 0, "celulas": []}
        self.lstcelula = []
        self.Grafo = Grafo()
        self.equipes_cadastradas = {}
        self.dados_para_enviar = {"lstcelula": [], "grafo": self.Grafo.grafo,"equipes_cadastradas":self.equipes_cadastradas}
    
    #função configura caminhos
    def ConfigureCaminhos(self):
        self.mensagem["text"] ="Gerando Caminhos do pipeline..."

        qtdCelulas = self.obterQtdCelulas()
        self.start = self.celulaStart.get().upper()
        self.end = self.CelulaEnd.get().upper()
        if self.start != "":
            self.Grafo.adicionar_verticeStart(self.start)
        else: self.mensagem["text"] = "Insira uma celula Para ser a Inicial do Pipeline.";return

        if self.end != "":
            self.Grafo.adicionar_verticeEnd(self.end)
        else: self.mensagem["text"] = "Insira uma celula Para ser a Final do Pipeline.";return
        if len(self.lstcelula) <= int(qtdCelulas):
            self.Grafo.caminhosDoPipeline()
            if self.Grafo.caminhosEnd != []:
                self.TextoPipeline.delete("1.0", "end")
                self.TextoPipeline.insert("end", f"\n Caminho {self.Grafo.caminhosEnd}")
                self.caminhosEnd = self.Grafo.caminhosEnd
            else: self.mensagem["text"] ="sem Caminhos que levam ao Final do Pipeline.";return
        else:
            srtCaminhoErro = " Não foi possivel gerar caminho."
            self.mensagem["text"] ="Mais celulas permitidas pelo pipeline,"+ srtCaminhoErro
            return
        
        return "ok"    
    def NovaCelula(self):
        qtdCelulas = self.obterQtdCelulas()
        celula = self.nomeCelula.get().upper()
        vertice = self.vertice.get().upper()
        start = self.celulaStart.get().upper()
        end = self.CelulaEnd.get().upper()

        if start != "":
            self.Grafo.adicionar_verticeStart(start)
        else: 
            self.mensagem["text"] = "Insira uma celula Para ser a Inicial do Pipeline."; return


        if end != "":
            self.Grafo.adicionar_verticeEnd(end)
        else: 
            self.mensagem["text"] = "Insira uma celula Para ser a Final do Pipeline."; return

        if qtdCelulas == "" and not qtdCelulas.isnumeric():
            self.mensagem["text"] = "A quantidade de células é obrigatória. Por favor, preencha o campo com um numero."
            return
        if self.pipeline["celulas"].count(celula) >= 1:
            if self.Grafo.grafo.get(celula) is not None:
                # Modificado para evitar quebras se a estrutura interna do seu grafo variar
                self.addVertice(celula, vertice)
                self.mensagem["text"] = "Vértice processado na célula!"
        elif int(qtdCelulas) + 1 <= len(self.lstcelula) + 1 and celula not in ("0", 0, ""):
            self.mensagem["text"] = "A quantidade de células já foi atingida. Não é possível adicionar mais células."
            return
        if qtdCelulas != "" and (celula != "" or vertice != "" ):
            if celula not in self.lstcelula:
                if int(qtdCelulas)>= len(self.lstcelula) + 1 and celula not in ("0", 0, ""):
                    self.lstcelula.append(celula)
                else: 
                    self.mensagem["text"] = "A quantidade de células já foi atingida. Não é possível adicionar mais células."; return
            if vertice not in self.lstcelula:
                if int(qtdCelulas) >= len(self.lstcelula) + 1 and vertice not in ("0", 0, ""):
                    self.lstcelula.append(vertice)
                else: 
                    self.mensagem["text"] = "A quantidade de células já foi atingida. Não é possível adicionar mais células."; return
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
            self.mensagem["text"] = "Erro na Criação da célula. Verifique os campos e tente novamente.";return
            
        self.TextoPipeline.delete("1.0", "end")
        self.TextoPipeline.insert("end", f"\n Maximo de celulas do pipeline: {self.pipeline['qtd_celulas']}")
        self.TextoPipeline.insert("end", f"\n Células: {', '.join(self.pipeline['celulas'])}")
        
        self.TextoGrafo.delete("1.0", "end")
        #self.TextoGrafo.insert("end",self.pipeline['celulas'])
        self.TextoGrafo.insert("end", f"\n Grafo: {f'\n'.join(f'{key[0]}: {key[1]}' for key in self.Grafo.grafo.items())}")
        
    def obterQtdCelulas(self):
        return self.qtd_celulas.get()

    def addVertice(self, celula: str, vertice: str):
        celula = celula.upper()
        vertice = vertice.upper()
        dictGrafo = self.Grafo.grafo
        if celula != "" and celula not in dictGrafo:
            self.Grafo.adicionar_vertice(celula)
        if vertice != "" and vertice not in dictGrafo:
            self.Grafo.adicionar_vertice(vertice)
        if vertice != "" and celula != "":
            self.Grafo.adicionar_aresta(celula, vertice)

    def abrir_janelaEquipes(self):
        # Atualiza o dicionário mapeado corretamente com chaves string
        self.dados_para_enviar = {"lstcelula": self.lstcelula, "grafo": self.Grafo.grafo,"equipes_cadastradas":self.equipes_cadastradas}
        JanelaEquipes(self, self.dados_para_enviar,self.receber_dados_equipe)

    def abrir_janelaProcessamentoPipeline(self):

        strRetorno = self.ConfigureCaminhos()
        if strRetorno == "ok":
            dictObjetos = {"grafo":self.Grafo,"START":self.start,"END":self.end,"CaminhoPipeline":self.caminhosEnd }
            JanelaProcessamentoDados(self,dictObjetos,any)
        else:
            self.mensagem["text"] = "Não foi possivel gerar caminho"
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
#janela de equipes
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
            #Dicionario equipes cadastradas
            if self.DictEquipes_cadastradas!={}:
                for eq, dados in self.DictEquipes_cadastradas.items():
                    self.texto_formatado += f"Equipe: {eq}\n"
                    self.texto_formatado += f"  - Célula: {dados['celula']}\n"
                    self.texto_formatado += f"  - Operadores: {', '.join(dados['operadores'])}\n"
                    self.texto_formatado += f"  - Máquinas: {', '.join(dados['maquinas'])}\n"
                    self.texto_formatado += "-----------------------------\n"
                self.numeroEquipe = len(self.DictEquipes_cadastradas.items())
            else: 
                self.numeroEquipe = 0
                self.texto_formatado = "Nenhuma No Momento"
            # Inserindo o texto formatado no final do componente
            self.equipesCadastradas.config(state="normal")
            self.equipesCadastradas.insert(END, str(self.texto_formatado))
            self.equipesCadastradas.config(state="disabled")
            self.equipesCadastradas.pack(side="left",fill="both",expand=True, anchor="w")

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
            
            self.nomeEquipe = Entry(self.SegundoContainer, textvariable=StringVar(value=F"Equipe{self.numeroEquipe}"))
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
            self.txtVisor = Text(self.containerLista, height=8, width=50, font=self.fontePadrao,state="disabled")
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
        
        #Hbilita Para edições
        self.txtVisor.config(state="normal")
        # Limpa os campos de texto para a próxima digitação
        self.NovoOperador.delete(0, END)
        self.NovaMaquina.delete(0, END)
        
        # Atualiza a tela para mostrar quem já está acumulado por referência
        self.txtVisor.delete("1.0", END)
        self.txtVisor.insert(END, f"Operadores: {', '.join(self.lstoperadores)}\n")
        self.txtVisor.insert(END, f"Máquinas: {', '.join(self.lstMaquinas)}\n")
        
        #Desabilita para edições(state inicial)
        self.txtVisor.config(state="disabled")
    
    def finalizar_equipe(self):
       """Aproveita a mesma lógica de salvamento do método ao_fechar"""
       self.ao_fechar()
#janela de processamento de dados    
class JanelaProcessamentoDados(Toplevel):
    def __init__(self, master, dicionario_objetos,callback_salvar):
        from PIL import ImageFile
        from PIL import Image
        from PIL import Image, ImageTk

        super().__init__(master)
        self.title("Processamento de dados")
        self.geometry("1000x800")
        # Passamos 'self' como o master dos widgets agora!
        self.fontePadrao = ("Arial", "10")
        self.fontePadraoMaior = ("Arial", "14")

        self.start = dicionario_objetos["START"]
        self.end = dicionario_objetos["END"]
        self.CaminhoDoPiPeLine = list(dicionario_objetos["CaminhoPipeline"])
        self.EntradaConteiner = Frame(self)
        self.EntradaConteiner["pady"] = 10
        self.EntradaConteiner.pack(side=TOP,anchor=NW,fill="both")

        self.SegundoContainer = Frame(self.EntradaConteiner, bg="red")
        self.SegundoContainer["pady"] = 10
        self.SegundoContainer.pack(anchor=W,fill="both")

        self.celulaStartLabel = Label(self.SegundoContainer, text="Inicio Pipeline: " + self.start, font=self.fontePadrao)
        self.celulaStartLabel.pack(side="left", anchor=W)
        
        self.celulaEndLabel = Label(self.SegundoContainer, text="Final Pipeline: " + self.end, font=self.fontePadrao)
        self.celulaEndLabel["width"] = 15
        self.celulaEndLabel.pack(side="left", anchor=W)

        self.CaminhoLabel = Label(self.SegundoContainer, text=f"Caminho Pipeline: [{ ",".join(str(item) for item in self.CaminhoDoPiPeLine)}]", font=self.fontePadrao)
        self.CaminhoLabel["width"] = 100
        self.CaminhoLabel.pack(side="left", fill=BOTH, anchor=W)

        self.EntradaDeMateriais = StringVar(value=50)
        Label(self.EntradaConteiner,text="Entrada de materias(qtd)",).pack(side="left")
        Entry(self.EntradaConteiner,textvariable = self.EntradaDeMateriais).pack(side="left")
        Button(self.EntradaConteiner,text="Processar Entrada", width=15,command=self.btnProcessar).pack(side="bottom")
        lblMensagem = Label(self.EntradaConteiner,text="",)

        # 1. CRIAÇÃO DO CONTAINER PRINCIPAL (Mestre de todos)
        self.MasterFrame = Frame(self)
        self.MasterFrame.pack(fill=BOTH, expand=True)

        # 2. CRIAÇÃO DA SCROLLBAR VERTICAL
        self.ScrollbarJanela = Scrollbar(self.MasterFrame, orient="horizontal")
        self.ScrollbarJanela.pack(side="bottom", fill="x")

        # 3. CRIAÇÃO DO CANVAS (Área rolável)
        self.CanvasJanela1 = Canvas(
            self.MasterFrame, 
            xscrollcommand=self.ScrollbarJanela.set,
            highlightthickness=0
        )
        self.CanvasJanela1.pack(side=LEFT, fill=BOTH, expand=True)

        # Conecta a barra de rolagem ao movimento do Canvas
        self.ScrollbarJanela.config(command=self.CanvasJanela1.yview)

        # 4. O FRAME CONTEÚDO (Onde você vai colocar seus containers e widgets)
        self.ConteudoJanela = Frame(self.CanvasJanela1)

        # Insere o Frame de conteúdo dentro do Canvas
        self.CanvasWindowID = self.CanvasJanela1.create_window(
            (0, 0), 
            window=self.ConteudoJanela, 
            anchor="nw"
        )

        # 5. CONFIGURAÇÃO DOS EVENTOS DE REDIMENSIONAMENTO
        # Atualiza a área de rolagem sempre que novos widgets forem adicionados
        def configurar_scroll(event):
            self.CanvasJanela1.configure(scrollregion=self.CanvasJanela1.bbox("all"))

        self.ConteudoJanela.bind("<Configure>", configurar_scroll)

        # Suporte para Windows e MacOS (Roda do mouse)
        def _on_mousewheelX(event):
            # No Windows o evento usa .delta, no Linux usa botões específicos
            self.CanvasJanela1.xview_scroll(int(-1*(event.delta/120)), "units")

        # Vincula o scroll do mouse à janela inteira
        self.CanvasJanela1.bind_all("<MouseWheel>", _on_mousewheelX)

        self.ProcessarDadosConteiner = Frame(self.EntradaConteiner)
        self.ProcessarDadosConteiner["pady"] = 10
        self.ProcessarDadosConteiner.pack(side="bottom",anchor=W)

    def btnProcessar(self):
        self.dictParaProximaEntrada = {"ProximaCelulaAtual" : "",
                                  "listaDeSaidas":[],
                                  "lstTuplesaidasContadas":{()},
                                  "ProximaQtdEntradaMaterial":0
                                  }
        for filho in self.ConteudoJanela.winfo_children():
            filho.destroy()
        
        #start=self.start
        #caminho = self.CaminhoDoPiPeLine
        #end=self.end
        boolProUltSaida=False
        self.PrimeiraEntrada = True
        self.dicionarioProcessamento = {}
        self.intCelulasProcessadas = -1
        self.GerarNovaEntradaMateria(int(self.EntradaDeMateriais.get()))
        while(boolProUltSaida==False):
            boolProUltSaida=self.DesenharSaidasDoProcesso(self.listaDeSaidas,self.lstTuplesaidasContadas)
            self.PrimeiraEntrada = False
            qtd_proxima = int(self.dictParaProximaEntrada["ProximaQtdEntradaMaterial"])
            self.GerarNovaEntradaMateria(qtd_proxima)
        if self.intCelulasProcessadas>=0:
            self.DesenharFimDoProcessamento()
            
    #Monta o novo dado da class de entrada de materiais 
    def GerarNovaEntradaMateria(self, qtdMaterialEntrada: int):
        if qtdMaterialEntrada > 0:
            # 3. For duplo para criar a matriz 5x10 (5 linhas e 10 colunas)
            grafo = {"A": {'A': 'A', 'vizinhos': ['B']}, "B": {'B': 'B', 'vizinhos': ['A', 'C']},"C": {'C': 'C', 'vizinhos': ['B']}}

            self.intCelulasProcessadas += 1 
            
            # CRIAMOS UM NOVO DICIONÁRIO LOCAL PARA ESTA RODADA
            # Isso impede que dados de uma rodada estraguem a outra
            dados_desta_rodada = {}

            if self.PrimeiraEntrada:
                entradaA = entrada(int(self.EntradaDeMateriais.get()), "", "ProcessoPadrão", grafo)
                self.listaDeSaidas = entradaA.processaEmUnicoLote()
                self.lstTuplesaidasContadas = Saida.ContarTipoDeSaida(self.listaDeSaidas)
                
                if entradaA.celulaAtual == "":
                    self.ProximaSaida = self.start
                elif entradaA.celulaAtual != self.end:
                    for i, celula in enumerate(self.CaminhoDoPiPeLine):
                        if entradaA.celulaAtual == celula[0]:
                            self.ProximaSaida = celula[1]
                self.qtdNovaEntrada = 0
                for tuple in self.lstTuplesaidasContadas:
                    if str(tuple[0]) == Saida.PecaAcabada.name:
                        self.qtdNovaEntrada = int(tuple[1])
                        break
                
                # Salvamos no dicionário local desta rodada
                dados_desta_rodada["listaDeSaidas"] = self.listaDeSaidas
                dados_desta_rodada["lstTuplesaidasContadas"] = self.lstTuplesaidasContadas
                dados_desta_rodada["ProximaCelulaAtual"] = self.ProximaSaida
                dados_desta_rodada["ProximaQtdEntradaMaterial"] = self.qtdNovaEntrada
                
                # Atualiza a referência global para o próximo 'else' usar
                self.dictParaProximaEntrada = deepcopy(dados_desta_rodada)
                
                # Guarda o histórico perfeitamente isolado
                self.dicionarioProcessamento[f"{self.intCelulasProcessadas}"] = dados_desta_rodada
                
            else:
                # 1. BUSCA O VALOR CORRETO DA ANTERIOR:
                # A entrada de B DEVE SER a quantidade de peças boas (PecaAcabada) que saíram de A
                AnteriorQtdEntradaMaterial = int(self.dictParaProximaEntrada["ProximaQtdEntradaMaterial"])

                entradaB = entrada(AnteriorQtdEntradaMaterial,
                                   self.ProximaSaida,
                                   "ProcessoPadrão",
                                   grafo)
                self.listaDeSaidas = entradaB.processaEmUnicoLote()
                self.lstTuplesaidasContadas = Saida.ContarTipoDeSaida(self.listaDeSaidas)
                
                if entradaB.celulaAtual != self.end:
                    for i,celula in enumerate(self.CaminhoDoPiPeLine):
                        if entradaB.celulaAtual == celula[0]:
                            self.ProximaSaida = celula[1]
                
                # 2. PROCURA QUANTAS PEÇAS BOAS A CÉLULA ATUAL GEROU PARA A PRÓXIMA:
                # Zeramos a variável para não acumular lixo ou referências antigas da memória
                self.qtdNovaEntrada = 0
                for tuple in self.lstTuplesaidasContadas:
                    # Garantimos que acessamos o nome [0] e a quantidade [1] explicitamente
                    if str(tuple[0]) == Saida.PecaAcabada.name:
                        self.qtdNovaEntrada = int(tuple[1])
                        break
                    
                # 3. SALVA NO SEU DICIONÁRIO DE HISTÓRICO:
                self.dictParaProximaEntrada["listaDeSaidas"] = self.listaDeSaidas
                self.dictParaProximaEntrada["lstTuplesaidasContadas"] = self.lstTuplesaidasContadas
                self.dictParaProximaEntrada["ProximaCelulaAtual"] = self.ProximaSaida
                self.dictParaProximaEntrada["ProximaQtdEntradaMaterial"] = self.qtdNovaEntrada
                self.dictParaProximaEntrada["AnteriorQtdEntradaMaterial"] = AnteriorQtdEntradaMaterial
                
                # O SEGREDO DO ISOLAMENTO: Usamos o copy() aqui para congelar o estado atual do dicionário
                self.dicionarioProcessamento[f"{self.intCelulasProcessadas}"] = self.dictParaProximaEntrada.copy()

        else:
            self.lblMensagem["text"] = "Insira um numero maior que zero"  # Corrigido erro de sintaxe aqui (Text -> "text")
            self.lblMensagem.pack(side=LEFT)

    # Monta os componentes dos processamento da entrada
    def DesenharSaidasDoProcesso(self,listaDeSaidas,lstTuplesaidasContadas):
        from PIL import ImageFile
        from PIL import Image
        from PIL import Image, ImageTk

        self.PrimeiroContainer = Frame(self.ConteudoJanela,padx="25")
        self.PrimeiroContainer.pack(side=LEFT)

        self.frame_matriz = Frame(self.PrimeiroContainer, bg="lightgray",padx="25",)
        self.frame_matriz.pack(fill="both") 
        
        #Se é o primeiro endereço do pipeline busca da tela a informações
        #as outras vezes busca do processo
        if self.PrimeiraEntrada:
            Label(self.PrimeiroContainer, text=f"Celula Processada:{self.start}", padx=0, pady=0).pack(side="top",anchor="center")
            Label(self.PrimeiroContainer, text=f"Entrada processadas: {self.EntradaDeMateriais.get()}",font=self.fontePadraoMaior
                  ).pack()
        else:
           Label(self.PrimeiroContainer, text=f"Celula Processada: {self.dictParaProximaEntrada["ProximaCelulaAtual"]}", padx=0, pady=0).pack(side="top",anchor="center")
           Label(self.PrimeiroContainer, text=f"Entrada processadas: {self.dictParaProximaEntrada["AnteriorQtdEntradaMaterial"]}",font=self.fontePadraoMaior
                  ).pack()

        self.SegundoContainer = Frame(self.PrimeiroContainer)
        self.SegundoContainer["pady"] = 10
        self.SegundoContainer.pack(side="top", fill="x")
        
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

        #Contagem na tela da representação dos itens processados(A grid com as imagens)
        for tuple in lstTuplesaidasContadas:
            if tuple[0] == Saida.PecaAcabada.name and tuple[1] > 0:
                Label(self.SegundoContainer, image=verde, bd=0, padx=0, pady=0).pack(side="left",anchor=S)
                Label(self.SegundoContainer, text=" = " + str(tuple[1]), font=self.fontePadrao).pack(side="left",anchor=S)
            if tuple[0] == Saida.PontasDeEstoque.name and tuple[1] > 0:
                Label(self.SegundoContainer, image=amarelo, bd=0, padx=0, pady=0).pack(side="left",anchor=S)
                Label(self.SegundoContainer, text=" = " +str(tuple[1]), font=self.fontePadrao).pack(side="left",anchor=S)                
            if tuple[0] == Saida.Reciclagem.name and tuple[1] > 0:
                Label(self.SegundoContainer, image=vermelho, bd=0, padx=0, pady=0).pack(side="left",anchor=S)
                Label(self.SegundoContainer, text=" = " + str(tuple[1]), font=self.fontePadrao).pack(side="left",anchor=S)
        
        nomeEquipe = "Equipe X"
        integrantesCelula = {"Operadores": ["A", "B", "C"], "Máquinas": ["M1", "M2"]}
        texto_equipe = f"Equipe {nomeEquipe} \n Integrantes: {', '.join(integrantesCelula['Operadores'])}\n maquinas: {', '.join(integrantesCelula['Máquinas'])}"

        lbl_equipe = Label(self.PrimeiroContainer, text=texto_equipe, font=self.fontePadrao, justify="left", anchor="n")
        lbl_equipe.pack()

        # Adicione isso na última linha da função:
        self.ConteudoJanela.update_idletasks()
        self.CanvasJanela1.configure(scrollregion=self.CanvasJanela1.bbox("all"))
        if self.end == self.dictParaProximaEntrada["ProximaCelulaAtual"] or self.end == self.start:
            return True 
        else: return FALSE
    #Posto de Triagem / Inspeção Final - log juntando todas as peças que não viram nova entrada
    def DesenharFimDoProcessamento(self):
        self.PrimeiroContainer = Frame(self.ConteudoJanela, padx="25")
        self.PrimeiroContainer.pack(side=LEFT)

        self.frame_matriz = Frame(self.PrimeiroContainer, bg="lightgray", padx="25")
        self.frame_matriz.pack(fill="both") 
        Label(self.PrimeiroContainer, text="Posto de Triagem / Inspeção Final:", padx=0, pady=0).pack(anchor="w")
        
        lstSaidasProcessadas = []
        
        # 1. Descobrimos qual é a última chave numérica que foi de fato populada no histórico
        chaves_ordenadas = sorted(self.dicionarioProcessamento.keys(), key=int)
        ultima_chave_processada = int(chaves_ordenadas[-1]) if chaves_ordenadas else -1
        
        # Iteramos pelas chaves gravadas
        for chave_str in chaves_ordenadas:
            intProcessados = int(chave_str)
            objDicionario = self.dicionarioProcessamento[chave_str]
            
            # Identifica o nome da célula no histórico
            nome_celula = self.start if intProcessados == 0 else objDicionario.get("ProximaCelulaAtual", "Desconhecida")
            
            for tupleSaidaContada in objDicionario["lstTuplesaidasContadas"]:
                nome_saida = str(tupleSaidaContada[0])
                quantidade = int(tupleSaidaContada[1])
                
                # Filtro de Segurança: Ignora itens zerados ou tipo Default
                if quantidade <= 0 or nome_saida == Saida.Default.name:
                    continue
                
                # REGRA MATEMÁTICA PARA FECHAR COM O INPUT:
                # Se for a ÚLTIMA célula que o pipeline conseguiu rodar até agora, 
                # nós mostramos TUDO dela (inclusive as Peças Acabadas que pararam nela).
                if intProcessados == ultima_chave_processada:
                    lstSaidasProcessadas.append((nome_celula, nome_saida, quantidade))
                else:
                    # Se for uma célula anterior do histórico, as peças acabadas já mudaram 
                    # de célula. Então guardamos APENAS os descartes para não duplicar a soma.
                    if nome_saida != Saida.PecaAcabada.name:
                        lstSaidasProcessadas.append((nome_celula, nome_saida, quantidade))

        # Desenha as linhas no painel da direita
        for item in lstSaidasProcessadas:
            celula, saida, qtd = item
            Label(
                self.PrimeiroContainer, 
                text=f"Celula de Processamento: {celula} Saida: {saida} Qtd : {qtd}", 
                padx=0, pady=0, 
                font=self.fontePadrao
            ).pack(anchor="w")
        if hasattr(self, "canvas"):
            self.CanvasJanela1.configure(scrollregion=self.CanvasJanela1.bbox("all"))
            

            #self.dictParaProximaEntrada["listaDeSaidas"] = self.listaDeSaidas
            #self.dictParaProximaEntrada["lstTuplesaidasContadas"] = self.lstTuplesaidasContadas
            #self.dictParaProximaEntrada["ProximaCelulaAtual"] = self.ProximaSaida
            #self.dictParaProximaEntrada["ProximaQtdEntradaMaterial"] = self.qtdNovaEntrada
            #self.dictParaProximaEntrada["AnteriorQtdEntradaMaterial"] = AnteriorQtdEntradaMaterial
    
