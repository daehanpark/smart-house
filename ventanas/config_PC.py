from Tkinter import *

class config_PC:

	def __init__(self):

		#Variables asociadas a los objetos 
		self.master = Tk()
		self.master.title("CONFIGURACION PC")
		self.master.geometry("300x250")

		self.config=None
		
		var_encendido = StringVar()
		var_so = StringVar()		

		#Etiquetas

		lbl_encendido = Label(self.master, text = "Encendido??:")
		lbl_encendido.place(x = 10, y = 10)

		lbl_so = Label(self.master, text = "Sistema Operativo:")
		lbl_so.place(x = 10, y = 50)

		#RadioButtons

		opt_si = Radiobutton(self.master, text = "SI", variable = var_encendido, value = "SI", 
			command = lambda: enable_options())
		opt_si.place(x = 90, y = 10)

		opt_no = Radiobutton(self.master, text = "NO", variable = var_encendido, value = "NO",
			command = lambda: disable_options())
		opt_no.place(x = 130, y = 10)

		#Lista de Opciones 
		opt_so = OptionMenu(self.master, var_so, "MacSO", "Unix/Linux", "Windows")
		opt_so.place(x = 140, y = 40)
		opt_so.config(state = DISABLED)

		#Botones 

		btn_configurar = Button(self.master, text = "CONFIGURAR", width = 10, command = lambda: configuracion_SO())
		btn_configurar.place(x = 50, y = 90)
		btn_salir = Button(self.master, text = "SALIR", command = self.master.destroy, width = 7)
		btn_salir.place(x = 170, y = 90)


		def enable_options():
			opt_so.config(state = NORMAL)

		def disable_options():
			opt_so.config(state = DISABLED)

		def configuracion_SO():
			if var_encendido.get() == 'SI':
				self.config = {'sist_op': var_so.get()}
			else:
				self.config = {'encendido': 'no'}
			
			self.master.destroy()
			#print configurar_so.keys(), "", configurar_so.values()
		
		self.master.mainloop()
	
	def correr(self):
		pass

	def get_config(self):
		return self.config
		

# so = Tk()
# so.title("CONFIGURACION_LUZ")
# so.geometry("300x130")
# conf = config_SO(so)
# so.mainloop()