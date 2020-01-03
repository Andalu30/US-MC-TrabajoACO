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



def probabilidadHormiga(hormiga, nodos, feromonas, coste, alpha, beta):

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
            prob = (feromonas[i][j]**alpha * n_ij**beta) / sumvecinosNovisitados(hormigaK, nodos, feromonas, coste, alpha, beta, i, j)
        else:
            prob = 0

        return prob
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

def actualizaFeromonas(hormigas, costes, feromonas, q, rho):
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
    #print(range(len(feromonas)))
    for i in range(len(feromonas)):

      # TODO borrar prints

        #print(feromonas)
        for j in range(len(feromonas[i])):
            disipacion = feromonas[i][j] * (1-rho) # Disipacion
           # print("-----------------------------------")
           # print(i,j)
           # print(feromonas[i][j])

            
            r = 0
            #hay que poner que no se actualice si es el mismo nodo
            #if i == j:
            #    feromonas[i][j] = 0.0001 #TODO 
            if i < j:
                for x in range(len(hormigas)):
                    hormigaK = hormigas[x]
                    if (i,j) in hormigaK['circuito'] or (j,i) in hormigaK['circuito']:
                        r = r + q / costeCircuito[x]

                feromonas[i][j] = disipacion + r
                feromonas[j][i] = disipacion + r

            if i == j:
              feromonas[i][j] = disipacion

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

    



#-----------------------------------------
          
      







class AlgoritmoACOparaTSP():

    def __init__(self, hormigas, feromonas, costes, nodos, alpha, beta):
        self.hormigas = hormigas
        self.hormigas_iniciales = copy.deepcopy(self.hormigas)

        self.feromonas = feromonas
        self.costes = costes
        self.nodos = nodos
        
        self.alpha = alpha
        self.beta = beta
        
        
    def ejecutaAlgoritmo(self, iteraciones=100, q = 1, rho = 0.5):
    
    
        for iteracion in range(iteraciones):
            # Hacerlo n veces, el numero de iteraciones, hasta criterio de parada
            print(f'Iteración {iteracion}')

            # Soluciones de verdad
            circuitoMejor = []
            pesoMejorSolucion = math.inf # Para minimizacion


            for _ in range(len(self.costes)-1): # Bucle para optener un recorrido por todos los nodos
                for hormigaK in self.hormigas:
                    probabilidades = probabilidadHormiga(hormigaK, self.nodos, self.feromonas, self.costes, self.alpha, self.beta)
                    
                    movimiento = politicaDecision(probabilidades, self.nodos)
                    actualizaHormiga(hormigaK, movimiento)
                
                    
                actualizaFeromonas(self.hormigas, self.costes, self.feromonas, q, rho)

            # Soluciones parciales
            circuitoMejoractual, pesoMejorSolucionactual = MejorSolucionEncontrada(self.hormigas, self.costes)

            # Actualizacion de las soluciones finales
            if pesoMejorSolucionactual < pesoMejorSolucion:
                pesoMejorSolucion = pesoMejorSolucionactual
                circuitoMejor = circuitoMejoractual

            # Reinicializacion de las hormigas pero no de las feromonas?
            self.hormigas = copy.deepcopy(self.hormigas_iniciales)
        
        print(f"La mejor solución encontrada ha sido: {circuitoMejor}, que tiene un peso de {pesoMejorSolucion}")
        return circuitoMejor, pesoMejorSolucion
    















# #------------------------------------------

# alpha = 1
# beta = 1

# # Grafo TSP = K6
# nodos = [0,1,2,3,4,5]

# # 6 Hormigas, una en cada nodo.
# hormigas = [        
#     {
#         'nodoActual':0,
#         'nodosVisitados': [0],
#         'circuito': []
#     },
#     {
#         'nodoActual':1,
#         'nodosVisitados': [1],
#         'circuito': []
#     },
#     {
#         'nodoActual':2,
#         'nodosVisitados': [2],
#         'circuito': []
#     },        
#     {
#         'nodoActual':3,
#         'nodosVisitados': [3],
#         'circuito': []
#     },
#     {
#         'nodoActual':4,
#         'nodosVisitados': [4],
#         'circuito': []
#     },        
#     {
#         'nodoActual':5,
#         'nodosVisitados': [5],
#         'circuito': []
#     }
# ]

# feromonas = [[0,10,10,10,10,10],
#             [10,0,10,10,10,10],
#             [10,10,0,10,10,10],
#             [10,10,10,0,10,10],
#             [10,10,10,10,0,10],
#             [10,10,10,10,10,0]]
#             [1, None, math.sqrt(2), 2, math.sqrt(5),math.sqrt(5)],
#             [math.sqrt(5), math.sqrt(2), None, math.sqrt(2), math.sqrt(5), 3],
#             [math.sqrt(5), 2, math.sqrt(2), None, 1, math.sqrt(5)],
#             [2, math.sqrt(5), math.sqrt(5), 1, None, math.sqrt(2)],
#             [math.sqrt(2), math.sqrt(5), 3, math.sqrt(5), math.sqrt(2), None]
#         ]








# algoritmo = AlgoritmoACOparaTSP(hormigas, feromonas, costes, nodos, alpha, beta)
# circuito, peso = algoritmo.ejecutaAlgoritmo() # 100 iteraciones,  q = 1, rho = 0.5
