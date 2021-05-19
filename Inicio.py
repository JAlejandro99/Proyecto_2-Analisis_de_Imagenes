from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image,ImageTk
from numpy import *
from operaciones_histograma import *
from filtros import *
import cv2 as cv

def drag_start(event):
    global img_sel,seleccion_anterior
    widget = event.widget
    widget.startX = event.x
    widget.startY = event.y
    if seleccion_anterior!=-1:
        imagenesLabel[seleccion_anterior].config(bd=0)
    img_sel = imagenesLabel.index(widget)
    #print(img_sel)
    imagenesLabel[img_sel].config(bd=10,relief="groove")
    seleccion_anterior = img_sel

def drag_motion(event):
    widget = event.widget
    x = widget.winfo_x() - widget.startX + event.x
    y = widget.winfo_y() - widget.startY + event.y
    widget.place(x=x,y=y)

def button_hover(e):
    widget = e.widget
    if widget==b1:
        status_label.config(text="Ver histograma")
    elif widget==b2:
        status_label.config(text="Ver histograma RGB")
    elif widget==b3:
        status_label.config(text="Desplazar histograma a la izquierda")
    elif widget==b4:
        status_label.config(text="Desplazar histograma a la derecha")
    elif widget==b5:
        status_label.config(text="Estiramiento del histograma")
    elif widget==b6:
        status_label.config(text="Histograma de la imagen ecualizada")
    elif widget==b7:
        status_label.config(text="Estrechamiento del histograma")
    elif widget==b8:
        status_label.config(text="Eliminar imagen")
    elif widget==b9:
        status_label.config(text="Ruido Gaussiano")
    elif widget==b10:
        status_label.config(text="Filtro Gaussiano")
    elif widget==b11:
        status_label.config(text="Filtro Roberts")
    elif widget==b12:
        status_label.config(text="Filtro Prewitt")
    elif widget==b13:
        status_label.config(text="Filtro Sobel")
    elif widget==b14:
        status_label.config(text="Filtro Máximo")
    elif widget==b15:
        status_label.config(text="Filtro Mínimo")

def button_hover_leave(e):
    status_label.config(text="")

#Ventana para elgir un valor de desplazamiento
def eligeDesp(desplazamiento):
    
    def guardaDato():
        a = -1

        try:
            a = int(my_spin.get())
            
            #Comprueba el valor del dato ingresado
            if(a>=0 and a<=255):
               despWindow.destroy()
               if(desplazamiento == False):
                   #Desplazamiento a la izquierda
                   img = desplazamiento_i(im[img_sel],a)
                   agregar_img(img)
               else:
                    #Desplazamiento a la derecha
                    img = desplazamiento_d(im[img_sel],a)
                    agregar_img(img)
                   
            else:
                messagebox.showerror(message="El valor debe ser un entero entre 0 y 255", 
                             title="Valor fuera de rango")
            
        except:
            messagebox.showerror(message="No se aceptan caracteres, solo números", 
                             title="Tipo de dato incorrecto")

    #Ubica la ventana en el centro
    ancho_v = 200
    alto_v = 150

    x_v = root.winfo_screenwidth() // 2 - ancho_v // 2
    y_v = root.winfo_screenheight() // 2 - alto_v // 2

    pos = str(ancho_v) + "x" + str(alto_v) + "+" + str(x_v) + "+" + str(y_v)
    despWindow = Toplevel(root)
    despWindow.title("Desplazamiento")
    despWindow.geometry(pos)
    despWindow.resizable(ancho_v, alto_v)
    
    lblspin = Label(despWindow, text="Elige un valor de desplazamiento")
    lblspin.pack(pady=10)
    
    #Spinbox para elegir un valor
    my_spin = Spinbox(despWindow, from_=0, to=255,)
    my_spin.pack(pady=10)
    
    #Boton para enviar
    my_button = Button(despWindow, 
                       text="Aceptar", 
                       command= guardaDato)
    my_button.pack(pady=20)

#Ventana para elegir valores de estrechamiento
def eligeEstr():
 
    def guardaDatos():
        Cmax = 0
        Cmin = 0

        try:
            Cmin = int(my_spin.get())
            Cmax = int(my_spin2.get())
            
            #Comprueba el valor de los datos ingresado
            if((Cmax>=0 and Cmax<=255) and (Cmin>=0 and Cmin<=255)):
                despWindow.destroy()
                img = estrechamiento(im[img_sel],Cmin, Cmax)
                agregar_img(img)
                                   
            else:
                messagebox.showerror(message="El valor debe ser un entero entre 0 y 255", 
                             title="Valor fuera de rango")
            
        except:
            messagebox.showerror(message="No se aceptan caracteres, solo números", 
                             title="Tipo de dato incorrecto")

    #Ubica la ventana en el centro
    ancho_v = 300
    alto_v = 200

    x_v = root.winfo_screenwidth() // 2 - ancho_v // 2
    y_v = root.winfo_screenheight() // 2 - alto_v // 2

    pos = str(ancho_v) + "x" + str(alto_v) + "+" + str(x_v) + "+" + str(y_v)
   
    despWindow = Toplevel(root)
    despWindow.title("Estrechamiento")
    despWindow.geometry(pos)
    
    lblspin = Label(despWindow, text="Elige los valores de compresión")
    lblspin.pack()
    
    lblspin2 = Label(despWindow, text="Cmin:")
    lblspin2.place(x=40, y=50)
    lblspin.pack(pady=10)
    
    #Spinbox para elegir el valor de Cmin
    my_spin = Spinbox(despWindow, from_=0, to=255,)
    my_spin.place(x=50, y=20)
    my_spin.pack(pady=10)
    
    lblspin2 = Label(despWindow, text="Cmax:")
    lblspin2.place(x=40, y=90)
    lblspin.pack()

    #Spinbox para elegir el valor de Cmax
    my_spin2 = Spinbox(despWindow, from_=0, to=255,)
    my_spin2.place(x=50, y=70)
    my_spin2.pack(pady=10)
    
    
    #Boton para enviar
    my_button = Button(despWindow, 
                       text="Aceptar", 
                       command= guardaDatos)
    my_button.pack(pady=20)

#Funcion con la que se pide una imagen al usuario
def addImg():
    global nomb_imagenes,im,imagenes,imagenesLabel,img_sel,seleccion_anterior
    #Pedir nombre del archivo
    nom_img = filedialog.askopenfilename(title="Seleccione archivo",filetypes=(("jpeg files",".jpg"),("png files",".png"),("all files",".*")))
    nomb_imagenes.append(nom_img)
    img = cv.imread(nom_img)
    h = img.shape[0]
    w = img.shape[1]
    im.append(img)
    img = cv.cvtColor(img,cv.COLOR_BGR2RGB)
    imagenes.append(ImageTk.PhotoImage(Image.fromarray(img)))
    img_sel = len(imagenes)-1
    imagenesLabel.append(Label(frame,image=imagenes[len(imagenes)-1],width=w,height=h,bg="gray"))
    imagenesLabel[img_sel].place(x=100,y=100)
    imagenesLabel[img_sel].bind("<Button-1>",drag_start)
    imagenesLabel[img_sel].bind("<B1-Motion>",drag_motion)
    imagenesLabel[img_sel].config(bd=10,relief="groove")
    if seleccion_anterior!=-1:
        imagenesLabel[seleccion_anterior].config(bd=0)
    seleccion_anterior = img_sel

def saveImg():
    global im,nomb_imagenes
    if nomb_imagenes[img_sel]=="nueva":
        nom_img = filedialog.asksaveasfilename(title="Nombre del archivo a guardar",filetypes=(("jpeg files",".jpg"),("png files",".png"),("all files",".*")))
        cv.imwrite(nom_img,im[img_sel])
        nomb_imagenes[img_sel] = nom_img

def agregar_img(img):
    global nomb_imagenes,im,imagenes,imagenesLabel,img_sel,seleccion_anterior
    #Pedir nombre del archivo
    nom_img = "nueva"
    nomb_imagenes.append(nom_img)
    h = img.shape[0]
    w = img.shape[1]
    im.append(img)
    img = cv.cvtColor(img,cv.COLOR_BGR2RGB)
    imagenes.append(ImageTk.PhotoImage(Image.fromarray(img)))
    img_sel = len(imagenes)-1
    imagenesLabel.append(Label(frame,image=imagenes[len(imagenes)-1],width=w,height=h,bg="gray"))
    imagenesLabel[img_sel].place(x=100,y=100)
    imagenesLabel[img_sel].bind("<Button-1>",drag_start)
    imagenesLabel[img_sel].bind("<B1-Motion>",drag_motion)
    imagenesLabel[img_sel].config(bd=10,relief="groove")
    if seleccion_anterior!=-1:
        imagenesLabel[seleccion_anterior].config(bd=0)
    seleccion_anterior = img_sel

def verHist():
    #Si no hay imagenes seleccionadas muestra advertencia
    if(len(im)==0):
        messagebox.showwarning(message="Debes seleccionar una imagen", 
                             title="Imagen no seleccionada")
        return
    #Histograma de la imagen original
    print(img_sel)
    hist = h_original(im[img_sel])
    
#Hacer que reciba imagenes en lugar de el nombre
def verHistRGB():
    #Si no hay imagenes seleccionadas muestra advertencia
    if(len(im)==0):
        messagebox.showwarning(message="Debes seleccionar una imagen", 
                             title="Imagen no seleccionada")
        return
    #Si la imagen recibida solo tiene un canal muestra mensaje de error
    if( histogramas_RGB(im[img_sel]) ):
        messagebox.showerror(message="La imagen debe tener los 3 canales RGB", 
                             title="Imagen en escala de grises")
        

def despIzqHist():
    #Si no hay imagenes seleccionadas muestra advertencia
    if(len(im)==0):
        messagebox.showwarning(message="Debes seleccionar una imagen", 
                             title="Imagen no seleccionada")
        return
    eligeDesp(False)
    
def despDerHist():
    #Si no hay imagenes seleccionadas muestra advertencia
    if(len(im)==0):
        messagebox.showwarning(message="Debes seleccionar una imagen", 
                             title="Imagen no seleccionada")
        return
    eligeDesp(True)

def estHist():
    #Si no hay imagenes seleccionadas muestra advertencia
    if(len(im)==0):
        messagebox.showwarning(message="Debes seleccionar una imagen", 
                             title="Imagen no seleccionada")
        return
    hist=cv.calcHist([im[img_sel]], [0], None, [256], [0, 256])
    img = estiramiento(hist,im[img_sel])
    agregar_img(img)

def histEcual():
    #Si no hay imagenes seleccionadas muestra advertencia
    if(len(im)==0):
        messagebox.showwarning(message="Debes seleccionar una imagen", 
                             title="Imagen no seleccionada")
        return
    img = ecualizacion(im[img_sel])
    agregar_img(img)

#Hacer que reciba imagenes en lugar de un nombre
def histEstr():
    #Si no hay imagenes seleccionadas
    if(len(im)==0):
        messagebox.showwarning(message="Debes seleccionar una imagen", 
                             title="Imagen no seleccionada")
        return
    eligeEstr()

def ruidoGaussiano():
    pass

def filtroGaussiano():
    #Si no hay imagenes seleccionadas muestra advertencia
    if(len(im)==0):
        messagebox.showwarning(message="Debes seleccionar una imagen", 
                             title="Imagen no seleccionada")
        return
    img = fgaussiano(im[img_sel],3) #Se debe de preguntar al usuario
    agregar_img(img)

def filtroRoberts():
    #Si no hay imagenes seleccionadas muestra advertencia
    if(len(im)==0):
        messagebox.showwarning(message="Debes seleccionar una imagen", 
                             title="Imagen no seleccionada")
        return
    img = froberts(im[img_sel])
    agregar_img(img[0])
    agregar_img(img[1])
    agregar_img(img[2])

def filtroPrewitt():
    #Si no hay imagenes seleccionadas muestra advertencia
    if(len(im)==0):
        messagebox.showwarning(message="Debes seleccionar una imagen", 
                             title="Imagen no seleccionada")
        return
    img = fprewitt(im[img_sel])
    agregar_img(img[0])
    agregar_img(img[1])
    agregar_img(img[2])

def filtroSobel():
    #Si no hay imagenes seleccionadas muestra advertencia
    if(len(im)==0):
        messagebox.showwarning(message="Debes seleccionar una imagen", 
                             title="Imagen no seleccionada")
        return
    img = fsobel(im[img_sel])
    agregar_img(img[0])
    agregar_img(img[1])
    agregar_img(img[2])

def filtroMaximo():
    pass

def filtroMinimo():
    pass

def eliminar_img():
    global imagenes,imagenesLabel,im,nomb_imagenes,seleccion_anterior,img_sel,frame
    imagenesLabel[img_sel].config(bd=0)
    #imagenesLabel[img_sel].place_forget() #Lo olvidamos
    #print("T0")
    #print(len(imagenes))
    #print(len(imagenesLabel))
    #print(len(im))
    #print(len(nomb_imagenes))
    imagenesLabel[img_sel].destroy() #Lo eliminamos de forma definitiva
    del imagenes[img_sel]
    del imagenesLabel[img_sel]
    del im[img_sel]
    del nomb_imagenes[img_sel]
    #print("T1")
    #print(len(imagenes))
    #print(len(imagenesLabel))
    #print(len(im))
    #print(len(nomb_imagenes))
    seleccion_anterior = -1
    img_sel = -1

def leer_imagen(nombre):
    img = cv.imread(nombre)
    alto, w, channel = img.shape
    nuevo_alto = 80
    escala = nuevo_alto/alto
    img = PhotoImage(file=nombre)
    if (escala-int(escala))!=0:
        img = img.zoom(int(escala*10))
        img = img.subsample(10)
    else:
        img = img.zoom(escala)
    return img

#Raíz
root=Tk()
root.title("Ventana de pruebas")

#Ubica la raiz en el centro de la pantalla

ancho_v = root.winfo_screenwidth() - 400
alto_v = root.winfo_screenheight() - 200
x_v = root.winfo_screenwidth() // 2 - ancho_v // 2
y_v = root.winfo_screenheight() // 2 - alto_v // 2

pos = str(ancho_v) + "x" + str(alto_v) + "+" + str(x_v) + "+" + str(y_v)
root.geometry(pos)
root.config(bd=20)

w=700
h=500
x=w/2
y=h/2
imagenes = list()
imagenesLabel = list()
im = list()
nomb_imagenes = list()
seleccion_anterior = -1
img_sel = -1

Grid.rowconfigure(root,3,weight=1)
Grid.columnconfigure(root,0,weight=1)
Grid.columnconfigure(root,1,weight=1)
Grid.columnconfigure(root,2,weight=1)
Grid.columnconfigure(root,3,weight=1)
Grid.columnconfigure(root,4,weight=1)
Grid.columnconfigure(root,5,weight=1)
Grid.columnconfigure(root,6,weight=1)
Grid.columnconfigure(root,7,weight=1)

bAddImg=Button(root,text="Abrir Imagen",command=lambda:addImg())
bAddImg.grid(row=0,column=0)

bSaveImg=Button(root,text="Guardar Imagen",command=lambda:saveImg())
bSaveImg.grid(row=0,column=1)

#Tenemos que descubrir qué imagen se seleccionó con anterioridad y la pasamos a la funcion ver histograma
img1 = leer_imagen("iconos/histograma2.png")
b1=Button(root,image=img1,width=80,command=lambda:verHist())
b1.grid(row=1,column=0)
b1.bind("<Enter>",button_hover)
b1.bind("<Leave>",button_hover_leave)

#Ver histograma RGB
img2 = leer_imagen("iconos/histograma.png")
b2=Button(root,image=img2,width=80,command=lambda:verHistRGB())
b2.grid(row=1,column=1)
b2.bind("<Enter>",button_hover)
b2.bind("<Leave>",button_hover_leave)

#Desplazamiento del histograma a la izquierda
img3 = leer_imagen("iconos/izquierda.png")
b3=Button(root,image=img3,width=80,command=lambda:despIzqHist())
b3.grid(row=1,column=2)
b3.bind("<Enter>",button_hover)
b3.bind("<Leave>",button_hover_leave)

#Desplazamiento del histograma a la derecha
img4 = leer_imagen("iconos/derecha.png")
b4=Button(root,image=img4,width=80,command=lambda:despDerHist())
b4.grid(row=1,column=3)
b4.bind("<Enter>",button_hover)
b4.bind("<Leave>",button_hover_leave)

#Estiramiento del histograma
img5 = leer_imagen("iconos/estiramiento.png")
b5=Button(root,image=img5,width=80,command=lambda:estHist())
b5.grid(row=1,column=4)
b5.bind("<Enter>",button_hover)
b5.bind("<Leave>",button_hover_leave)

#Histograma de la imagen ecualizada
img6 = leer_imagen("iconos/ecualizacion.png")
b6=Button(root,image=img6,width=80,command=lambda:histEcual())
b6.grid(row=1,column=5)
b6.bind("<Enter>",button_hover)
b6.bind("<Leave>",button_hover_leave)

#Estrechamiento del histograma
img7 = leer_imagen("iconos/estrechamiento.png")
b7=Button(root,image=img7,width=80,command=lambda:histEstr())
b7.grid(row=1,column=6)
b7.bind("<Enter>",button_hover)
b7.bind("<Leave>",button_hover_leave)

#Eliminar imagen
img8 = leer_imagen("iconos/eliminar.png")
b8=Button(root,image=img8,width=80,command=lambda:eliminar_img())
b8.grid(row=1,column=7)
b8.bind("<Enter>",button_hover)
b8.bind("<Leave>",button_hover_leave)

#Segundo parcial
#Ruido Gaussiano
img9 = leer_imagen("iconos/ruido_gaussiano.png")
b9=Button(root,image=img9,width=80,command=lambda:ruidoGaussiano())
b9.grid(row=2,column=0)
b9.bind("<Enter>",button_hover)
b9.bind("<Leave>",button_hover_leave)

#Ver histograma RGB
img10 = leer_imagen("iconos/filtro_gaussiano.png")
b10=Button(root,image=img10,width=80,command=lambda:filtroGaussiano())
b10.grid(row=2,column=1)
b10.bind("<Enter>",button_hover)
b10.bind("<Leave>",button_hover_leave)

#Desplazamiento del histograma a la izquierda
img11 = leer_imagen("iconos/roberts.png")
b11=Button(root,image=img11,width=80,command=lambda:filtroRoberts())
b11.grid(row=2,column=2)
b11.bind("<Enter>",button_hover)
b11.bind("<Leave>",button_hover_leave)

#Desplazamiento del histograma a la derecha
img12 = leer_imagen("iconos/prewitt.png")
b12=Button(root,image=img12,width=80,command=lambda:filtroPrewitt())
b12.grid(row=2,column=3)
b12.bind("<Enter>",button_hover)
b12.bind("<Leave>",button_hover_leave)

#Estiramiento del histograma
img13 = leer_imagen("iconos/sobel.png")
b13=Button(root,image=img13,width=80,command=lambda:filtroSobel())
b13.grid(row=2,column=4)
b13.bind("<Enter>",button_hover)
b13.bind("<Leave>",button_hover_leave)

#Histograma de la imagen ecualizada
img14 = leer_imagen("iconos/ecualizacion.png")
b14=Button(root,image=img14,width=80,command=lambda:filtroMaximo())
b14.grid(row=2,column=5)
b14.bind("<Enter>",button_hover)
b14.bind("<Leave>",button_hover_leave)

#Estrechamiento del histograma
img15 = leer_imagen("iconos/estrechamiento.png")
b15=Button(root,image=img15,width=80,command=lambda:filtroMinimo())
b15.grid(row=2,column=6)
b15.bind("<Enter>",button_hover)
b15.bind("<Leave>",button_hover_leave)

frame=Frame(root,height=h,width=w,bg="gray")
frame.grid(row=3,column=0,columnspan=8,sticky="nsew")

status_label = Label(root,text='',bd=1,relief=SUNKEN,anchor=E,font=(18),pady=10)
status_label.grid(row=4,column=0,columnspan=8,sticky="nsew")

root.mainloop()