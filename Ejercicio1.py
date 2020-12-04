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
    plot(paredesX, paredesY, 'sm')
    plot(puertasX, puertasY, 'sy')
    plot(puntoInicio[0]/(tamano), puntoInicio[1]/(tamano), 'sc')
    plot(puntoFin[0]/(tamano), puntoFin[1]/(tamano), 'sr')
    show()

#main
solucion = []
size = 10
ratio = 1
solucion = generaLaberinto(size,ratio,131)
dibujamela(solucion[0],solucion[1], solucion[2], size)

