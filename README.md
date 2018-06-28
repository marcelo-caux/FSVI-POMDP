# FSVI-POMDP
Código do algoritmo FSVI para navegação em POMDP

Este código implementa uma tela simples destinada a apresentar uma grid representando um espaço de crença de um POMDP (Partially 
Observable Markov Decision Process) que tem sua navegação resolvida usando um algoritmo chamado Foward Search Value Iteraction
descrito no artigo Forward Search Value Iteration For POMDPs, Department of Computer Science, Ben-Gurion University, Beer-Sheva, Israel
Este algorítmo propõe usar o MDP adjacente ao POMDP para definir a política ótima a cada espaço de crença do POMDP

Os scripts AIMA_MDP.py e utils.py foram obtidos aqui no Github e são parte do acervo de código livre oferecidos pelo livro
Artificial Inteligence - A modern Approach, Stuart Russel and Peter Norvig, Pearson e pode ser encontrado em
https://github.com/aimacode

Foi criado usando a versão 3.6 do Python e não roda em versões inferiores a 3
Todos os parâmetros de configuração da grid, MDP e POMDP estão no script GRID.py, linhas 12 a 27, são eles:

# 1-dimensoes da grid [colunas,linhas] (x,y)
# 2-terminasl, são os pontos de saída do mdp (tem que ser iguais as recompensas) [(x,y),(x,y)]
# 3-recompenas, dicionário no formato [(x,y):Recompensa,(x,y):recompensa)], todos os (x,y) estão em terminals
# 4-Muros ou obstáculos, dicionário no formato [(x,y):None,(x,y):None)]
# 5-Probilidade de b0=s0, ou seja de o agente do POMDP estar na mesma posição do MDP
# 6-b0 >> Ponto de partida do POMDP, qualquer coordenada dentro do grid
# define o ponto de partida do POMDP
b0=(3,1)
# define as dimensoes do grid
dims=[16,16]
#define as coordenadas dos terminais e pontos de recompensa << evita errar a configuração...
t1=(0,15)
t2=(2,2)
#define os muros/obstáculos (l,c):None
ListMuros={(5,15):None,(0,14):None,(3,14):None,(2,14):None,(4,13):None,(5,13):None,(6,13):None,(6,15):None,(1,14):None}
esta é a configuração que está disponível aqui no Github, podendo ser ajustada a gosto

Sugiro baixar o código e rodar usando o Pycharm que facilita muito a execução e debug do código para avaliação de variáveis
