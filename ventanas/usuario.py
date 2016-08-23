from Tkinter import *

class ventana_usuario:

    def __init__(self):

        #Variables asociadas a los objetos 
        self.master = Tk()
        self.master.title("Ingrese nombre de usuario")
        self.master.geometry("300x150")

        self.nombre="default"
        
        var_nombre = StringVar()        

        #Etiquetas

        lbl_nombre = Label(self.master, text = "Nombre:")
        lbl_nombre.place(x = 10, y = 10)

        #Campo de texto
        txt_nombre = Entry(self.master, textvar= var_nombre, width = 30)
        txt_nombre.place(x = 90, y = 50)

        #Botones 

        btn_aceptar = Button(self.master, text = "Aceptar", width = 10, command = lambda: asignar_nombre())
        btn_aceptar.place(x = 50, y = 90)
        
        btn_salir = Button(self.master, text = "SALIR", command = self.master.destroy, width = 7)
        btn_salir.place(x = 170, y = 90)

        def asignar_nombre():
            self.nombre = var_nombre.get()
            self.master.destroy()
        
        self.master.mainloop()

    def get_nombre(self):
        if(self.nombre!=""):
            return self.nombre
        else:
            return "default"