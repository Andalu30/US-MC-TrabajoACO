"""
Intento del ejemplo de la pagina 18 de las diapositivas
"""

import math
import random

''' hormigas = [
    {
        'nodosVisitados': [],
        'circuito': []
    },  # Hormiga 1
    {
        'nodosVisitados': [1],
        'circuito': [(0, 1)]
    }  # Hormiga 2
]

nodos = ['0', '1', '2', '3', '4', '5', '6']

feromonas = [[-1, 2, 12, 6, 3, 5, 2], 
            ['2', -1, -1, -1, -1, -1, -1],
            ['12', -1, -1, -1, -1, -1, -1],
            ['6', -1, -1, -1, -1, -1, -1],
            ['3', -1, -1, -1, -1, -1, -1],
            ['5', -1, -1, -1, -1, -1, -1],
            ['2', -1, -1, -1, -1, -1, -1]]

coste = [[-1, 4, 6, 5, 4, 3, 2],
        ['4', -1, -1, -1, -1, -1, -1],
        ['6', -1, -1, -1, -1, -1, -1],
        ['5', -1, -1, -1, -1, -1, -1],
        ['4', -1, -1, -1, -1, -1, -1],
        ['3', -1, -1, -1, -1, -1, -1],
        ['2', -1, -1, -1, -1, -1, -1]] '''


def probabilidad_ij(hormigaK, nodos, feromonas, coste, alpha, beta, i, j):
    def sumvecinosNovisitados(hormigaK, nodos, feromonas, coste, alpha, beta,
                              i, j):
        vecinosNoVisitados = conjuntoVecinosAi(i, hormigaK, coste)

        sum = 0
        for s in vecinosNoVisitados:
            n_is = 1 / coste[i][int(s)]
            sum = sum + (feromonas[i][int(s)]**alpha * n_is**beta)
        return sum

    def conjuntoVecinosAi(i, hormigaK, costes):
        vecinos = []
        visitados = hormigaK['nodosVisitados']

        aux = coste[i]
        cont = 0
        for a in aux:
            if a != -1 and cont not in visitados:  # -1 seria el NoExisteEnLaMatriz
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



'''print('Cálculo de probabilidades:\n')

print('Sin ignorar ningun nodo:')
for i in range(1, 7):
    print(probabilidad_ij(hormigas[0], nodos, feromonas, coste, 1, 1, 0, i))

print('----------------------')
print('Con una hormiga que ya ha estado en el nodo 1: (2º ejemplo))')
for i in range(1, 7):
    print(probabilidad_ij(hormigas[1], nodos, feromonas, coste, 1, 1, 0, i))
print("--------------------------------------------\n\n") '''



def probabilidadHormiga(hormiga, nodos, feromonas, coste, alpha, beta):
    i = hormiga['nodoActual']
    
    probabilidades = []

    for j in range(0, len(nodos)):
        probabilidades.append(probabilidad_ij(hormiga, nodos, feromonas, coste, alpha, beta, i, j))
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

def actualizaFeromonas(hormigas, costes, feromonas, q=1, rho = 0.1):
    # circuitos de hormigas

    costeCircuito = []

    for hormigaK in hormigas:
        aux = 0
        for t in hormigaK['circuito']:
            i, j = t[0],t[1] #arista del circuito
            aux = aux + costes[i][j]
        costeCircuito.append(aux)
    
    #print(f'Costes Circuitos: {costeCircuito}')

    # Coste del circuito es una lista con los costes de los circuitos de todas las hormigas


    #actualizar feromonas
    for i in range(len(feromonas)):
        for j in range(len(feromonas[i])):
            disipacion = feromonas[i][j] * (1-rho) # Disipacion

            r = 0
            #hay que poner que no se actualice si es el mismo nodo
            #if i == j:
            #    feromonas[i][j] = 0.0001 #TODO 
            #if i != j:
            #    for x in range(len(hormigas)):
            #        hormigaK = hormigas[x]
            #        if (i,j) in hormigaK['circuito']:
            #            r = r + q / costeCircuito[x]
            feromonas[i][j] = disipacion + r


    


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

    feromonas = [[10]*6]*6 #Matriz 6*6

    costes = [
              [-1, 1, math.sqrt(5), math.sqrt(5), 2, math.sqrt(2)],
              [1, -1, math.sqrt(2), 2, math.sqrt(5),math.sqrt(5)],
              [math.sqrt(5), math.sqrt(2), -1, math.sqrt(2), math.sqrt(5), 3],
              [math.sqrt(5), 2, math.sqrt(2), -1, 1, math.sqrt(5)],
              [2, math.sqrt(5), math.sqrt(5), 1, -1, math.sqrt(2)],
              [math.sqrt(2), math.sqrt(5), 3, math.sqrt(5), math.sqrt(2), -1]
            ]

    #----------------------------------------------------

    

    for _ in range(4):

        for hormigaK in hormigas:
            probabilidades = probabilidadHormiga(hormigaK, nodos, feromonas, costes, alpha, beta)
            #print(f"Probabilidades hormiga {hormigaK['nodoActual']}:\n{probabilidades}")

            movimiento = politicaDecision(probabilidades, nodos)
            #print(movimiento)

            actualizaHormiga(hormigaK, movimiento)
            #print(hormigaK)
            
        actualizaFeromonas(hormigas, costes, feromonas) 

    print(f'Feromonas nuevas: {feromonas}')
    #print(hormigas)

          
          
      






iteracionACO()