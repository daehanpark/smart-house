from Tkinter import *


class config_tv:

	def __init__(self):
		self.master = Tk()
		self.master.title("CONFIGURACION TV")
		self.master.geometry("300x250")
		
		self.config=None
		#variables de referencia asociadas a cada uno de los objetos de la ventana 
		newvol = StringVar()
		newchannel = StringVar()
		currentvol = StringVar()
		currentchannel = StringVar()
		var_encendido = StringVar()
		
		
		#etiquetas
		lbl_encendido = Label(self.master, text = "Encendido??:")
		lbl_encendido.place(x = 10, y = 10)

		lbl_volumen = Label(self.master, text="Volumen: ")
		lbl_volumen.place(x = 10, y = 50)

		lbl_canal = Label(self.master, text="Canal: ")
		lbl_canal.place(x = 10, y = 90)

		lbl_mostrar_volumen = Label(self.master, textvar = newvol)
		lbl_mostrar_volumen.place(x = 250, y = 50)

		lbl_mostrar_canal = Label(self.master, textvar = newchannel)
		lbl_mostrar_canal.place(x = 250, y = 90)


		#caja de texto
		txt_volumen = Entry(self.master, textvar = currentvol)
		txt_volumen.place(x = 70, y = 50)
		txt_canal = Entry(self.master, textvar = currentchannel)
		txt_canal.place(x = 70, y = 90)

		#botones de opciones 

		opt_si = Radiobutton(self.master, text = "SI", variable = var_encendido, value = 'SI', 
			command = lambda: enable_options())
		opt_si.place(x = 100, y= 10)
		opt_no = Radiobutton(self.master, text = "NO", variable = var_encendido, value = 'NO',
			command = lambda: disable_options())
		opt_no.place(x = 150, y = 10)

		#botones
		btn_configurar = Button(self.master, text = "CONFIGURAR", 
			command = lambda: configurar_tv(), width = 10)
		btn_configurar.place(x = 40, y = 140)
		btn_salir = Button(self.master, text = "SALIR", width = 7, command = self.master.destroy)
		btn_salir.place(x = 150, y = 140)

		#funcion de desabilitar las configuracion del tv
		def disable_options():
			txt_volumen.config(state = DISABLED)
			txt_canal.config(state = DISABLED)
			currentvol.set("")
			currentchannel.set("")

		#funcion para habilitar opciones aconfigurar del televisor
		def enable_options():
			txt_volumen.config(state = NORMAL)
			txt_canal.config(state = NORMAL)


		def configurar_tv():
			if var_encendido.get() == 'SI':

				self.config = {'volumen': currentvol.get(), 'canal': currentchannel.get()}
			else:
				self.config = {'encendido': 'no'}
			self.master.destroy()

			#print configuracion_tv.keys(), "", configuracion_tv.values()
		
		self.master.mainloop()

	def correr(self):
		pass
# 		self.master = Tk()
# 		self.master.title("CONFIGURACION_T2V")
# 		self.master.geometry("300x250")
	def get_config(self):
		return self.config
		
		
		
		





# principal = Tk()
# principal.title("CONFIGURACION_TV")
# principal.geometry("280x180")
# conf = config_tv()
# conf.correr()
# principal.mainloop()