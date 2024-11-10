import threading
import random 
import time
import sys

pontos_redistribuicao = 0
veiculos = 0
encomendas = 0
espacos_de_carga = 0 #por veiculo

if len(sys.argv) != 5:
    print("Usage: python Untitled-1.py <S> <C> <P> <A>")
    exit()

S = int(sys.argv[1])
C = int(sys.argv[2])
P = int(sys.argv[3])
A = int(sys.argv[4])

pontos_redistribuicao = S
veiculos = C
encomendas = P
espacos_de_carga = A

if encomendas <= espacos_de_carga or encomendas <= veiculos or espacos_de_carga <= veiculos:
    print("Encomendas insuficientes para distribuir")
    exit()