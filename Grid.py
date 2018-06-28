# importa modulo
from tkinter import *
import MDC_POMDP
import datetime

ini=datetime.datetime.now()
# Cria formulario
formulario = Tk()
formulario.geometry('500x400')

#executa o POMPD" ---------------------------------
# Parametros
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
#define os terminais e pontos de recompensa
t1=(0,15)
t2=(2,2)
#define os muros/obstáculos (l,c):None
ListMuros={(5,15):None,(0,14):None,(3,14):None,(2,14):None,(4,13):None,(5,13):None,(6,13):None,(6,15):None,(1,14):None}

# processa o POMDP ---------------------------------

pomdp=MDC_POMDP.POMDP(dims,[t1, t2],{t1:10,t2:-1},ListMuros,0.85,b0)

#---------------------------------------------------

Path=pomdp.path
muros=pomdp.obstaculos
vmax=0
vmin=0
for k in pomdp.recompensa.keys():
    v=pomdp.recompensa[k]
    if v>vmax:
        kmax=k
        vmax=v
    if v<vmin:
        kmin=k
        vmin=v

xymax="("+str(kmax[1])+","+str(kmax[0])+")"
#formulario.title("POMDP(x,y), bo="+str(b0)+" recompensa"+xymax+ "="+str(vmax)+ "/morte="+str(kmin))
#formulario.title("POMDP(l,c), bo="+str(b0)+" recompensa"+str(kmax)+ "="+str(vmax)+ "/morte="+str(kmin))
#muros=[(1,2)]
elementos=[]
li=5
for k in Path.keys():
    elementos=Path[k]

rot=[]
for l in range(dims[1]): # vai de 0 a 3
    for c in range(dims[0]):
        tx="("+str(l)+","+str(c)+")"
        txx=[]
        txx.append((l,c))
        if txx[0] in elementos:
            if txx[0]==kmax:
                rotp = Button(formulario, text=str(vmax), padx=6, pady=5, relief=RAISED, fg="blue")
                rotp.grid(row=l + li, column=c)
            else:
                if txx[0] == kmin: #só morro quando a escolho b0 adjacente a recompensa menor e o sampling de s0 cai lá.
                    rotx = Button(formulario, text="MORRI", padx=0, pady=5, relief=RAISED, fg="red")
                    rotx.grid(row=l + li, column=c)
                else:
                    rotp=Button(formulario, text=tx, padx=5, pady=5, relief=RAISED, fg="blue")
                    rotp.grid(row=l + li, column=c)
        else:
            if txx[0] in muros:
                rotm = Button(formulario, text="MURO", padx=1, pady=5, fg="green")
                rotm.grid(row=l + li, column=c)
            else:
                if txx[0] == kmin:
                    rotx = Button(formulario, text=str(vmin), padx=7, pady=5, relief=RAISED, fg="red")
                    rotx.grid(row=l + li, column=c)
                else:
                    rot = Button(formulario, text=tx, padx=5, pady=5, relief=SUNKEN)
                    rot.grid(row=l+li, column=c)

# calcula tempo processamento
fim=datetime.datetime.now()
dif=fim-ini
#r = StringVar()
r= " Tempo: " + str(dif.total_seconds())+ " seg"
formulario.title("POMDP(l,c), bo="+str(b0)+" recompensa"+str(kmax)+ "="+str(vmax)+ r)
if dims[0]<9:
    formulario.geometry('500x400')
else:
    formulario.geometry('1000x500')

#resultado = Button(formulario, text=r, padx=7, pady=5, relief=RAISED, fg="red")
#resultado.grid(row=35, column=0)
#resultado.insert(0,r)
#texto1 = Entry(formulario)
#rx=4+int(dims[1])

# Roda o loop principal do tcl
mainloop()
