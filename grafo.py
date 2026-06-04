from dataclasses import dataclass, field

@dataclass
class PropriedadesVertice:
    # Define exatamente o que o vértice vai conter
    vizinhos: list[any] = field(default_factory=list)
    #peso: int = 0
    #cor: str = "branco"  # Útil para algoritmos como BFS/DFS

@dataclass
class Grafo:
    # O dict agora mapeia o nome do vértice para a classe de propriedades
    grafo: dict[any, PropriedadesVertice] = field(default_factory=dict)

    def adicionar_vertice(self, vertice):
        if vertice not in self.grafo:
            self.grafo[vertice] = PropriedadesVertice()

    def adicionar_aresta(self, v1, v2):
        self.adicionar_vertice(v1)
        self.adicionar_vertice(v2)
        
        if v2 not in self.grafo[v1].vizinhos:
            self.grafo[v1].vizinhos.append(v2)
        if v1 not in self.grafo[v2].vizinhos:
            self.grafo[v2].vizinhos.append(v1)
