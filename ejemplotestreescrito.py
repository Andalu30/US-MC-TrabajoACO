"""
Intento del ejemplo de la pagina 18 de las diapositivas
"""

import math
import random



def imprimeferomonas(feromonas):
    print("---------------------")
    for i in feromonas:
        print(i)
    print("---------------------")
def imprimehormigas(hormigas):
    print("---------------------")
    for i in hormigas:
        print(i)
    print("---------------------")



def probabilidad_ij(hormigaK, nodos, feromonas, coste, alpha, beta, i, j):
    
    def sumvecinosNovisitados(hormigaK, nodos, feromonas, coste, alpha, beta,
                              i, j):
        vecinosNoVisitados = conjuntoVecinosAi(i, hormigaK, coste)

        sum = 0
        for s in vecinosNoVisitados:
            n_is = 1 / coste[i][s]
            sum = sum + (feromonas[i][s]**alpha * n_is**beta)
        return sum

    def conjuntoVecinosAi(i, hormigaK, costes):
        vecinos = []
        visitados = hormigaK['nodosVisitados']

        aux = coste[i]
        cont = 0
        for a in aux:
            if a is not None and cont not in visitados:
                vecinos.append(cont)
                cont = cont + 1
            else:
                cont = cont + 1
        return vecinos


    #--------------------
    if j in conjuntoVecinosAi(i, hormigaK, coste):
        n_ij = 1 / coste[i][j]
        prob = (feromonas[i][j]**alpha * n_ij**beta) / sumvecinosNovisitados(
            hormigaK, nodos, feromonas, coste, alpha, beta, i, j)
    else:
        prob = 0

    return prob



def probabilidadHormiga(hormiga, nodos, feromonas, coste, alpha, beta):
    i = hormiga['nodoActual']
    
    probabilidades = []

    for j in range(0, len(nodos)):
        probabilidades.append(
            probabilidad_ij(hormiga, nodos, feromonas, coste, alpha, beta, i, j)
            )
    return probabilidades

def politicaDecision(probabilidades, nodos):
    u = random.random()

    sum = 0
    index = 0
    for probciudad in probabilidades: # No compruebo cuales son las vecinas porque las que no lo son tienen probabilidad 0 y por lo tanto no suman nada.
        sum = sum + probciudad
        if sum > u:
            break
        else:
            index = index + 1
    return index
    
def actualizaHormiga(hormiga, movimiento):

    nodoactu = hormiga['nodoActual']
    nueva_arista = (nodoactu, movimiento)

    hormiga['nodoActual'] = movimiento
    hormiga['nodosVisitados'].append(movimiento)
    hormiga['circuito'].append(nueva_arista)


def costeLongCircuitoHormiga(circuito, costes):
    sum = 0
    for (i,j) in circuito:
        sum = sum + costes[i][j]
    return sum


def actualizaFeromonas(hormigas, feromonas, costes, q=1, rho = 0.1):
   

    def aporteTodasHormigas(hormigas, feromonas, costes, i, j, q):

        aporte = 0
        arista = (i, j)

        for hormiga in hormigas:
            if arista in hormiga['circuito']:
                aporte = aporte + (q / costeLongCircuitoHormiga(hormiga['circuito'], costes))

        return aporte


    for i in range(len(feromonas)):
         
        for j in range(len(feromonas[i])):
            evaporacion = feromonas[i][j]*(1 - rho)
            sumTodasHormigas = aporteTodasHormigas(hormigas, feromonas, costes, i, j, q)

            feromonas[i][j] = evaporacion + sumTodasHormigas
    return feromonas
   
   

def MejorSolucionEncontrada(hormigas, costes):
    
    
    pesoMejorSolucion = math.inf
    for hormiga in hormigas:
        circuito = hormiga['circuito']
        coste = costeLongCircuitoHormiga(circuito, costes)
        if coste < pesoMejorSolucion:
            pesoMejorSolucion = coste
            mejorSolucion = circuito
    
    return mejorSolucion, pesoMejorSolucion



    


# 1 iteracion completa ACO
def iteracionACO():

    #---------------Definicion datos---politicaDecision----------------------|
    # Hiperparámetros
    alpha = 1
    beta = 1

    # Grafo TSP = K6
    nodos = [0,1,2,3,4,5]

    # 6 Hormigas, una en cada nodo.
    hormigas = [        
        {
            'nodoActual':0,
            'nodosVisitados': [0],
            'circuito': []
        },
        {
            'nodoActual':1,
            'nodosVisitados': [1],
            'circuito': []
        },
        {
            'nodoActual':2,
            'nodosVisitados': [2],
            'circuito': []
        },        
        {
            'nodoActual':3,
            'nodosVisitados': [3],
            'circuito': []
        },
        {
            'nodoActual':4,
            'nodosVisitados': [4],
            'circuito': []
        },        
        {
            'nodoActual':5,
            'nodosVisitados': [5],
            'circuito': []
        }
    ]

    feromonas = [[10,10,10,10,10,10],
                 [10,10,10,10,10,10],
                 [10,10,10,10,10,10],
                 [10,10,10,10,10,10],
                 [10,10,10,10,10,10],
                 [10,10,10,10,10,10]]

    costes = [
              [None, 1, math.sqrt(5), math.sqrt(5), 2, math.sqrt(2)],
              [1, None, math.sqrt(2), 2, math.sqrt(5),math.sqrt(5)],
              [math.sqrt(5), math.sqrt(2), None,  math.sqrt(2), math.sqrt(5), 3],
              [math.sqrt(5), 2, math.sqrt(2), None, 1, math.sqrt(5)],
              [2, math.sqrt(5), math.sqrt(5), 1, None, math.sqrt(2)],
              [math.sqrt(2), math.sqrt(5), 3, math.sqrt(5), math.sqrt(2), None]
            ]

    #----------------------------------------------------

    





    # Algoritmo:
    for _ in range(5):

        for hormigaK in hormigas:
            probabilidades = probabilidadHormiga(hormigaK, nodos, feromonas, costes, alpha, beta)
            #print(f"Probabilidades hormiga {hormigaK['nodoActual']}:\n{probabilidades}")

            movimiento = politicaDecision(probabilidades, nodos)
            #print(movimiento)

            actualizaHormiga(hormigaK, movimiento)
            #print(hormigaK)
            
        feromonas = actualizaFeromonas(hormigas, feromonas, costes) 
    
    
    circuitoMejor, pesoMejorSolucion = MejorSolucionEncontrada(hormigas, costes)

    imprimeferomonas(feromonas)
    imprimehormigas(hormigas)
    print(f"La mejor solución encontrada ha sido: {circuitoMejor}, que tiene un peso de {pesoMejorSolucion}")

          
          
      





print('Modificacion!')
iteracionACO()