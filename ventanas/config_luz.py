from Tkinter import *

class config_luz:

	def __init__(self):

		#Variables asociadas a los objetos 

		
		self.master = Tk()
		self.master.title("CONFIGURACION LUZ")
		self.master.geometry("300x250")
		
		self.config=None
		var_encendido = StringVar()
		var_intensidad = StringVar()

		

		
		#Etiquetas

		lbl_encendido = Label(self.master, text = "Encendido??:")
		lbl_encendido.place(x = 10, y = 10)

		lbl_intensidad = Label(self.master, text = "Intensidad:")
		lbl_intensidad.place(x = 10, y = 50)

		lbl_candela = Label(self.master, text = "CANDELAS")
		lbl_candela.place(x = 140, y = 50)


		#RadioButtons

		opt_si = Radiobutton(self.master, text = "SI", variable = var_encendido, value = "SI", 
			command = lambda: enable_options())
		opt_si.place(x = 90, y = 10)

		opt_no = Radiobutton(self.master, text = "NO", variable = var_encendido, value = "NO",
			command = lambda: disable_options())
		opt_no.place(x = 130, y = 10)

		#Caja de Texto

		txt_intensidad = Entry(self.master, textvar= var_intensidad, width = 5)
		txt_intensidad.place(x = 90, y = 50)

		#Botones 

		btn_configurar = Button(self.master, text = "CONFIGURAR", width = 10, command = lambda: configuracion_luz())
		btn_configurar.place(x = 50, y = 90)
		btn_salir = Button(self.master, text = "SALIR", command = self.master.destroy, width = 7)
		btn_salir.place(x = 170, y = 90)


		def enable_options():
			txt_intensidad.config(state = NORMAL)

		def disable_options():
			txt_intensidad.config(state = DISABLED)
			var_intensidad.set("")

		def configuracion_luz():

			if var_encendido.get() == 'SI':

				self.config = {'intensidad': var_intensidad.get()}

			else:
				self.config = {'encendido': 'no'}
			self.master.destroy()

			#print configurar_luz.keys(), "", configurar_luz.values()
		
		self.master.mainloop()
	
	def correr(self):
		pass
	
	def get_config(self):
		return self.config

# luz = Tk()
# luz.title("CONFIGURACION_LUZ")
# luz.geometry("300x130")
# conf = config_luz(luz)
# luz.mainloop()