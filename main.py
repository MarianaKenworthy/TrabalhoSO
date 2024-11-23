import threading
import time
import random
import sys
import os

# Coloquei uns nomes que fazem mais ou menos sentido com a abreviação, se quiser mudar fique a vontade

# S = nº de Stations
# C = nº de Carriers
# P = nº de Packages
# A = Carrier.capacity (amount ficaria esquisitasso e nem faria sentido)

class Package(threading.Thread):
    def __init__(self, package_id, redist_stations):
        super.__init__(self)
        self.package_id = package_id
        order = random.sample(redist_stations, 2)
        self.origin = order[0]
        origin.to_deliver_packages.append(self)
        self.destination = order[1]
        self.redist_stations = redist_stations
        self.lock = threading.Semaphore(0)

    def end_delivery(self):
        filename = f"log_package{self.package_id}.txt"
        f = open(filename, "a")
        f.write(f"Package {self.package_id} was delivered at time {time.time()}\n")

        self.join()
    

    def begin_log(self):
        filename = f"log_package{self.package_id}.txt"
        f = open(filename, "w")

        f.write(f"Package {self.package_id} was created at time {time.time()}\n")
        f.write(f"Package {self.package_id} was sent from station {self.origin.station_id} to station {self.destination.station_id}\n")
        #conferir isso aqui
        f.write(f"Package arrived at origin at time {time.time()}\n")
        f.close()


class Carrier(threading.Thread):
    def __init__(self, carrier_id, redist_stations, capacity):
        super.__init__(self)
        self.carrier_id = carrier_id
        self.redist_stations = redist_stations
        self.capacity = capacity
        self.carried_packages = []
        self.current_station = random.choice(redist_stations)
        self.lock = threading.Semaphore(0)

    def load_package(self, package):
        if (self.capacity - len(self.carried_packages)) > 0:
            self.carried_packages.append(package)
            package.origin.to_deliver_packages.remove(package)

            filename = f"log_package{package.package_id}.txt"
            f = open(filename, "a")
            f.write(f"Package {package.package_id} was loaded by carrier {self.carrier_id} at time {time.time()}\n")
            print(f"Carrier {self.carrier_id} loaded package {package.package_id} from station {package.origin.station_id} at time {time.time()}")
        
    def unload_package(self, package):
        delivered_packages = []

        for i in len(self.carried_packages):
            if self.carried_packages[i].destination == self.current_station:
                delivered_packages.append(self.carried_packages[i])
                print(f"Carrier {self.carrier_id} unloaded package {self.carried_packages[i].package_id} on station {self.current_station} at time {time.time()}")
                removed_package = self.carried_packages.pop(self.carried_packages[i])
                removed_package.end_delivery()
                time.sleep(0.5)
            
        return delivered_packages
        
    def travel(self):
        next_station_index = (self.redist_stations.index(self.current_station) + 1) % len(self.redist_stations)
        self.current_station.carriers.remove(self)
        travel_time = random.uniform(1, 10)
        print(f"Carrier {self.carrier_id} traveling to station {self.current_station.station_id} for {travel_time} seconds")
        time.sleep(travel_time)
        self.current_station = self.redist_stations[next_station_index]

    def run(self):

        while sum(station.get_to_deliver_packages_count() for station in self.redist_stations) > 0 or len(self.carried_packages) > 0:

            self.lock.acquire()
            self.current_station.add_carrier(self)
            self.lock.release()
                
            self.travel()

                




class Station(threading.Thread):
    def __init__(self, station_id):
        super.__init__(self)
        self.station_id = station_id
        self.to_deliver_packages = []
        self.received_packages = []
        self.carriers = []

    def add_carrier(self, carrier):
        self.carriers.append(carrier)

    def get_to_deliver_packages_count(self):
        return len(self.to_deliver_packages)

    def run(self): 
        while len(self.to_deliver_packages) > 0:

            for i in range(self.carriers):

                if len(self.carriers[i].carried_packages) < self.carriers[i].capacity:
                    for package in self.to_deliver_packages:
                        self.carriers[i].load_package(package)
                        time.sleep(0.5)

                self.carriers[i].delivered_packages = self.carriers[i].unload_package(package)

                if len(self.carriers[i].delivered_packages) > 0:
                    for package in self.carriers[i].delivered_packages:
                        self.received_packages.append(package)
                        package.end_delivery()



if len(sys.argv) != 5:
    print("Usage: python Untitled-1.py <S> <C> <P> <A>")
    exit()

S = int(sys.argv[1])
C = int(sys.argv[2])
P = int(sys.argv[3])
A = int(sys.argv[4])

if P <= A or P <= C or A <= C:
    print("Insufficient packages to distribute")
    exit()

def main():
    stations = []
    carriers = []
    packages = []

    for i in range(S):
        station = Station(i)
        stations.append(station)
        station.start()
    
    for i in range(C):
        carrier = Carrier(i, stations, A)
        carriers.append(carrier)
        carrier.start()
    
    for i in range(P):
        package = Package(i, stations)
        packages.append(package)
        package.start()

    """ 
        package não tá em join pq pelo q entendi a thread encerra quando a entrega é feita, 
        mas tbm não sei se dá pra fazer isso em um método da própria classe
    """
    for carrier in carriers:
        carrier.join()

    for station in stations:
        station.join()