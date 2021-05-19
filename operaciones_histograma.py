import numpy as np
from matplotlib import pyplot as plt
import cv2 as cv
import copy
import math

#Histograma de imagen original
def h_original(im):
    
    #Verifica si la imagen tiene 3 canales RGB
    if(len(im.shape)==3):
        #Si los tiene la convierte a escala de grises con un solo canal
        im2=cv.cvtColor(im, cv.COLOR_BGR2GRAY)
    else:
        #En caso de que la imagen original es de un canal se crea una copia
        im2 = copy.copy(im)
    
    hist=cv.calcHist([im2], [0], None, [256], [0, 256])
    plt.plot(hist, color='gray' )
    plt.title("Histograma Original")
    plt.xlabel('Intensidad de iluminacion')
    plt.ylabel('Cantidad de pixeles')
    plt.show()
    
    #cv.imshow('Original', im)
    #cv.waitKey()
    
    return hist
    
# Función que muestra histogramas de los canales RGB
# Recibe como parámetro una imagen
def histogramas_RGB(img):
    
    #Si la imagen tiene solo un canal (está en escala de grises) mostrará error
    if(len(img.shape)==2):
        return -1
    
    # Lista con los 3 histogramas
    histogramas = []
    # Histograma canal azul
    histogramas.append(cv.calcHist([img], [0], None, [256], [0, 256]))
    # Histograma canal Verde
    histogramas.append(cv.calcHist([img], [1], None, [256], [0, 256]))
    #Histograma canal Azul
    histogramas.append(cv.calcHist([img], [2], None, [256], [0, 256]))
    
    # Imprime los histogramas
    colores = ["blue", "green", "red"]
    for i in range (0,3):
        plt.plot(histogramas[i], color=colores[i] )
    plt.title("Histogramas Canales RGB")
    plt.xlabel('Intensidad de iluminacion')
    plt.ylabel('Cantidad de pixeles')
    plt.show()

def desplazamiento_d(im2,a):
    #DESPLAZAMIENTO HACIA LA DERECHA
    im = copy.copy(im2)
    i=0
    while i<im.shape[0]:
        j=0
        while j<im.shape[1]:
            b,g,r=im[i,j]
            v0=int(b)+a
            v1=int(g)+a
            v2=int(r)+a
            if v0>255:
                v0=255
            if v1>255:
                v1=255
            if v2>255:
                v2=255
            im[i,j]=v0,v1,v2
            j+=1
        i+=1
    
    hist= cv.calcHist([im], [0], None, [256], [0, 256])
    plt.plot(hist, color='gray' )
    plt.title("Histograma Desplazamiento Derecha")
    plt.xlabel('Intensidad de iluminacion')
    plt.ylabel('Cantidad de pixeles')
    plt.show()
    #cv.imshow('DesDerecha', im)
    #cv.waitKey()
    return im

def desplazamiento_i(im2,a):
    #DESPLAZAMIENTO HACIA LA IZQUIERDA
    im = copy.copy(im2)
    i=0
    while i<im.shape[0]:
        j=0
        while j<im.shape[1]:
            b,g,r=im[i,j]
            v0=int(b)-a
            v1=int(g)-a
            v2=int(r)-a
            if v0<0:
                v0=0
            if v1<0:
                v1=0
            if v2<0:
                v2=0
            im[i,j]=v0,v1,v2
            j+=1
        i+=1
    
    hist= cv.calcHist([im], [0], None, [256], [0, 256])
    plt.plot(hist, color='gray' )
    plt.title("Histograma Desplazamiento Izquierda")
    plt.xlabel('Intensidad de iluminacion')
    plt.ylabel('Cantidad de pixeles')
    plt.show()
    #cv.imshow('DesIzquierda', im)
    #cv.waitKey()
    return im

def estiramiento(hist,im2):
    im = copy.copy(im2)
    frec=[]
    k=0
    for i in range(0,hist.shape[0]):
        for j in range(0,hist.shape[1]):
            if hist[i,j]>0:
                frec.insert(k,i)
                k+=1
    
    minimo=frec[0]
    maximo=frec[len(frec)-1]
    
    i=0
    while i<im.shape[0]:
        j=0
        while j<im.shape[1]:
            b,g,r=im[i,j]
            v0=(int(b)-minimo)*255/(maximo-minimo)
            v1=(int(g)-minimo)*255/(maximo-minimo)
            v2=(int(r)-minimo)*255/(maximo-minimo)
            im[i,j]=v0,v1,v2
            j+=1
        i+=1
    
    hist2= cv.calcHist([im], [0], None, [256], [0, 256])
    plt.plot(hist2, color='gray' )
    plt.title("Histograma Estiramiento")
    plt.xlabel('Intensidad de iluminacion')
    plt.ylabel('Cantidad de pixeles')
    plt.show()
    #cv.imshow('Estiramiento', im)
    #cv.waitKey()
    
    return im

#ECUALIZACIÓN
def ecualizacion(im2):
    
    """#Verifica si la imagen tiene 3 canales RGB
    if(len(im2.shape)==3):
        #Si los tiene la convierte a escala de grises con un solo canal
        im=cv.cvtColor(im2, cv.COLOR_BGR2GRAY)
    else: 
        #En caso de que la imagen original es de un canal se crea una copia
        im = copy.copy(im2)"""
    
    pixeles=[]
    im=copy.copy(im2)
    total=im.shape[0]*im.shape[1]
    frecuencia={}
    
    #Valor RGB de cada pixel de la imagen
    k=0
    i=0
    while i<im.shape[0]:
        j=0
        while j<im.shape[1]:
            b,g,r=im[i,j]
            pixeles.insert(k,(b+g+r))
            k+=1
            j+=1
        i+=1
    
    pixeles=sorted(pixeles)#Se ordenan los pixeles de menor a mayor
    minimo=min(pixeles)#Se obtiene el valor mínimo de los pixeles
    maximo=max(pixeles)#Se obtiene el valor máximo de los pixeles
    
    #Guarda en un diccionario la frecuencia de cada nivel RGB
    for pixel in pixeles:
        if pixel in frecuencia:
            frecuencia[pixel]+=1
        else:
            frecuencia[pixel]=1
    
    #Toma solo la frecuencia de cada nivel de RGB del diccionario         
    n_g=list(frecuencia.values())
    
    #Probabilidad de ocurrencia posterior del nivel de RGB
    pp_g=[]
    acum=0
    
    for i in range(len(n_g)):
        acum=acum+n_g[i]
        pp_g.insert(i,(acum/total))
    
    #Calculando la ecualización uniforme
    f_g=[]
    for i in range(len(pp_g)):
        f_g.insert(i,math.floor((maximo-minimo)*(pp_g[i]+minimo)))
    
    #Obtiene los valores de los pixeles RGB
    pix=list(frecuencia.keys())
    
    i=0
    while i<im.shape[0]:
        j=0
        while j<im.shape[1]:
            b,g,r=im[i,j]
            if b+g+r in pix:
                v=pix.index(b+g+r)
                im[i,j]=f_g[v]
            j+=1
        i+=1

    hist4=cv.calcHist([im], [0], None, [256], [0, 256])
    plt.plot(hist4, color='gray' )
    plt.title("Histograma Ecualización")
    plt.xlabel('Intensidad de iluminacion')
    plt.ylabel('Cantidad de pixeles')
    plt.show()
    #cv.imshow('Ecualización', im)
    #cv.waitKey()
    return im
    
# Función que realiza estrechamiento del histograma
# Recibe como parámetros la imagen y los valores deseados de compresión
# Devuelve una nueva imagen (matriz numpy) con los cambios realizados
def estrechamiento(img, Cmin, Cmax):
    
    #Verifica si la imagen tiene 3 canales RGB
    if(len(img.shape)==3):
        #Si los tiene la convierte a escala de grises con un solo canal
        nueva_img=cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    else:    
        #En caso de que la imagen original es de un canal se crea una copia
        nueva_img = copy.copy(img)
    
    # Valores de la formula
    rmin = np.amin(img)
    rmax = np.amax(img)

    # Cambio de valores a la imagen de acuerdo a la fórmula
    for i in range(0, nueva_img.shape[0]):
        for j in range(0, nueva_img.shape[1]):
            nueva_img[i,j] = round(((Cmax-Cmin)/(rmax-rmin))*nueva_img[i,j] + Cmin)
    
    # Calcula el histograma con estrechamiento
    nhistograma = cv.calcHist([nueva_img], [0], None, [256], [0, 256])
    # Muestra el histograma
    plt.plot(nhistograma, color='gray' )
    plt.title("Histograma Estrechamiento")
    plt.xlabel('Intensidad de iluminacion')
    plt.ylabel('Cantidad de pixeles')
    plt.show()
    
    # Muestra los cambios realizados en la imagen
    #cv.imshow('Estrechamiento', nueva_img)
    #cv.waitKey()
    
    return nueva_img

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

    print(nueva_img.shape)    
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

def principal():
    im=cv.imread("Imagen1.png")
    im2=cv.imread("Imagen1.png")
    hist=cv.calcHist([im2], [0], None, [256], [0, 256])
    a=50
    
    #Histograma de la imagen original
    hist=h_original(im)
    #Histogramas RGB
    histogramas_RGB(copy.copy(im2))
    #Histograma desplazado a la derecha
    desplazamiento_d(im,a)
    #Histograma desplazado a la izquierda
    desplazamiento_i(im2,a)
    #Estiramiento del histograma
    estiramiento(hist,im2)
    #Histograma de la imagen ecualizada
    ecualizacion(im)
    # Estrechamiento de Histograma
    estrechamiento(copy.copy(im2), 50, 150)
    