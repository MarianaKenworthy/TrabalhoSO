import threading
import time
import random
import sys

# S = nº de Stations
# C = nº de Carriers
# P = nº de Packages
# A = Carrier.capacity


# Exemplo de uso caso número de argumentos seja diferente do esperado
if len(sys.argv) != 5:
    print("Usage: python Untitled-1.py <S> <C> <P> <A>")
    exit()

# Atribuição dos argumentos a variáveis
S = int(sys.argv[1])
C = int(sys.argv[2])
P = int(sys.argv[3])
A = int(sys.argv[4])

# Verificação de valores inválidos
if P <= A or P <= C or A <= C:
    print("Insufficient packages to distribute")
    exit()


class Package(threading.Thread):
    def __init__(self, package_id, redist_stations):
        super().__init__()
        self.package_id = package_id
        self.redist_stations = redist_stations
        self.lock = threading.Semaphore(0)

        # Escolhe aleatoriamente duas estações para origem e destino, garantindo que não sejam iguais
        order = random.sample(redist_stations, 2)
        self.origin = order[0]
        self.origin.to_deliver_packages.append(self)
        self.destination = order[1]

    # Método para finalizar a entrega do pacote
    def end_delivery(self):
        # Abre o log do pacote
        filename = f"log_package{self.package_id}.txt"
        f = open(filename, "a")

        # Escreve no log o tempo de entrega
        f.write(f"Package {self.package_id} was delivered at time {round(time.time() - start_time, 4)}\n")
        f.close()

        # Destrava a thread e permite que ela finalize
        self.lock.release()

        print(f"Thread for package {self.package_id} ended at time {round(time.time() - start_time, 4)}")
    

    # Método para iniciar o log do pacote
    def begin_log(self):
        # Abre o arquivo de log
        filename = f"log_package{self.package_id}.txt"
        f = open(filename, "w")

        # Escreve no log o tempo de criação do pacote, a origem e o destino
        f.write(f"Package {self.package_id} was created at time {round(time.time() - start_time, 4)}\n\n")
        f.write(f"Package {self.package_id}  \n\tOrigin: {self.origin.station_id} \n\t Destination: {self.destination.station_id}\n")

        f.close()

    def run(self):

        self.begin_log()
        self.lock.acquire()


class Carrier(threading.Thread):
    def __init__(self, carrier_id, redist_stations, capacity):
        super().__init__()
        self.carrier_id = carrier_id
        self.redist_stations = redist_stations
        self.capacity = capacity
        self.carried_packages = []
        self.lock = threading.Semaphore(0)

        # Escolhe aleatoriamente uma estação para iniciar
        self.current_station = random.choice(redist_stations)

    # Método para carregar um pacote
    def load_package(self, package):
        # Verifica se a capacidade do carrier permite carregar o pacote
        if (self.capacity - len(self.carried_packages)) > 0:
            self.carried_packages.append(package)
            package.origin.to_deliver_packages.remove(package)

            # Faz a anotação no log do pacote
            filename = f"log_package{package.package_id}.txt"
            f = open(filename, "a")
            f.write(f"Package {package.package_id} was loaded by carrier {self.carrier_id} at time {round(time.time() - start_time, 4)}\n")
            print(f"Carrier {self.carrier_id} loaded package {package.package_id} from station {package.origin.station_id} at time {round(time.time() - start_time, 4)}")
            f.close()

    # Método para descarregar os pacotes
    def unload_packages(self):
        delivered_packages = []

        for i in range(len((self.carried_packages))):
            # Verifica se o pacote deve ser entregue na estação atual
            if self.carried_packages[i].destination.station_id == self.current_station.station_id:
                # Adiciona o pacote à lista de pacotes entregues
                delivered_packages.append(self.carried_packages[i])
                removed_package = self.carried_packages[i]
                #abre o log do pacote
                filename = f"log_package{removed_package.package_id}.txt"
                f = open(filename, "a") 

                # Simula o tempo de descarga do pacote
                time_unload = round(random.uniform(0.1, 0.5), 4)
                time.sleep(time_unload)
                # Escreve na tela e no log o tempo de descarga
                print(f"Carrier {self.carrier_id} unloaded package {self.carried_packages[i].package_id} on station {self.current_station.station_id} at time {round(time.time() - start_time, 4)}")
                f.write(f"Package {removed_package.package_id} was unloaded by carrier {self.carrier_id} on station {self.current_station.station_id} at time {round(time.time() - start_time, 4)}\n")
                f.close()
                # Finaliza a entrega do pacote e encerra sua thread
                removed_package.end_delivery()
                removed_package.join()
        # Remove os pacotes entregues da lista de pacotes carregados
        self.carried_packages = list(set(self.carried_packages) - set(delivered_packages))  

        return delivered_packages
        
    # Método para simular a viagem do carrier
    def travel(self):
        # Determina qual a próxima estação, respeitando uma lista circular
        next_station_index = (self.redist_stations.index(self.current_station) + 1) % len(self.redist_stations)

        # Determina o tempo de viagem
        travel_time = round(random.uniform(1, 4), 4)

        # Escreve na tela o tempo de viagem
        print(f"Carrier {self.carrier_id} traveling to station {self.current_station.station_id} for {travel_time} seconds")
        # Simula o tempo de viagem
        time.sleep(travel_time)
        # Atualiza a estação atual
        self.current_station = self.redist_stations[next_station_index]

    def run(self):
        # Imprime na tela a estação de origem do carrier
        print(f"carrier {self.carrier_id} running from station {self.current_station.station_id}")

        # Loop para processar os pacotes, enquanto houver pacotes a serem entregues ou pacotes carregados por essa carrier
        while (sum(station.get_to_deliver_packages_count() for station in self.redist_stations) > 0) or (len(self.carried_packages) > 0):
            # Se adiciona na estação
            self.current_station.add_carrier(self)

            # Destrava a estação permitindo o processamento dos pacotes da carrier
            self.current_station.lock.release()

            # Aguarda a estação liberar a carrier, ou seja, o fim do processamento dos pacotes
            self.lock.acquire()
            
            # Viaja para a próxima estação
            self.travel()

class Station(threading.Thread):
    def __init__(self, station_id):
        super().__init__()
        self.station_id = station_id
        self.to_deliver_packages = []
        self.received_packages = []
        self.carriers = []
        self.keep_running = True
        self.lock = threading.Semaphore(0)
        self.add_carrier_lock = threading.Semaphore(1)

    # Método para retornar a quantidade de pacotes a serem entregues
    def get_to_deliver_packages_count(self):
        return len(self.to_deliver_packages)

    # Método para adicionar um carrier à estação
    def add_carrier(self, carrier):
        # Garante que a operação de adição de carrier seja atômica
        self.add_carrier_lock.acquire()
        self.carriers.append(carrier)
        self.add_carrier_lock.release()

    # Método para iniciar o log da estação
    def begin_log(self):
        # Abre o arquivo de log de estação
        filename = f"log_station{self.station_id}.txt"
        f = open(filename, "w")

        # Escreve no log o tempo de criação da estação e os pacotes a serem entregues
        f.write(f"Station {self.station_id}  \n")
        for package in self.to_deliver_packages:
            f.write(f"Package {package.package_id} to be delivered\n")

        f.close()

    # Método para finalizar o log da estação
    def end_log(self):
        # Abre o arquivo de log da estação
        filename = f"log_station{self.station_id}.txt"
        f = open(filename, "a")

        # Escreve no log os pacotes recebidos
        f.write(f"\nStation {self.station_id}  \n")
        for package in self.received_packages:
            f.write(f"Package {package.package_id} received\n")
        f.close()

    # Método para processar os pacotes
    def process_packages(self, carrier):
        
        # Descarrega os pacotes em uma lista
        delivered_packages = carrier.unload_packages()

        # Adiciona os pacotes descarregados à lista de pacotes recebidos
        if len(delivered_packages) > 0:
            self.received_packages.extend(delivered_packages)

        # Carrega os pacotes a serem entregues em um carrier
        if len(carrier.carried_packages) < carrier.capacity:
            for package in self.to_deliver_packages[:]:
                carrier.load_package(package)
                time.sleep(0.5)

                
    def run(self): 
        
        # Trava a estação esperando a chegada de um carrier
        self.lock.acquire()

        # Loop para processar os pacotes enquanto a estação estiver ativa
        while self.keep_running:
            # Processa o primeiro carrier da fila
            carrier = self.carriers.pop(0)
            self.process_packages(carrier)

            # Destrava o carrier permitindo que siga para a próxima estação
            carrier.lock.release()

            # Trava a estação esperando a chegada de um carrier
            self.lock.acquire()

        self.end_log()


def main():

    # Inicialização das listas de estações, carriers e pacotes
    print(f"Running with {S} stations, {C} carriers, {P} packages and {A} carrier capacity")
    stations = []
    carriers = []
    packages = []

    # Tempo de início da simulação
    global start_time
    start_time = time.time()

    # Inicialização das estações
    for i in range(S):
        station = Station(i)
        stations.append(station)
        station.start()
    
    # Inicialização dos pacotes
    for i in range(P):
        package = Package(i, stations)
        packages.append(package)
        package.start()

    # Inicialização dos logs das estações
    for i in range(S):
        stations[i].begin_log()

    # Inicialização dos carriers
    for i in range(C):
        carrier = Carrier(i, stations, A)
        carriers.append(carrier)
        carrier.start()
    
    
    # Aguarda o fim da execução de todas as threads de carriers
    for carrier in carriers:
        carrier.join()

    # Finaliza as estações
    for station in stations:
        # Finaliza a execução da estação, após não haver mais pacotes a serem entregues
        station.keep_running = False
        station.lock.release()
        
        station.join()

if __name__ == "__main__":
    main()