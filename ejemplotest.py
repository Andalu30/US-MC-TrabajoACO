hormigas = [{'nodosVisitados': [],
             'circuito':[]}, # Hormiga 1
            {'nodosVisitados': [1],
             'circuito':[(0,1)]}  # Hormiga 2
            ]


nodos = ['0','1','2','3','4','5','6']

feromonas = [['-',2  ,12 ,6  ,3  ,5, 2],
             ['-','-','-','-','-','-','-'],
             ['-','-','-','-','-','-','-'],
             ['-','-','-','-','-','-','-'],
             ['-','-','-','-','-','-','-'],
             ['-','-','-','-','-','-','-'],
             ['-','-','-','-','-','-','-']
            ]

coste = [['-',4  ,6  ,5  ,5  ,3  ,2],
         ['-','-','-','-','-','-','-'],
         ['-','-','-','-','-','-','-'],
         ['-','-','-','-','-','-','-'],
         ['-','-','-','-','-','-','-'],
         ['-','-','-','-','-','-','-'],
         ['-','-','-','-','-','-','-']
        ]



def probabilidad_ij(hormigaK, feromonas, coste, alpha, beta, i, j):
    def sumvecinosNovisitados(hormigaK, feromonas, coste, alpha, beta, i, j):
        visitados = hormigaK['nodosVisitados']

        sum = 0
        for s in nodos:
            if s in visitados:
                print('La hormiga ya ha pasado por este nodo')
                break
            elif coste[i][int(s)] != '-':
                n_is = 1/coste[i][int(s)]
                sum = sum + (feromonas[i][int(s)]**alpha * n_is**beta)
        return sum

    def conjuntoVecinosAi(i):
        vecinos = []
        aux = coste[i]
        cont = 0
        for a in aux:
            if a != '-':
                vecinos.append(cont)
                cont = cont + 1
            else:
                cont = cont + 1
        return vecinos


    #--------------------
    if j not in conjuntoVecinosAi(i):
        prob = 0
    else:
        n_ij = 1 / coste[i][j]
        prob = (feromonas[i][j]**alpha * n_ij**beta) / sumvecinosNovisitados(hormigaK, feromonas, coste, alpha, beta, i, j)
    return prob



# for hormigaK in hormigas:

print('Probabilidades del ejemplo de las diapositivas:\n')

print('Sin ignorar ningun nodo:')
for i in range(1,7):
    print(probabilidad_ij(hormigas[0], feromonas,coste,1,1,0,i))

print('----------------------')
print('Con una hormiga que ya ha estado en el nodo 1: (no funciona)')
for i in range(1,7):
    print(probabilidad_ij(hormigas[1], feromonas,coste,1,1,0,i))





# Actualizacion feromonas

def actualizacionFeromonas(feromonas, tao, hormigas,i,j):

    def circuitoHormiga(circuitoHormiga):
        sol = 0
        for c in circuitoHormiga:
            i = c[0]
            j = c[1]
            sol = sol + coste[i][j]
        return sol

    def aportehormigas(hormigas, Q=1):
        aporte = 0
        for hormiga in hormigas:
            circuitoHormiga = hormiga['circuito']

            if ij in circuitoHormiga:
                aporte = Q / costeCircuitoHormiga(circuitoHormiga)
            else:
                aporte = 0
        return aporte


    for i in range(feromonas):
        for j in range(feromonas[0]):
            feromonas[i][j] = (1 - tao)*feromonas[i][j] + aportehormigas(hormigas, Q, i,j)





