"""
Procedimento para rodar o POMDP
Parametros:
Tamanho da Grid=[X,Y] >> grid X x Y de estados
Terminals é um array de dois estados =>> [(x,y), (x,y)]
recompensa é um dicionário com quantas recompensas quizer=>>{(x,y):V,(x,y):V}
obstaculos é um dicionário com quantos obstaculos quizer=>>{(x,y):None,(x,y):None}
barreitas é um dicionário com quantas barreiras quizer=>>{(x,y):V,(x,y):V}
probPOMDP é o valor da certeza de estar em um espaço no POMDP, 1-probPOMDP é a
probabilidade de estar em um espaço adjacente, 0<probPOMDP<=1
b0=início da obeservação, ponto de partida de onde se deseja chegar a recompensa
"""

#import numpy as np
import AIMA_MDP
import utils
import random

class POMDP:
    def __init__(self, dims, terminals, recompensa, obstaculos, probPOMPD,b0):

        if not (0<probPOMPD<1):
            raise ValueError("A probabilidade de estar em um espaço no POMDP deve ser um valor 0< p <1")
        if not isinstance(recompensa,dict):
            raise ValueError("recompensa deve ser criado na forma {(x,y):V,(x,y):V}, onde x=coluna, y=linha e V=número")

        self.dims=dims
        self.terminals=terminals
        self.recompensa=recompensa
        self.obstaculos=obstaculos
        self.probPOMPD=probPOMPD

        mgrid=[]
        pgrid=[]
        # bstates é a grid de estados do POMDP, incializada em criaGrids
        self.bstates = set()
        # b é o vetor de possíveis estados de b0
        self.b={}
        # path é o vetor que vai de um estado até a recompensa positiva
        self.path={}


        self.criaGrids(dims,recompensa,obstaculos,probPOMPD,mgrid,pgrid,self.bstates)
        self.montavetor_b(self.b,self.bstates)

#----- Cria o MDP para a grid escolhida com as características desejadas
        self.mdp = AIMA_MDP.GridMDP(mgrid, terminals)
        #a criação do mdp faz uma inversão da grid, assim é necessário mudar recompensa
        self.recompensa=self.recompensa_reverse()
        #mesmo ajuste feito para os obstáculos, só que direto no mdp
        self.obstaculos=self.mdp.murorev
        self.U = AIMA_MDP.value_iteration(self.mdp)
        self.pi = AIMA_MDP.best_policy(self.mdp, self.U)

#----- Incia o processamento do POMDP baseado no grid pgrid
        self.FSVI(b0)

#---------  funcoes do programa  -----------------------------------------

    #função de inicialização de elementos
    def criaGrids(self, dims, recompensa, obstaculos, probPOMDP,mgrid,pgrid,bstates):
        #monta a grid basica no mdp = mgrid e do pomdp = pgrid
        pelement={"me":probPOMDP,"ad":round(1-probPOMDP,4)}
        for l in range(dims[0]):
            mcols =[]
            pcols =[]
            for c in range(dims[1]):
                mcols.append(0.01)
                pcols.append(pelement)
                bstates.add((l,c))
            mgrid.append(mcols)
            pgrid.append(pcols)
        #coloca as recompensas na grid mgrid do mdp
        for key in recompensa.keys():
            y=int(key[0])
            x=int(key[1])
            mgrid[x][y]=float(recompensa[key])
        #coloca os obstaculos na grid mgrid do mdp
        for key in obstaculos.keys():
            y=int(key[0])
            x=int(key[1])
            mgrid[x][y]=obstaculos[key]
        return [None]

    #monta o vetor b de estados de crença do agente
    def montavetor_b(self,b,bstares):
        for s in bstares:
            nearstates = []
            nearstates.append({s: .85})
            for act in utils.orientations:
                near=utils.vector_add(s,act)
                #só adiciona estados adjacentes limitados pela grid
                if (near[0]>=0 and near[1]>=0) and (near[0]<self.dims[0] and near[1]<self.dims[1]):
                    nearstates.append({near:.15})
            b[s]=nearstates
        return [None]

#---- Implementa o algorítimo FSVI
    def FSVI(self,b0):
        self.path={}
        self.V={}
        fim=False
        while not fim:
            s0=self.Sample_s0_b0(b0)
            fim=self.MDPExplore(b0,s0)
       # print("Utility: ",self.V)
       # print("Path:",self.path)

    def MDPExplore(self,b0,s0):
        # testa se existe valor de utilidade para s0, caso negativo ele é uma parede
        # retorna false e FSVI gera um novo sample de b0
        if s0 not in self.U:
            return False
        else:
        # salva/incrementa o caminho definido pela politica para b0
            if b0 in self.path:
                self.path[b0].append(s0)
            else:
                self.path[b0] = [s0]
            # Salva/incrementa valor de Utilidade V[b0]
            if b0 in self.V:
                self.V[b0] += self.U[s0]
            else:
                self.V[b0] = self.U[s0]
            if not (s0 in self.recompensa):
                #busca a politica ótima do MDP para s0)
                a=self.pi[s0]
                #identifica o proximo estado s1 aplicando a politica a s0
                s1=utils.vector_add(s0,a)
                self.MDPExplore(b0,s1)
            return True



    def Sample_s0_b0(self,b0):
        nearstates=self.b[b0]
        qtKeys=len(nearstates)
        i=0
        rd=random.randrange(1, qtKeys+1, 1)
        for state in nearstates:
            i += 1
            for k in state.keys():
                rstate=k
            if i==rd:
                break
        return rstate

    def recompensa_reverse(self):
        valores=[]
        recomprev={}
        for key in self.recompensa:
            valores.append(self.recompensa[key])
        for l in range(self.dims[0]):
            for c in range(self.dims[1]):
                if self.mdp.grid[l][c] in valores:
                    recomprev[(c,l)]=self.mdp.grid[l][c]
        return recomprev


class InitPOMDP(POMDP):
    def __init__(self, dims, terminals, recompensa, obstaculos, probPOMPD,b0):
        POMDP.__init__(self, dims, terminals, recompensa, obstaculos, probPOMPD,b0)
