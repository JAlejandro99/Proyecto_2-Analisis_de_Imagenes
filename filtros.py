import numpy as np
from matplotlib import pyplot as plt
import cv2 as cv
import copy
import math

def atan_imgs(img1,img2):
    ret = copy.copy(img1)
    #Dimensiones de la imagen
    filas = ret.shape[1]
    columnas = ret.shape[0]
    for i in range(columnas):
        #Recorre filas
        for j in range(filas):
            ret[i,j] = int(math.degrees(math.atan2(img2[i,j],img1[i,j])))
    
    #Muestra los resultados
    cv.imshow('Arcotangente de imagenes', ret)
    cv.waitKey()

    return ret

def suma_imgs(img1,img2):
    ret = copy.copy(img1)
    #Dimensiones de la imagen
    filas = ret.shape[1]
    columnas = ret.shape[0]
    for i in range(columnas):
        #Recorre filas
        for j in range(filas):
            r = img1[i,j]+img2[i,j]
            #Normalización
            if(r > 255):
                r = 255
            if(r < 0):
                r = 0
            ret[i][j] = r
    
    #Muestra los resultados
    cv.imshow('Suma de imagenes', ret)
    cv.waitKey()

    return ret

#Algoritmo general de convolución
#Recibe como parámetro el kernel y la imagen a la que se aplica la convolución
#Regresa una matriz que es la imagen resultado de la convolución
def convolucion(kernel, imagen):
    
    #Verifica dimensiones del kernel
    tam_kernel = len(kernel)
    if(tam_kernel % 2 == 0 | len(kernel) < 3):
        #Si el tamaño es impar o es menor a 3 regresa
        print("Las dimensiones del kernel no son correctas")
        return
    
    #Verifica si la imagen tiene 3 canales RGB
    if(len(imagen.shape)==3):
        #Si los tiene la convierte a escala de grises con un solo canal
        nueva_img=cv.cvtColor(imagen, cv.COLOR_BGR2GRAY)
    else:    
        #En caso de que la imagen original es de un canal se crea una copia
        nueva_img = copy.copy(imagen)
        
    #Matriz para guardar resultados de convolución
    img_conv = copy.copy(nueva_img)
    
    #Dimensiones de la imagen
    filas = nueva_img.shape[1]
    columnas = nueva_img.shape[0]
    #Origen del kernel
    origenk = tam_kernel//2
    
    #Recorre columnas
    for i in range(origenk, columnas - origenk):
        #Recorre filas
        for j in range(origenk, filas - origenk):
            r = 0
            #Crea una ventana de la imagen del tamaño del kernel
            ventana = nueva_img[i-1:i+2,j-1:j+2]
            #Multiplica las matrices
            aux = ventana*kernel
            #Suma de valores
            for l in aux :
                r += sum(l)
            #Normalización
            if(r > 255):
                r = 255
            if(r < 0):
                r = 0
            #Asigna el valor a la nueva imagen
            img_conv[i][j] = r
           
    #Muestra los resultados
    cv.imshow('Original', nueva_img)
    cv.waitKey()
    cv.imshow('Convolucion', img_conv)
    cv.waitKey()
    
    return img_conv

def fgaussiano(img,tipo):
    if tipo==3:
        ret = convolucion([[1/16,2/16,1/16],[2/16,4/16,2/16],[1/16,2/16,1/16]], img)
    else:
        ret = convolucion([[1/246,4/246,6/246,4/246,1/246],[4/246,16/246,24/246,16/246,4/246],[6/246,24/246,36/246,24/246,6/246],[4/246,16/246,24/246,16/246,4/246],[1/246,4/246,6/246,4/246,1/246]], img)
    return ret

def froberts(img):
    gx = convolucion([[0,0,-1],[0,1,0],[0,0,0]], img)
    gy = convolucion([[-1,0,0],[0,1,0],[0,0,0]], img)
    f = suma_imgs(gx,gy)
    return gx,gy,f

def fprewitt(img):
    gx = convolucion([[1/3,0,-1/3],[1/3,0,-1/3],[1/3,0,-1/3]], img)
    gy = convolucion([[-1/3,-1/3,-1/3],[0,0,0],[1/3,1/3,1/3]], img)
    f = suma_imgs(gx,gy)
    return gx,gy,f

def fsobel(img):
    gx = convolucion([[1/4,0,-1/4],[2/4,0,-2/4],[1/4,0,-1/4]], img)
    gy = convolucion([[-1/4,-2/4,-1/4],[0,0,0],[1/4,2/4,1/4]], img)
    f = suma_imgs(gx,gy)
    return gx,gy,f