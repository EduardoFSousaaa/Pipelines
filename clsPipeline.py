import enum
from tkinter import *
from dataclasses import dataclass
from array import array
from typing import List
from grafo import *
from datetime import datetime
import random

@dataclass
class celula:
    nome: str = ""
    entrada: entrada = None
    integrantes: integrantesCelula = None
    vizinhos: List[Grafo]= field(default_factory=list)
    capacidadeDeProducao: int = 50
    tempoDeProducao: tempoDeProducao = field(default_factory= lambda:tempoDeProducao(60,60))
    Ocupada: bool = False
    start: bool = False
    
    def __getitem__(self, chave):
        return self.celula.get(chave, None)
    
    def ObterListaDeSaidas(self, grafo: Grafo):
        if self.nome in grafo.grafo:
            return grafo[self.nome].vizinhos
        return []
    
@dataclass()
class integrantesCelula:
    nomeEquipe: str = ""
    operadores: list = field(default_factory=list[str])
    maquinas:  list = field(default_factory=list[str])

@dataclass
class PropriedadesVertice:
    # Inicializa uma lista vazia para cada novo vértice criado
    vizinhos: list[any] = field(default_factory=list)

@dataclass
class entrada:        
    qtdmateriaPrima: int = 0
    celulasPossiveis:  list[celula] = field(default_factory=list)
    ProcessoDeProducao: str = "Processo Padrão"
    grafo: dict[any, PropriedadesVertice] = field(default_factory=dict)
    def SortearQualidadeDaPeca(self):
        numSorteado = random.randint(0, 100) * 1.5
        if numSorteado >= 25:
            return Saida.PecaAcabada
        if numSorteado <= 24 and numSorteado > 5:
            return Saida.PontasDeEstoque
        if numSorteado <= 5:
            return Saida.Reciclagem
        else:
            return Saida.Default
    def ProcessarEntrada(self):
        if self.qtdmateriaPrima >= 0:   
            for celula in self.celulasPossiveis:
                if not celula.ocupada:
                    if celula.capacidadeDeProducao >= self.qtdmateriaPrima:
                        celula.ocupada = True 
                        lstSaidas = self.processaEmUnicoLote(self,celula)
                        self.qtdmateriaPrima = 0
                        return lstSaidas
                    else:
                        if len(self.celulasPossiveis)>=2:
                            if celula.capacidadeDeProducao >= self.qtdmateriaPrima/2:
                                print(f"Processando {self.qtdmateriaPrima/2} unidades de matéria-prima usando o {self.ProcessoDeProducao} na célula {celula.nome}")
                                celula.ocupada = True
                                self.qtdmateriaPrima = self.qtdmateriaPrima/2
                        else:
                            print(f"A célula {celula.nome} não tem capacidade suficiente para processar a matéria-prima. Por favor, aguarde ou tente outra célula.")
                            continue
            return "Todas as células estão ocupadas no momento. Por favor, aguarde."
        else:  
            return "Sem materia-prima disponível."
    def processaEmUnicoLote(entrada: entrada, celula: celula):
        print(f"Processando {entrada.qtdmateriaPrima} unidades de matéria-prima usando o {entrada.ProcessoDeProducao} em um único lote")
        ListaDeSaidas = []
        for i in range(entrada.qtdmateriaPrima):
            if i % 10 == 0:
                print(f"Hora Final para o número: {i}/{entrada.qtdmateriaPrima} unidades processadas: {str(datetime.now())}")
            saida = entrada.SortearQualidadeDaPeca()
            ListaDeSaidas.append(saida)
            print(f"Peça {i+1}: {saida.name}")
        return ListaDeSaidas
        #ListaSaidas = Saida.ContarTipoDeSaida(ListaDeSaidas)
        #for saida in lstSaidasContadas:
            
        #dataSaidaLote = datetime.datetime.now()
        #return [Contagem, dataSaidaLote]
        #NovaSaida = SaidaDaCelula()
        #lstSaidas = []
        #lstSaidas = ListaDeSaidas
        #for saida in Contagem:
        #    saidaDaCelula = SaidaDaCelula(tipoDeSaida=saida,
        #                                   qtd=Contagem[saida], 
        #                                   destinosPossiveis=[celula.ObterListaDeSaidas(entrada.grafo)],
        #                                   dataSaida=str(datetime.datetime.now()))
        #    lstSaidas.append(saidaDaCelula)
        #return ListaSaidas
@dataclass
class tempoDeProducao:        
    horahomem: int = 60
    horaMaquina: int = 60
@dataclass
class Pipeline:
    id:int
    Titulo:str
    tamanho:int = 0
    grafo: Grafo = field(default_factory = dict())

class Saida(enum.Enum):
    PecaAcabada = 1
    PontasDeEstoque = 2
    Reciclagem = 3
    Default = 0
    
    @staticmethod
    def ContarTipoDeSaida(listaDeSaidas: List):
        contagem = {
            Saida.PecaAcabada: 0,
            Saida.PontasDeEstoque: 0,
            Saida.Reciclagem: 0,
            Saida.Default: 0
        }
        for saida in listaDeSaidas:
            if saida in contagem:
                contagem[saida] += 1
        # Retorna a lista de tuplas (nome, quantidade) dinamicamente
        return [(saida.name, qtd) for saida, qtd in contagem.items()]

@dataclass
class SaidaDaCelula():
    tipoDeSaida: Saida = Saida.Default
    qtd: int = 0
    destinosPossiveis:  list = field(default_factory=list[celula])
    dataSaida: str = ""

    def __init__(self, tipoDeSaida: Saida, qtd: int, destinosPossiveis: list[celula], dataSaida: str):
        self.tipoDeSaida = tipoDeSaida
        self.qtd = qtd
        self.destinosPossiveis = destinosPossiveis
        self.dataSaida = dataSaida