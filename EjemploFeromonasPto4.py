import ClaseSMTTP
import random
import math

# Redefinicion de las funciones para que se aplique la Pheromone SummationRule


def politicaDecision(probabilidades, nodos, u, feromonas, i, j, alpha, beta, hormiga, pTime, due_dates):
    decision = None

    aux = random.random()
    if aux <= u:
        #primera formula

        selecciones = []
        
        sum = 0
        for k in range(0,i):
            sum = sum + feromonas[k][j]
            valorNij = func_n_ij(hormiga,pTime,due_dates,k,j)

            selecciones.append(sum**alpha * valorNij**beta)

        decision = selecciones.index(max(selecciones))

    else:
        #segunda formula
        aux2 = random.random()
        sum = 0
        index = 0
        for probciudad in probabilidades:
            if sum > aux2:
                break
            else:
                index = index + 1
        decision = index
    
    return decision



def func_n_ij(hormiga, pTime, due_dates, i, j):

    circuito = hormiga['circuito']
    T = 0
    for (i,j) in circuito:
        T  = T + pTime[i][j]

    return 1 / math.max(T + pTime[i][j], due_dates[i][j])


def probabilidadHormiga(hormiga, nodos, feromonas, pTime, due_dates, alpha, beta):

    def probabilidad_ij(hormigaK, nodos, feromonas, coste, alpha, beta, i, j):
        def sumvecinosNovisitados(hormigaK, nodos, feromonas, coste, alpha, beta,
                                i, j):
            vecinosNoVisitados = conjuntoVecinosAi(i, hormigaK, coste)

            sum = 0
            for s in vecinosNoVisitados:

                suminterno = 0
                for k in range(0,i):
                    suminterno = suminterno + feromonas[k][j]

                n_is = func_n_ij(hormiga,pTime,due_dates,i,s) #<---- Cambiado

                sum = sum + (suminterno**alpha * n_is**beta)
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

            sum = 0
            for k in range(0,i):
                sum = sum + feromonas[k][j]


            prob = (sum**alpha * n_ij**beta) / sumvecinosNovisitados(hormigaK, nodos, feromonas, coste, alpha, beta, i, j)



        else:
            prob = 0

        return prob
    i = hormiga['nodoActual']
    
    probabilidades = []

    for j in range(0, len(nodos)):
        probabilidades.append(probabilidad_ij(hormiga, nodos, feromonas, pTime, due_dates, alpha, beta, i, j))
    return probabilidades










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

# costes = [
#             [None, 1, math.sqrt(5), math.sqrt(5), 2, math.sqrt(2)],
#             [1, None, math.sqrt(2), 2, math.sqrt(5),math.sqrt(5)],
#             [math.sqrt(5), math.sqrt(2), None, math.sqrt(2), math.sqrt(5), 3],
#             [math.sqrt(5), 2, math.sqrt(2), None, 1, math.sqrt(5)],
#             [2, math.sqrt(5), math.sqrt(5), 1, None, math.sqrt(2)],
#             [math.sqrt(2), math.sqrt(5), 3, math.sqrt(5), math.sqrt(2), None]
#         ]








# algoritmo = AlgoritmoACOparaTSP(hormigas, feromonas, costes, nodos, alpha, beta)
# circuito, peso = algoritmo.ejecutaAlgoritmo() # 100 iteraciones,  q = 1, rho = 0.5

# #------------------------------------------

# alpha = 1
# beta = 1

# algoritmo = AlgoritmoACOparaTSP(hormigas, feromonas, costes, nodos, alpha, beta)
# circuito, peso = algoritmo.ejecutaAlgoritmo() # 100 iteraciones,  q = 1, rho = 0.5
