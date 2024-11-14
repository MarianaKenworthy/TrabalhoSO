import threading
import random 
import time
import sys

pontos_redistribuicao = 0
veiculos = 0
encomendas = 0
espacos_de_carga = 0 #por veiculo

semafore = threading.Semaphore(1)

if len(sys.argv) != 5:
    print("Usage: python Untitled-1.py <S> <C> <P> <A>")
    exit()

S = int(sys.argv[1])
C = int(sys.argv[2])
P = int(sys.argv[3])
A = int(sys.argv[4])



if P <= A or P <= C or A <= C:
    print("Encomendas insuficientes para distribuir")
    exit()


def criar_threads(P, C, S, A):
     pontos_redistribuicao = []
    veiculos = []
    encomendas = []
    espacos_de_carga = A

    # Criar threads para cada encomenda.
    for i in range(P):
        encomendas = threading.Thread(target=, args=(i,))
        threads.append(encomendas)
        thread.start()

    # Criar threads para cada veículo.
    for i in range(C):
        ponto_partida = random.choice(pontos_redistribuicao)
        veiculos = threading.Thread(target= processamento_veiculos, args=(i, ponto_partida))
        threads.append(veiculos)
        thread.start()

    # Criar threads para cada ponto de redistribuição.
    for i in range(S):
        pontos_redistribuicao = threading.Thread(target= , args=(i, espacos_de_carga))
        threads.append(pontos_redistribuicao)
        thread.start()

    # Esperar todas as threads terminarem.
    for thread in threads:
        thread.join()


def processamento_veiculos(i, ponto_partida):
    print(f"Veículo {i} partindo do ponto de redistribuição {ponto_partida}.")

    # Simular tempo de viagem.
    


# Exemplo de uso:
criar_threads(P=5, C=3, S=2)