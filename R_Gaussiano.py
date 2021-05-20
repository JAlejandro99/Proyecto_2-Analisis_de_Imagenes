import numpy as np
from matplotlib import pyplot as plt
import cv2 as cv
import copy


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