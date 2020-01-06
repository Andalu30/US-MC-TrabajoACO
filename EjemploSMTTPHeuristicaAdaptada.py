import random
import math
import copy
import numpy as np

#------------------------------------------------------------------------



def actualizaHormiga(hormiga, movimiento):
    nodoactu = hormiga['nodoActual']
    nueva_arista = (nodoactu, movimiento)

    hormiga['nodoActual'] = movimiento
    hormiga['nodosVisitados'].append(movimiento)
    hormiga['circuito'].append(nueva_arista)








def actualizaFeromonasLocal(hormiga,pTime,feromonas,tao_0, m, q=1, rho = 0.1):
    (i,j) = hormiga['circuito'][len(hormiga['circuito'])-1]

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

    


#-----------------------------------------------------------------------------
# Redefinicion de las funciones para que se aplique la Pheromone SummationRule


# def politicaDecision(probabilidades, nodos, u):
    

#     sum = 0
#     index = 0
#     for probciudad in probabilidades: # No compruebo cuales son las vecinas porque las que no lo son tienen probabilidad 0 y por lo tanto no suman nada.
#         sum = sum + probciudad
#         if sum > u:
#             break
#         else:
#             index = index + 1
#     print(index)
#     return index


def politicaDecision(probabilidades, nodos, u, feromonas, i, j, alpha, beta, hormiga, pTime, due_dates):
    decision = None

    aux = random.random()

    if aux <= u:
        #primera formula
        selecciones = []
        
        sum = 0
        for k in range(0,i):

            sum = sum + feromonas[k][j]
            valorNkj = func_n_ij(hormiga,pTime,due_dates,k,j)
        
            if probabilidades[k] == 0:
                selecciones.append(-math.inf)
            else:
                selecciones.append(sum**alpha * valorNkj**beta)

        #print(f'selecciones {selecciones} ')
        decision = selecciones.index(max(selecciones))

    else:
        #segunda formula
        aux2 = random.random()
        sum = 0
        index = 0
        for probciudad in probabilidades:
            sum = sum + probciudad
            if sum > aux2:
                if probciudad != 0:
                    decision = index
                break
            else:
                index = index + 1
        decision = index
    
    return decision

'''    u = random.random()

    sum = 0
    index = 0
    for probciudad in probabilidades: 
        sum = sum + probciudad
        if sum > u:
            break
        else:
            index = index + 1
    return index'''







def func_n_ij(hormiga, pTime, due_dates, i, j):

    circuito = hormiga['circuito']
    T = 0
    for (x,y) in circuito:
        T  = T + pTime[x][y]

    return 1 / (max(T + pTime[i][j], due_dates[i][j]) - T )



# # #(hormigaK, nodos, feromonas, pTime, due_dates, alpha, beta)
# def probabilidadHormiga(hormiga, nodos, feromonas, pTime, due_dates, alpha, beta):

#     #probabilidad_ij(hormiga, nodos, feromonas, pTime, due_dates, alpha, beta, i, j))
#     def probabilidad_ij(hormigaK, nodos, feromonas, coste, due_dates, alpha, beta, i, j):
       
       
#         def sumvecinosNovisitados(hormigaK, nodos, feromonas, coste, alpha, beta,i, j):
#             vecinosNoVisitados = conjuntoVecinosAi(i, hormigaK, coste)

#             sumator = 1
#             for s in vecinosNoVisitados:

#                 suminterno = 0
#                 for k in range(0,i):
#                     suminterno = suminterno + feromonas[s][k]

#                 #print(suminterno)

#                 n_is = func_n_ij(hormiga,pTime,due_dates,i,s) #<---- Cambiado

#                 sumator = sumator + (suminterno**alpha * n_is**beta)
#             return sumator




#         def conjuntoVecinosAi(i, hormigaK, costes):
#             vecinos = []
#             visitados = hormigaK['nodosVisitados']

#             aux = coste[i]
#             cont = 0
#             for a in aux:
#                 if a is not None and cont not in visitados:
#                     vecinos.append(cont)
#                     cont = cont + 1
#                 else:
#                     cont = cont + 1
#             return vecinos



#         #--------------------
#         if j in conjuntoVecinosAi(i, hormigaK, coste):
            
#             n_ij = func_n_ij(hormiga,pTime,due_dates,i,j) #<--- Cambiado

#             sum = 0
#             for k in range(0,i):
#                 sum = sum + feromonas[k][j]


#             prob = (sum**alpha * n_ij**beta) / sumvecinosNovisitados(hormiga, nodos, feromonas, coste, alpha, beta, i, j)

#         else:
#             prob = 0

#         return prob



#     i = hormiga['nodoActual']
    
#     probabilidades = []

#     for j in range(0, len(nodos)):
#         if j == i:
#             probabilidades.append(0)
#         else:
#             probabilidades.append(probabilidad_ij(hormiga, nodos, feromonas, pTime, due_dates, alpha, beta, i, j))
    
#     return probabilidades



def probabilidadHormiga(hormiga, nodos, feromonas, pTime, due_dates, alpha, beta):

    def probabilidad_ij(hormigaK, nodos, feromonas, pTime, due_dates, alpha, beta, i, j):
        def sumvecinosNovisitados(hormigaK, nodos, feromonas, coste, due_dates, alpha, beta, i, j):
            
            vecinosNoVisitados = conjuntoVecinosAi(i, hormigaK, coste)

            sum = 0
            for s in vecinosNoVisitados:
                n_is = func_n_ij(hormiga,pTime,due_dates,i,s) #<---- Cambiado

                sum = sum + (feromonas[i][s]**alpha * n_is**beta)
            return sum

        def conjuntoVecinosAi(i, hormigaK, costes):
            vecinos = []
            visitados = hormigaK['nodosVisitados']

            aux = pTime[i]
            cont = 0
            for a in aux:
                if a is not None and cont not in visitados:
                    vecinos.append(cont)
                    cont = cont + 1
                else:
                    cont = cont + 1
            return vecinos
















        #--------------------
        if j in conjuntoVecinosAi(i, hormigaK, pTime):
            
            n_ij = func_n_ij(hormiga,pTime,due_dates,i,j) #<--- Cambiado

            prob = (feromonas[i][j]**alpha * n_ij**beta) / sumvecinosNovisitados(hormigaK, nodos, feromonas, pTime, due_dates, alpha, beta, i, j)
        else:
            prob = 0

        return prob


    i = hormiga['nodoActual']
    
    probabilidades = []

    for j in range(0, len(nodos)):
        probabilidades.append( probabilidad_ij(hormiga, nodos, feromonas, pTime, due_dates, alpha, beta, i, j))
                                            #(hormigaK, nodos, feromonas, coste, alpha, beta, i, j):
    return probabilidades







# 1 iteracion completa ACO
def iteracionACO():

    #---------------Definicion datos---politicaDecision----------------------|
    # Hiperparámetros
    alpha = 1
    beta = 1

    # Grafo TSP = K6
    nodos = range(40)

    hormigas = []
    for i in range(len(nodos)):
        hormigas.append({
            'nodoActual':i,
            'nodosVisitados': [i],
            'circuito': []
        })
        


    hormigas_iniciales = copy.deepcopy(hormigas)

    processingTimes = [26, 24, 79, 46, 32, 35, 73, 74, 14, 67, 86, 46, 78, 40, 29, 94, 64, 27, 90, 55, 35, 52, 36, 69, 85, 95, 14, 78, 37, 86, 44, 28, 39, 12, 30 ,68 ,70 , 9, 49, 50]

    Weights = [1, 10, 9, 10, 10, 4, 3, 2, 10, 3, 7, 3, 1, 3, 10, 4, 7, 7, 4, 7, 5, 3, 5, 4, 9, 5, 2, 8, 10, 4, 7, 4, 9, 5, 7, 7, 5, 10, 1, 3]

    due_datesInicial = [1588,1620,1731,1773,1694,1487,1566,1844,1727,1636,1599,1539,1855,1645,1709,1660,1582,1836,1484,1559,1772,1510,1512,1795,1522,1509,1598,1658,1826,1628,1650,1833,1627,1528,1541,1497,1481,1446,1579,1814]


    pTime = []
    for i, e in enumerate(processingTimes):
        pTime.append(processingTimes)

    

    pTime = np.matrix(pTime)
    np.fill_diagonal(pTime, 0)
    pTime = pTime.tolist()
    
    

    weights = []
    for i, e in enumerate(Weights):
        weights.append(Weights)

    weights = np.matrix(weights)
    np.fill_diagonal(weights, 0)
    weights = weights.tolist()

    due_dates = []
    for i, e in enumerate(due_datesInicial):
        due_dates.append(due_datesInicial)

    due_dates = np.matrix(due_dates)
    np.fill_diagonal(due_dates, 0)
    due_dates = due_dates.tolist()




    

    def Tedd():
        Tedd = 0
        for d in due_datesInicial:
            Tedd = Tedd + 1/d
        return Tedd


    #print(f'Tedd= {Tedd()}')

    tao_0 = 1 / len(hormigas) * Tedd()

    feromonas = []
    for i in range(len(nodos)):
        aux = []
        for j in range(len(nodos)):
            if i == j:
                aux.append(0)
            else:
                aux.append(Tedd())
        feromonas.append(aux)
    

    # feromonas = [[0,Tedd(),Tedd(),Tedd(),Tedd(),Tedd()],
    #              [Tedd(),0,Tedd(),Tedd(),Tedd(),Tedd()],
    #              [Tedd(),Tedd(),0,Tedd(),Tedd(),Tedd()],
    #              [Tedd(),Tedd(),Tedd(),0,Tedd(),Tedd()],
    #              [Tedd(),Tedd(),Tedd(),Tedd(),0,Tedd()],
    #              [Tedd(),Tedd(),Tedd(),Tedd(),Tedd(),0]]
    
    u = random.random()

    #----------------------------------------------------
     # Soluciones de verdad
    circuitoMejor = []
    pesoMejorSolucion = math.inf # Para minimizacion
    
    for iteracion in range(9):
        # Hacerlo n veces, el numero de iteraciones, hasta criterio de parada
        print(f'Iteración {iteracion}')

       


        for _ in range(len(pTime)-1): # Bucle para optener un recorrido por todos los nodos
            for hormigaK in hormigas:
                probabilidades = probabilidadHormiga(hormigaK, nodos, feromonas, pTime, due_dates, alpha, beta)
                #print(f"Probabilidades hormiga {hormigaK['nodoActual']}:\n{probabilidades}")

                
                #movimiento = politicaDecision(probabilidades, nodos, u)
                movimiento = politicaDecision(probabilidades, nodos, u, feromonas, i,j,alpha,beta, hormigaK,pTime,due_dates)
                
                #print(movimiento)

                actualizaHormiga(hormigaK, movimiento)
                #print(hormigaK)
                

                #local
                actualizaFeromonasLocal(hormigaK,pTime,feromonas,tao_0,len(hormigas),q=100, rho=0.5)


        # Soluciones parciales
        circuitoMejoractual, pesoMejorSolucionactual = MejorSolucionEncontrada(hormigas, pTime)

        print(circuitoMejoractual, pesoMejorSolucionactual)



        #aunMejorCircuito, aunMejorPeso = opt2Strategy(circuitoMejoractual, pesoMejorSolucionactual, pTime)

        #aunMejorCircuito, aunMejorPeso = circuitoMejoractual, pesoMejorSolucionactual


        # Actualizacion de las soluciones finales
        if pesoMejorSolucionactual < pesoMejorSolucion:
            pesoMejorSolucion = pesoMejorSolucionactual
            circuitoMejor = circuitoMejoractual


        actualizaFeromonasGlobal(hormigas, pTime, feromonas,circuitoMejor, q=1, rho = 0.1)

        #print(np.matrix(feromonas))



       

        print(f'Parcial: {pesoMejorSolucionactual}, final: {pesoMejorSolucion}')


        # Reinicializacion de las hormigas pero no de las feromonas?
        hormigas = copy.deepcopy(hormigas_iniciales)

        #imprimeferomonas(feromonas)

        
    
    print(f"La mejor solución encontrada ha sido: {circuitoMejor}, que tiene un peso de {pesoMejorSolucion}")

    #imprimeferomonas(feromonas)
    # imprimehormigas(hormigas)

          
iteracionACO()




