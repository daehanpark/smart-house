from Tkinter import *

class config_aire:

	def __init__(self):

		
		#variables asociadas a los objetos de la ventana config_aire 

		self.master = Tk()
		self.master.title("CONFIGURACION AIRE")
		self.master.geometry("300x250")

		self.config=None
		var_temperatura = StringVar()
		var_velocidad = StringVar()
		var_encendido = StringVar()

		TEMPERATURA = {
			'16 C': 16,
			'17 C': 17,
			'18 C': 18,
			'19 C': 19,
			'20 C': 20,
			'21 C': 21,
			'22 C': 22,
			'23 C': 23,
			'24 C': 24,
			'25 C': 25,
			'26 C': 26,
			'27 C': 27,
			'28 C': 28
		}

		#etiquetas

		lbl_velocidad = Label(self.master, text = "Velocidad:")
		lbl_velocidad.place(x = 10, y = 50)

		lbl_temperatura = Label(self.master, text = "Temperatura:")
		lbl_temperatura.place(x = 10, y = 90)

		lbl_rpm = Label(self.master, text = "RPM")
		lbl_rpm.place(x = 130, y = 50)

		lbl_encendido = Label(self.master, text = "Encendido??:")
		lbl_encendido.place(x = 10, y = 10)

		#Caja de texto

		txt_velocidad = Entry(self.master, textvar = var_velocidad, width = 5)
		txt_velocidad.place(x = 80, y = 50)

		#Menu de Opciones 

		opt_temp = OptionMenu(self.master, var_temperatura, *TEMPERATURA.keys())
		opt_temp.place(x = 100, y = 80)


		#RadioButtons

		opt_si = Radiobutton(self.master, text = "SI", variable = var_encendido, value = 'SI',
			command = lambda: enable_options())
		opt_si.place(x = 100, y = 10)
		opt_no = Radiobutton(self.master, text = "NO", variable = var_encendido, value = 'NO', 
			command = lambda: disable_options())
		opt_no.place(x = 150, y = 10)

		#Botones

		btn_configurar = Button(self.master, text = "CONFIGURAR", width = 10, command = lambda: configuracion_aire())
		btn_configurar.place(x = 50, y = 120)
		btn_salir = Button(self.master, text = "SALIR", command = self.master.destroy, width = 7)
		btn_salir.place(x = 170, y = 120)


		def enable_options():
			txt_velocidad.config(state = NORMAL)
			opt_temp.config(state = NORMAL)

		def disable_options():
			txt_velocidad.config(state = DISABLED)
			opt_temp.config(state = DISABLED)
			var_velocidad.set("")

		def configuracion_aire():

			if var_encendido.get() == 'SI':
				self.config = {'velocidad': var_velocidad.get(), 'temperatura': TEMPERATURA[var_temperatura.get()]}
			else:
				self.config = {'encendido': 'no'}
			self.master.destroy()
			#print configurar_aire.keys(), "", configurar_aire.values()
		
		self.master.mainloop()
	def correr(self):
		pass
	
	def get_config(self):
		return self.config

# aire = Tk()
# aire.geometry("300x160")
# aire.title("CONFIGURACION_AIRE")
# configuracion = config_aire(aire)
# aire.mainloop()