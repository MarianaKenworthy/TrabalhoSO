import threading
import time
import random
import sys

# Coloquei uns nomes que fazem mais ou menos sentido com a abreviação, se quiser mudar fique a vontade

# S = nº de Stations
# C = nº de Carriers
# P = nº de Packages
# A = Carrier.capacity (amount ficaria esquisitasso e nem faria sentido)

class Package(threading.Thread):
    def __init__(self, package_id, redist_stations):
        threading.Thread.__init__(self)
        self.package_id = package_id
        order = random.sample(redist_stations, 2)
        self.origin = order[0]
        self.destination = order[1]
        self.redist_stations = redist_stations

class Carrier(threading.Thread):
    def __init__(self, carrier_id, redist_stations, capacity):
        threading.Thread.__init__(self)
        self.carrier_id = carrier_id
        self.redist_stations = redist_stations
        self.capacity = capacity
        self.packages = []
        self.current_station = random.choice(redist_stations)

class Station(threading.Thread):
    def __init__(self, station_id):
        threading.Thread.__init__(self)
        self.station_id = station_id
        self.packages = []
        self.carriers = []

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