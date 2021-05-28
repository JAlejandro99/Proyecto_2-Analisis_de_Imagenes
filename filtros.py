import numpy as np
from matplotlib import pyplot as plt
import cv2 as cv
import copy
import math

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
            ventana = nueva_img[i-origenk:i+origenk+1,j-origenk:j+origenk+1]
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

def binarizar(img,umbral):
    #Verifica si la imagen tiene 3 canales RGB
    if(len(img.shape)==3):
        #Si los tiene la convierte a escala de grises con un solo canal
        ret = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    else:    
        #En caso de que la imagen original es de un canal se crea una copia
        ret = copy.copy(img)
    
    #Dimensiones de la imagen
    filas = ret.shape[1]
    columnas = ret.shape[0]
    
    #Recorre columnas
    for i in range(columnas):
        #Recorre filas
        for j in range(filas):
            if(ret[i,j] > umbral):
                ret[i,j] = 255
            else:
                ret[i,j] = 0
           
    #Muestra los resultados
    cv.imshow('Binarización', ret)
    cv.waitKey()
    
    return ret

def rgaussiano(im,media,varianza):
    
    #Verifica si la imagen tiene 3 canales RGB
    if(len(im.shape)==3):
        #Si los tiene la convierte a escala de grises con un solo canal
        im2=cv.cvtColor(im, cv.COLOR_BGR2GRAY)
    else:
        #En caso de que la imagen original es de un canal se crea una copia
        im2 = copy.copy(im)
    
    im2= np.array(im2/255, dtype=float)
    ruido=np.random.normal(media, varianza ** 0.5, im2.shape)
    agregar=im2+ruido
    if agregar.min() < 0:
        low_clip = -1
    else:
        low_clip = 0
    agregar=np.clip(agregar, low_clip, 1.0)
    agregar=np.uint8(agregar*255)

    return agregar

def fgaussiano(img,tipo):
    if tipo==3:
        ret = convolucion(np.array([[1,2,1],[2,4,2],[1,2,1]])*(1/16), img)
    else:
        ret = convolucion(np.array([[1,4,6,4,1],[4,16,24,16,4],[6,24,36,24,6],[4,16,24,16,4],[1,4,6,4,1]])*(1/246), img)
    return ret

def froberts(img):
    gx = convolucion([[0,0,-1],[0,1,0],[0,0,0]], img)
    gy = convolucion([[-1,0,0],[0,1,0],[0,0,0]], img)
    #g3 = convolucion([[0,0,0],[0,1,0],[0,0,-1]], img)
    #g4 = convolucion([[0,0,0],[0,1,0],[-1,0,0]], img)
    f = suma_imgs(gx,gy)
    #f = suma_imgs(f,g3)
    #f = suma_imgs(f,g4)
    return gx,gy,f

def fprewitt(img):
    gx = convolucion(np.array([[1,0,-1],[1,0,-1],[1,0,-1]])*(1/3), img)
    gy = convolucion(np.array([[-1,-1,-1],[0,0,0],[1,1,1]])*(1/3), img)
    f = suma_imgs(gx,gy)
    return gx,gy,f

def fsobel(img):
    gx = convolucion(np.array([[1,0,-1],[2,0,-2],[1,0,-1]])*(1/4), img)
    gy = convolucion(np.array([[-1,-2,-1],[0,0,0],[1,2,1]])*(1/4), img)
    f = suma_imgs(gx,gy)
    return gx,gy,f

#Función que implementa el filtro máximo
#Recibe como parámetro una imagen y el tamaño de la ventana
#Regresa la imagen resultante de aplicar el filtro máxmo
def fmax(img,tam_ventana):
    
    #Verifica si la imagen tiene 3 canales RGB
    if(len(img.shape)==3):
        #Si los tiene la convierte a escala de grises con un solo canal
        nueva_img=cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    else:    
        #En caso de que la imagen original es de un canal se crea una copia
        nueva_img = copy.copy(img)
        
    #Matriz para guardar resultados de aplicar el filtro
    img_max = copy.copy(nueva_img)
      
    #Dimensiones de la imagen
    filas = nueva_img.shape[1]
    columnas = nueva_img.shape[0]
    #Origen de la ventana
    origenv = tam_ventana//2
    
    #Recorre columnas
    for i in range(origenv, columnas - origenv):
        #Recorre filas
        for j in range(origenv, filas - origenv):
            #Crea una ventana de la imagen con el tamaño del parametro
            ventana = nueva_img[i-origenv:i+origenv+1,j-origenv:j+origenv+1]
            #Encuentra el máximo y sustituye en la nueva imagen
            maximo = 0
            for m in ventana:
                for n in m:
                    if int(n) > maximo: maximo = int(n)
            img_max[i][j] = maximo
           
    #Muestra los resultados
    cv.imshow('Original', nueva_img)
    cv.waitKey()
    cv.imshow('Filtro maximo', img_max)
    cv.waitKey()

    return img_max
  
#Función que implementa el filtro minimo
#Recibe como parámetro una imagen y el tamaño de la ventana
#Regresa la imagen resultante de aplicar el filtro minimo
def fmin(img,tam_ventana):
    
    #Verifica si la imagen tiene 3 canales RGB
    if(len(img.shape)==3):
        #Si los tiene la convierte a escala de grises con un solo canal
        nueva_img=cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    else:    
        #En caso de que la imagen original es de un canal se crea una copia
        nueva_img = copy.copy(img)
        
    #Matriz para guardar resultados de aplicar el filtro
    img_min = copy.copy(nueva_img)
      
    #Dimensiones de la imagen
    filas = nueva_img.shape[1]
    columnas = nueva_img.shape[0]
    #Origen de la ventana
    origenv = tam_ventana//2
    
    #Recorre columnas
    for i in range(origenv, columnas - origenv):
        #Recorre filas
        for j in range(origenv, filas - origenv):
            #Crea una ventana de la imagen con el tamaño del parametro
            ventana = nueva_img[i-origenv:i+origenv+1,j-origenv:j+origenv+1]
            #Encuentra el minimo y sustituye en la nueva imagen
            minimo = 255
            for m in ventana:
                for n in m:
                    if int(n) < minimo: minimo = int(n)
            img_min[i][j] = minimo
           
    #Muestra los resultados
    cv.imshow('Original', nueva_img)
    cv.waitKey()
    cv.imshow('Filtro minimo', img_min)
    cv.waitKey()
    
    return img_min

def principal():
    
    im=cv.imread("manzana.jpg",0)
    
    #Imagen Original
    cv.imshow('Imagen original', im)
    hist=cv.calcHist([im], [0], None, [256], [0, 256])
    plt.plot(hist, color='gray' )
    plt.title("Histograma Original")
    plt.xlabel('Intensidad de iluminacion')
    plt.ylabel('Cantidad de pixeles')
    plt.show()
    
    #Imagen con Ruido Gaussiano
    im_ruido=rgaussiano(im, 0, 0.001)#Los parámetros pueden ser introducidos por el usuario
    cv.imshow('Imagen con ruido', im_ruido)
    hist2=cv.calcHist([im_ruido], [0], None, [256], [0, 256])
    plt.plot(hist2, color='gray' )
    plt.title("Histograma con ruido Gaussiano")
    plt.xlabel('Intensidad de iluminacion')
    plt.ylabel('Cantidad de pixeles')
    plt.show()
    cv.waitKey(0)

#principal()
#kernel
"""im=cv.imread("Imagen1.png")
kernel = np.array([[1,2,1],[2,4,2],[1,2,1]])*(1/9)
convolucion(kernel,im)

im=cv.imread("Casa.jpg")
fgaussiano(im,3)
fgaussiano(im,5)
froberts(im)
fprewitt(im)
fsobel(im)
"""

"""prueba = cv.imread("prueba_maxmin.png")
fmax(prueba,3)
fmin(prueba,3)"""