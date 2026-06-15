from dataclasses import dataclass, field
from clsPipeline import celula

@dataclass
class Grafo:
    # O dict agora mapeia o nome do vértice para a classe de propriedades
    grafo: dict[any] = field(default_factory=dict)
    def __init__(self):
        self.grafo = {} # Seu dicionário interno

    # Adicione este método mágico para permitir o uso de colchetes []
    def __getitem__(self, chave):
        return self.grafo.get(chave, None)
    def adicionar_vertice(self, vertice:str):
        if len(self.grafo) == 0:
            self.grafo["START"] = vertice
        if vertice not in self.grafo:
            self.grafo[vertice] = {"celula":celula(vertice,None,None,{},50,(60,60),False, True if self.grafo["START"] == vertice else False ),"vizinhos": [],"Saida":[]}

    def adicionar_aresta(self, v1:str, v2:str):
        self.adicionar_vertice(v1)
        self.adicionar_vertice(v2)
        if v2 not in self.grafo[v1]["vizinhos"]:
            self.grafo[v1]["Saida"].append(v1+"->"+v2)
            #self.grafo[v1]["celula"].append(celula.vizinhos(v2))
            self.grafo[v1]["vizinhos"].append(v2)
        if v1 not in self.grafo[v2]["vizinhos"]:
            self.grafo[v2]["vizinhos"].append(v1)
            #self.grafo[v2]["celula"].append(celula.vizinhos(v1))
            self.grafo[v2]["vizinhos"].append(v1)