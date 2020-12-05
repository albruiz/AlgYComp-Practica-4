import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from mpl_toolkits import mplot3d
from pylab import *

import random



def generaLaberinto(size, ratio, semilla):
    matriz_size = size*2+1
    matriz = np.zeros((matriz_size,matriz_size))
    # Rellena con habitación o pared
    count = 0
    for i in range(matriz_size):
        for j in range(matriz_size):
            if i % 2 == 1 and j % 2 == 1: matriz[i][j] = 0
            else: 
                matriz[i][j] = 10
                count += 1
    num_doors = 2 * (size-1) * (size-1)
    open = ratio * num_doors

        # Quita paredes
    random.seed(a = semilla, version = 2)
    for i in range(open):
        row,col = 0, 0
        vert_horz = random.randint(0,1)       
        if  vert_horz == 0 :
            row = random.randint(0,size-1)
            col = random.randint(0,size-2)
            
            row = row * 2 + 1
            col = col * 2 + 2 
        else:
            row = random.randint(0,size-2)
            col = random.randint(0,size-1)
            
            row = row * 2 + 2
            col = col * 2 + 1 
            
        matriz[row][col] = random.randint(0,9)

    # Escoge y marca habitación de salida
    rowSal = random.randint(0, size-1)
    colSal = random.randint(0, size-1)
    
    xsalida,ysalida = rowSal*2+1, colSal*2+1
    matriz[xsalida][ysalida] = -1 

    # Escoge y marca habitación de destino
    rowDes = random.randint(0, size-1)
    colDes = random.randint(0, size-1)
    xentrada, yentrada =  rowDes*2+1, colDes*2+1
    matriz[xentrada][yentrada] = -2 

    solucion = [matriz, [xsalida,ysalida], [xentrada, yentrada]]
    return solucion

# Funcion que dibuja la matriz con su punto de inicio, punto de fin y el laberinto
# toma como argumentos, la matriz, el punto de inicio, el punto de fin y el tamano de la matriz
def dibujamela(matriz,puntoInicio, puntoFin, tamano):
    tamano = tamano*2 +1
    paredesX, paredesY = [],[]
    puertasX, puertasY = [],[]
    x, y = 0,0
    for i in range(tamano):
        for j in range(tamano):
            if matriz[i][j] == 10: 
                paredesX.append(i/(tamano))
                paredesY.append(j/(tamano))
                x+=1
            else:  #if matriz[i][j] == 0: 
                puertasX.append(i/(tamano))
                puertasY.append(j/(tamano))
                y+=1
    plot(paredesX, paredesY, 'sk')
    plot(puertasX, puertasY, 'sy')
    plot(puntoInicio[0]/(tamano), puntoInicio[1]/(tamano), 'sc')
    plot(puntoFin[0]/(tamano), puntoFin[1]/(tamano), 'sr')
    show()

# Funcion de devuelve los puntos que puede tomar el camino a seguir, es decir que no son puertas
# Recibe como argumentos, la matriz y el punto inicial
def puntosAdyacentes(matriz, puntoInicial):
    posicionX = puntoInicial[0]
    posicionY = puntoInicial[1]
    puntosIntermedios = []
    for i in range(2):
        if matriz[posicionX - 1][posicionY - 1 + i] < 10:
            puntosIntermedios.append([posicionX-1, posicionY - 1 + i])
        if matriz[posicionX + 1][posicionY - 1 + i] < 10:
            puntosIntermedios.append([posicionX-1, posicionY - 1 + i])
        if i != 1 and matriz[posicionX][posicionY - 1 + i] < 10:
            puntosIntermedios.append([posicionX, posicionY - 1 + i])
    return puntosIntermedios

# Funcion que devuelve las coordenadas correctas sobre la matriz grande, tomando 
# como entrada un punto de la matriz de habitaciones (10,10)
def puntoReal(punto):
    nuevasCoordeanas = [(punto[0]*2) + 1, (punto[1]*2) + 1]
    return nuevasCoordeanas
# Funcion que devuelve los pesos acumulados
# Recibe como parametros el peso de la matriz, y el peso acumulado
def calculaPeso(peso, pesoAcumulado):
    if peso == 10 : 
        return 1000000
    else:
        return (pesoAcumulado + peso)

def djikstra(matriz, puntoInicial, puntoFinal):
    # Cola = almacena el costo de ir a cada una de las puertas (peso acumulado)
    cola = np.full((10,10), 1000000)
    posicionInicial = [(int)(puntoInicial[0]-1)/2 , (int)(puntoInicial[1]-1)/2]
    valorX, valorY = (int)(posicionInicial[0]), (int)(posicionInicial[1])
    print(valorX, valorY, "estos son los putos")
    cola[valorX][valorY] = 0
    
    # En el punto inicial el coste es 0
    condicion = False
    while condicion == False:
        #Encontrar adyacentes de los que miramos y ver sus costes
        #Almacenar sus costes y seguir con el que menor coste tenga
        #Condicion para parar de buscar caminos es si uno es mayor que otro, es decir que si el coste hasta el punto A es de 20 y otro camnio que esta al lado del punto es de 70, seguimos con el A
        #[x*2+1][y*2+1]
        # Sitios que tengo que mirar , variaciones de X++,X-- pero con la misma Y y al reves
        punto1, punto2, punto3, punto4 = [valorX - 1, valorY], [valorX + 1, valorY], [valorX, valorY - 1], [valorX, valorY + 1]
        
        # Variantes de X
        punto1Grande = puntoReal(punto1)
        peso = matriz[punto1Grande[0] - 1][punto1Grande[1]]
        cola[punto1[0], punto1[1]] = calculaPeso(peso, cola[valorX][valorY])
        
        punto2Grande = puntoReal(punto2)
        peso = matriz[punto2Grande[0] + 1][punto2Grande[1]]
        cola[punto2[0], punto2[1]] = calculaPeso(peso, cola[valorX][valorY])

        # Variantes de Y
        punto3Grande = puntoReal(punto3)
        peso = matriz[punto3Grande[0]][punto3Grande[1] - 1]
        cola[punto3[0], punto3[1]] = calculaPeso(peso, cola[valorX][valorY])
        
        punto4Grande = puntoReal(punto4)
        peso = matriz[punto4Grande[0]][punto4Grande[1] + 1]
        cola[punto4[0], punto4[1]] = calculaPeso(peso, cola[valorX][valorY])

        lista = [cola[punto1[0], punto1[1]], cola[punto2[0], punto2[1]], cola[punto3[0], punto3[1]], cola[punto4[0], punto4[1]], 1]
        var1, var0 = 0, 0
        minimo = 100000
        for i in range(len(cola)):
            for j in range(len(cola[i])):
                if minimo > cola[i][j] and cola[i][j] >= cola[valorX][valorY]:
                    if i != valorX or j != valorY:
                        minimo = cola[i][j]
                        var1, var0 = i, j
                    else: pass
                else: pass
        valorX, valorY = var1, var0
        if puntoReal([valorX, valorY]) == puntoFinal:
            condicion = True
        else: pass
'''
            if i = valorX : 
                for j in range(len(i)):
                    if j != valorY:
                        if minimo > lista[i][j]:
                            minimo = lista[i][j]
                            var1, var2 = i, j
                        else: pass
                    else: pass
            else: 
                minAux = np.min(cola[i])
                if minimo > minAux:
                    minimo = minAux
                    var1, var2 = i, j
                else: pass


            print(np.min(cola[i]))

        print(lista, lista.index(min(lista)), np.min(cola))
        condicion = True
    '''
    return 0




#main
solucion = []
size = 10
ratio = 1
# solucion = [matriz de valores],[punto de inicio], [punto de fin]
solucion = generaLaberinto(size,ratio,131)
matriz = solucion[0]
puntoInicial = solucion[1]
puntoFinal = solucion[2]
posiblesCaminos = []
#posiblesCaminos = djikstra(matriz, puntoInicial, puntoFinal)

djikstra(matriz, puntoInicial, puntoFinal)
dibujamela(solucion[0],solucion[1], solucion[2], size)

