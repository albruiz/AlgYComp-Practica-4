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
    contador2 = 0
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            if matriz[i][j] == 10: 
                paredesX.append((20 - i)/(tamano))
                paredesY.append((j)/(tamano))
                x+=1
                contador2 += 1
            else:  #if matriz[i][j] == 0: 
                puertasX.append((20 -i)/(tamano))
                puertasY.append((j)/(tamano))
                y+=1
    
    plot(paredesY, paredesX, 'sk')
    plot(puertasY, puertasX, 'sy')


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
    comprobacion = np.full((10,10), False)
    cola = np.full((10,10), None)
    posicionInicial = [(int)(puntoInicial[0]-1)/2 , (int)(puntoInicial[1]-1)/2]
    valorX, valorY = (int)(posicionInicial[0]), (int)(posicionInicial[1])
    cola[valorX][valorY] = 0
    contador = 0
    # En el punto inicial el coste es 0
    condicion = False
    while condicion == False:
        #Encontrar adyacentes de los que miramos y ver sus costes
        #Almacenar sus costes y seguir con el que menor coste tenga
        #Condicion para parar de buscar caminos es si uno es mayor que otro, es decir que si el coste hasta el punto A es de 20 y otro camnio que esta al lado del punto es de 70, seguimos con el A
        #[x*2+1][y*2+1]
        # Sitios que tengo que mirar , variaciones de X++,X-- pero con la misma Y y al reves
        punto1, punto2, punto3, punto4 = [valorX - 1, valorY], [valorX + 1, valorY], [valorX, valorY - 1], [valorX, valorY + 1]
        comprobacion[valorX, valorY] = True
        contador += 1
        # Variantes de X
        if punto1[0] <= 9 and punto1[1] <= 9 and punto1[0] >= 0 and punto1[1] >= 0:
            punto1Grande = puntoReal(punto1)
            peso = matriz[punto1Grande[0] + 1][punto1Grande[1]]
            #condicion para que se almacene el nuevo peso, significara que la unica vez que se almacena es que es menor que el  que estaba en la matriz
            if comprobacion[punto1[0], punto1[1]] == False:
                if cola[punto1[0], punto1[1]] != None:
                    if calculaPeso(peso, cola[valorX][valorY]) < cola[punto1[0], punto1[1]]:
                        cola[punto1[0], punto1[1]] = calculaPeso(peso, cola[valorX][valorY])
                    else: pass
                else: cola[punto1[0], punto1[1]] = calculaPeso(peso, cola[valorX][valorY])
                if cola[punto1[0], punto1[1]] < 10000:
                    plot((punto1Grande[1]/len(matriz)), (len(matriz) - 1 - punto1Grande[0])/len(matriz), 'sb')
            else: pass
        else: pass
            
        
        if punto2[0] <= 9 and punto2[1] <= 9 and punto2[0] >= 0 and punto2[1] >= 0:
            punto2Grande = puntoReal(punto2)
            peso = matriz[punto2Grande[0] - 1][punto2Grande[1]]
            if comprobacion[punto2[0], punto2[1]] == False:
                if cola[punto2[0],punto2[1]] != None: 
                    if calculaPeso(peso, cola[valorX][valorY]) < cola[punto2[0], punto2[1]]:
                        cola[punto2[0], punto2[1]] = calculaPeso(peso, cola[valorX][valorY])
                    else: pass 
                else: cola[punto2[0], punto2[1]] = calculaPeso(peso, cola[valorX][valorY])
                if cola[punto2[0], punto2[1]] < 10000:
                    plot((punto2Grande[1])/len(matriz),( len(matriz) - 1 - punto2Grande[0])/len(matriz), 'sb')
            else: pass
        else: pass

        # Variantes de Y
        if punto3[0] <= 9 and punto3[1] <= 9 and punto3[0] >= 0 and punto3[1] >= 0:
            punto3Grande = puntoReal(punto3)
            peso = matriz[punto3Grande[0]][punto3Grande[1] + 1]
            if comprobacion[punto3[0], punto3[1]] == False:
                if cola[punto3[0], punto3[1]] != None:
                    if calculaPeso(peso, cola[valorX][valorY]) < cola[punto3[0], punto3[1]]:
                        cola[punto3[0], punto3[1]] = calculaPeso(peso, cola[valorX][valorY])
                    else: pass
                else: cola[punto3[0], punto3[1]] = calculaPeso(peso, cola[valorX][valorY])
                if cola[punto3[0], punto3[1]] < 10000:
                    plot((punto3Grande[1])/len(matriz), (len(matriz) - 1 - punto3Grande[0])/len(matriz), 'sb') 
            else: pass
        else: pass

        if punto4[0] <= 9 and punto4[1] <= 9 and punto4[0] >= 0 and punto4[1] >= 0:
            punto4Grande = puntoReal(punto4)
            peso = matriz[punto4Grande[0]][punto4Grande[1] - 1]
            if comprobacion[punto4[0], punto4[1]] == False:
                if cola[punto4[0], punto4[1]] != None:
                    if calculaPeso(peso, cola[valorX][valorY]) < cola[punto4[0], punto4[1]]:
                        cola[punto4[0], punto4[1]] = calculaPeso(peso, cola[valorX][valorY])
                    else: pass
                else: cola[punto4[0], punto4[1]] = calculaPeso(peso, cola[valorX][valorY])
                if cola[punto4[0], punto4[1]] < 10000:
                    plot((punto4Grande[1])/len(matriz), (len(matriz) -1 - punto4Grande[0])/len(matriz), 'sb')     
            else: pass
        else: pass

        var1, var0 = 0, 0
        minimo = 100000
        for i in range(len(cola)):
            for j in range(len(cola[i])):
                if cola[i][j] != None:
                    if minimo > cola[i][j] and cola[i][j] >= cola[valorX][valorY]:
                        if i != valorX or j != valorY:
                            minimo = cola[i][j]
                            var1, var0 = i, j
                        else: pass
                    else: pass
                else: pass
        cola[valorX, valorY] = None
        valorX, valorY = var1, var0
                
        if puntoReal([valorX, valorY]) == puntoFinal:
            condicion = True
        else: 
            a = puntoReal([valorX, valorY])
            plot((a[1] )/len(matriz),(len(matriz) -1 - a[0])/len(matriz), 'sb')
    return 0




#main
solucion = []
size = 10
ratio = 1
# solucion = [matriz de valores],[punto de inicio], [punto de fin]
solucion = generaLaberinto(size,ratio,123)
matriz = solucion[0]
puntoInicial = solucion[1]
puntoFinal = solucion[2]
posiblesCaminos = []
#posiblesCaminos = djikstra(matriz, puntoInicial, puntoFinal)
contador = 0
for i in matriz:
    for j in i: 
        if j == 10: contador += 1
        else: pass

dibujamela(solucion[0],solucion[1], solucion[2], size)
djikstra(matriz, puntoInicial, puntoFinal)
plot((puntoInicial[1])/(size*2+1), (20 - puntoInicial[0])/(size*2+1),  'sc')
plot(puntoFinal[1]/(size*2+1), (20 - puntoFinal[0])/(size*2+1), 'sr')
show()


