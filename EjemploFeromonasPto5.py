import ClaseTSP


"""
Intento del ejemplo de SMTTP
"""

import math
import random
import copy


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



def func_n_ij(hormiga, pTime, due_dates, i, j):

    circuito = hormiga['circuito']
    T = 0
    for (i,j) in circuito:
        T  = T + pTime[i][j]

    return 1 / (math.max(T + pTime[i][j], due_dates[i][j]) - T)



def probabilidadHormiga(hormiga, nodos, feromonas, pTime, due_dates, alpha, beta):

    def probabilidad_ij(hormigaK, nodos, feromonas, coste, alpha, beta, i, j):
        def sumvecinosNovisitados(hormigaK, nodos, feromonas, coste, alpha, beta,
                                i, j):
            vecinosNoVisitados = conjuntoVecinosAi(i, hormigaK, coste)

            sum = 0
            for s in vecinosNoVisitados:
                n_is = func_n_ij(hormiga,pTime,due_dates,i,s) #<---- Cambiado

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
            
            n_ij = func_n_ij(hormiga,pTime,due_dates,i,j) #<--- Cambiado

            prob = (feromonas[i][j]**alpha * n_ij**beta) / sumvecinosNovisitados(hormigaK, nodos, feromonas, coste, alpha, beta, i, j)
        else:
            prob = 0

        return prob
    i = hormiga['nodoActual']
    
    probabilidades = []

    for j in range(0, len(nodos)):
        probabilidades.append(probabilidad_ij(hormiga, nodos, feromonas, pTime, due_dates, alpha, beta, i, j))
    return probabilidades

def politicaDecision(probabilidades, nodos, u):
    

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







def actualizaFeromonasLocal(hormiga,pTime,feromonas,tao_0, m, q=1, rho = 0.1):
  
    (i,j) = hormiga['circuito'][len(hormiga['circuito'])]

    feromonas_ij = feromonas[i][j]
    feromonas[i][j] = (1-rho) * feromonas_ij + rho * tao_0
    feromonas[j][i] = (1-rho) * feromonas_ij + rho * tao_0


  
def actualizaFeromonasGlobal(hormigas, pTime, feromonas, solucionMejor, q=1, rho = 0.1):
    
    T_star = 0
    for (i,j) in solucionMejor:
        T_star = T_star + pTime[i][j]
    
    
    for i in range(len(feromonas)):
        for j in range(len(feromonas[i])):
            
            #*************************
            disipacion = feromonas[i][j] * (1-rho) # Disipacion
            #******

        
            if(i<j):

                #*************************
                feromonas[i][j] = disipacion + rho * (1/T_star)
                feromonas[j][i] = disipacion + rho * (1/T_star)
            #*************************

            if i == j:

                #*************************
              feromonas[i][j] = disipacion

                #*************************

           # print("actualizada: --")
           # print(feromonas[i][j])
            #print("-----------------------------------")






def MejorSolucionEncontrada(hormigas, costes):
        
    def costeLongCircuitoHormiga(circuito, costes):
        sum = 0
        for (i,j) in circuito:
            sum = sum + costes[i][j]
        return sum
    
    pesoMejorSolucion = math.inf
    for hormiga in hormigas:
        circuito = hormiga['circuito']
        coste = costeLongCircuitoHormiga(circuito, costes)
        if coste < pesoMejorSolucion:
            pesoMejorSolucion = coste
            mejorSolucion = circuito
    
    return mejorSolucion, pesoMejorSolucion

    


from itertools import permutations

def opt2Strategy(circuitoMejoractual, pesoMejorSolucionactual, pTime):

    aunMejorCircuito = circuitoMejoractual
    aunMejorPeso = pesoMejorSolucionactual
    
    perms = permutations(circuitoMejoractual)

    for p in perms:
        peso = 0
        for (i,j) in p:
            peso = peso + pTime[i][j]
        
        if peso < aunMejorPeso:
            aunMejorCircuito = p
            aunMejorPeso = peso

    return aunMejorCircuito, aunMejorPeso













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

    hormigas_iniciales = copy.deepcopy(hormigas)


    pTime = [
              [None, 1, math.sqrt(5), math.sqrt(5), 2, math.sqrt(2)],
              [1, None, math.sqrt(2), 2, math.sqrt(5),math.sqrt(5)],
              [math.sqrt(5), math.sqrt(2), None, math.sqrt(2), math.sqrt(5), 3],
              [math.sqrt(5), 2, math.sqrt(2), None, 1, math.sqrt(5)],
              [2, math.sqrt(5), math.sqrt(5), 1, None, math.sqrt(2)],
              [math.sqrt(2), math.sqrt(5), 3, math.sqrt(5), math.sqrt(2), None]
            ]

    due_dates = [
                [],
                [],
                [],
                [],
                [],
                []
                ]
    

    def Tedd():
        Tedd = 0
        for i in due_dates:
            for j in due_dates[i]:
                Tedd = Tedd + 1/due_dates[i][j]
        return Tedd

    # TODO
    tao_0 = 1 / len(hormigas) * Tedd()

    feromonasAux = [[Tedd()]*len(due_dates)]*len(due_dates)
    feromonas = copy.deepcopy(feromonasAux)

    feromonas = [[0,Tedd(),Tedd(),Tedd(),Tedd(),Tedd()],
                 [Tedd(),0,Tedd(),Tedd(),Tedd(),Tedd()],
                 [Tedd(),Tedd(),0,Tedd(),Tedd(),Tedd()],
                 [Tedd(),Tedd(),Tedd(),0,Tedd(),Tedd()],
                 [Tedd(),Tedd(),Tedd(),Tedd(),0,Tedd()],
                 [Tedd(),Tedd(),Tedd(),Tedd(),Tedd(),0]]
    
    u = random.random()

    #----------------------------------------------------

    
    for iteracion in range(1000):
        # Hacerlo n veces, el numero de iteraciones, hasta criterio de parada
        print(f'Iteración {iteracion}')

        # Soluciones de verdad
        circuitoMejor = []
        pesoMejorSolucion = math.inf # Para minimizacion


        for _ in range(len(pTime)-1): # Bucle para optener un recorrido por todos los nodos
            for hormigaK in hormigas:
                probabilidades = probabilidadHormiga(hormigaK, nodos, feromonas, pTime, due_dates, alpha, beta)
                #print(f"Probabilidades hormiga {hormigaK['nodoActual']}:\n{probabilidades}")

                movimiento = politicaDecision(probabilidades, nodos, u)
                #print(movimiento)

                actualizaHormiga(hormigaK, movimiento)
                #print(hormigaK)
                

                #local
                actualizaFeromonasLocal(hormigaK, pTime, feromonas, tao_0, q=100, rho=0.5)


        # Soluciones parciales
        circuitoMejoractual, pesoMejorSolucionactual = MejorSolucionEncontrada(hormigas, pTime)

        aunMejorCircuito, aunMejorPeso = opt2Strategy(circuitoMejoractual, pesoMejorSolucionactual, pTime)

        actualizaFeromonasGlobal(hormigas, pTime, feromonas,aunMejorCircuito, q=1, rho = 0.1)


        # Actualizacion de las soluciones finales
        if aunMejorPeso < pesoMejorSolucion:
            pesoMejorSolucion = aunMejorPeso
            circuitoMejor = aunMejorCircuito

        # Reinicializacion de las hormigas pero no de las feromonas?
        hormigas = copy.deepcopy(hormigas_iniciales)

        #imprimeferomonas(feromonas)

        
    
    print(f"La mejor solución encontrada ha sido: {circuitoMejor}, que tiene un peso de {pesoMejorSolucion}")

    #imprimeferomonas(feromonas)
    # imprimehormigas(hormigas)

          
iteracionACO()