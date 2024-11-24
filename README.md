# Trabalho de Sistemas Operacionais
## Descrição
A proposta do projeto é desenvolver uma aplicação concorrente que simule o comportamento de uma rede de entregas, em que encomendas são transportadas por veículos de um ponto de redistribuição a outro.

A aplicação foi desenvolvida em python e utiliza as seguintes bibliotecas:
- threading
- time
- random
- sys

## Funcionamento e Implementação
Escolhemos dar nomes semanticos às variaveis S, C, P e A: Station, Carrier, Package e cApacity, respectivamente. Ademais, optamos por uma abordagem com classes, de forma que cada elemento correspondesse a um conjunto de funções e variáveis no qual cada instancia possui sua respectiva thread (vide classes Package, Carrier e Station).

Implementados nas funções de cada classe quando necessário estão semáforos que impedem que mais de uma carrier entre ao mesmo tempo numa estação e garantem que somente uma carrier seja carregada por vez. Há também um semáforo para manejar o log dos pacotes. 

Ao rodar o programa, são gerados logs que permitem acompanhar os eventos de cada pacote e em cada estação.