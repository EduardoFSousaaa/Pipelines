from dataclasses import dataclass, field
from clsPipeline import celula

@dataclass()
class Grafo:
    # O dict agora mapeia o nome do vértice para a classe de propriedades
    grafo: dict[any] = field(default_factory=dict)

    def __init__(self):
        self.grafo = {"lst_celulas":[],"START":"","END":""} # Seu dicionário interno

    # Adicione este método mágico para permitir o uso de colchetes []
    def __getitem__(self, chave):
        return self.grafo.get(chave, None)
    def adicionar_vertice(self, vertice:str):
        vertice = vertice.upper()
        if self.grafo["START"] == "":
            self.grafo["START"] = vertice
            self.grafo["END"] = vertice
        if vertice not in self.grafo:
            self.grafo[vertice] = {"celula:":celula(vertice,None,None,{},50,(60,60),False),"vizinhos" : [],"saida":[]}
            self.grafo["lst_celulas"].append(vertice)
    def adicionar_aresta(self, v1:str, v2:str):
        v1 = v1.upper()
        v2 = v2.upper()
        self.adicionar_vertice(v1)
        self.adicionar_vertice(v2)
        if v2 not in self.grafo[v1]["vizinhos"]:
            self.grafo[v1]["saida"].append((v1,v2))
            #self.grafo[v1]["celula"].append(celula.vizinhos(v2))
            self.grafo[v1]["vizinhos"].append(v2)
        if v1 not in self.grafo[v2]["vizinhos"]:
            self.grafo[v2]["vizinhos"].append(v1)
            #self.grafo[v2]["celula"].append(celula.vizinhos(v1))
    def adicionar_verticeStart(self,vStart:str):
        vStart = vStart.upper()
        self.grafo["START"] = vStart
    def adicionar_verticeEnd(self,vEnd:str):
        vEnd = vEnd.upper()
        self.grafo["END"] = vEnd.upper()

    def caminhosDoPipeline(self):
        celulaSTART = self.grafo["START"]
        celulaEND = self.grafo["END"]
        intCaminho = 0
        self.caminhosEnd = []
        caminhoRamos = []
        caminhoPercorrido = []
        #Se o celula Inicial  for a mesma que a final
        if celulaSTART !="" and celulaEND != "" and celulaSTART == celulaEND:
            self.caminhosEnd.append((celulaSTART,celulaEND))
            return 
        
        ##A logica de entradas anteriores: pode usar esse bloco alterando a saida[1] que o destino para procura a origem saida[0] que vai da na celula
        #Caminhos ramos que saem do inicio e vao para o proximo ponto
        for celula in self.grafo["lst_celulas"]:
            for saida in self.grafo[celulaSTART]["saida"]:
                if saida[1] == celula:
                    caminhoRamos.append(celula)
        caminhoPercorrido.append(celulaSTART)

        #Se a celula do fim estiver no caminho sabe-se que o inicio tem caminho direto para o fim do pipeline
        if celulaEND in caminhoRamos:
            caminhoPercorrido.append(celulaEND)
            self.montarCaminhoPercorrido(caminhoPercorrido)
            return
        RamosVisistados = []
        NovosCaminhos = {}
        for Ramos in caminhoRamos:
            if Ramos not in RamosVisistados:
                if Ramos == celulaEND:
                    caminhoPercorrido.append(Ramos)
                    self.montarCaminhoPercorrido(caminhoPercorrido)
                    break
                else: 
                    #Dicionario dos novos caminhos origem ramos e value saidas
                    NovosCaminhos[Ramos] = self.verificaSaidas(Ramos)
                    
                    #Se celula final esta nos proximos caminhos tem acesso direto Ramos para celua end
                    if celulaEND in NovosCaminhos:
                        #se a celula Final esta no ramo Coloca o ramo no Caminho percorrido
                        # apos A celula final inseri no caminho percorrido que tem acesso apartir do ramos.
                        caminhoPercorrido.append(Ramos)
                        caminhoPercorrido.append(celulaEND)
                        self.montarCaminhoPercorrido(caminhoPercorrido)
                        break
                    RamosVisistados.append(Ramos)
        
        for CaminhosOrigem in NovosCaminhos:
            CaminhoPEnd = self.verificaSaidasSevaiEND(CaminhosOrigem)
            if CaminhoPEnd != []:
                caminhoPercorrido.append(CaminhoPEnd[0])
                caminhoPercorrido.append(CaminhoPEnd[1])
                self.montarCaminhoPercorrido(caminhoPercorrido)              

    def montarCaminhoPercorrido(self,caminhoPercorrido:list):
        celulaEND = self.grafo["END"]
        for index,passos in enumerate(caminhoPercorrido):
            if  passos != celulaEND:
                #do passo que esta para o proximo da lista
                self.caminhosEnd.append((passos,caminhoPercorrido[index+1]))
                #Se é o passo final:
                # do ultimo passo Percorrido ao passo final que é o atual do caminho
            else: return
                #self.caminhosEnd.append((caminhoPercorrido[index-1],passos))
        
    def verificaSaidas(self,RamoDeVerificacao:str):
        caminhoRamos = []
        for celula in self.grafo["lst_celulas"]:
            for saida in self.grafo[RamoDeVerificacao]["saida"]:
                if saida[1] == celula:
                    caminhoRamos.append(celula)
        return caminhoRamos
    
    def verificaSaidasSevaiEND(self,RamoDeVerificacao:str):
        caminhoPercorrido = []
        for saida in self.grafo[RamoDeVerificacao]["saida"]:
            if saida[1] == self.grafo["END"]:
                caminhoPercorrido.append(RamoDeVerificacao)
                caminhoPercorrido.append(saida[1])
        return caminhoPercorrido
    
@dataclass
class Pipeline:
    id:int = 0
    Titulo:str = "Pipeline"
    tamanho:int = 0
    grafo: Grafo = field(default_factory = dict())
    start: celula = field(default_factory=dict())
    end: celula = field(default_factory=dict())