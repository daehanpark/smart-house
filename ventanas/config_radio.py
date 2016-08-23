from Tkinter import *

class config_radio:

	def __init__(self):
		self.master = Tk()
		self.master.title("CONFIGURACION RADIO")
		self.master.geometry("400x250")

		self.config=None
		#etiquetas 

		lbl_encendido = Label(self.master, text = "Encendido???: ").place(x = 10, y = 10)
		lbl_volumen = Label(self.master, text = "Volumen: ").place(x = 10, y = 50)
		lbl_emisora = Label(self.master, text = "Emisora: ").place(x = 10, y = 90)
		lbl_Banda = Label(self.master, text = "Banda: ").place(x = 10, y = 130)

		#cuadros de texto
		volumen = StringVar()
		txt_volumen = Entry(self.master, textvariable = volumen)
		txt_volumen.place(x = 70, y = 50)
		
			#menu de opciones 
			#Lista que incluye todas las emisoras con banda FM
		EMISORAS_FM = {
			'Romantica 88.7': 88.7,
			'La Mega 89.3': 89.3,
			'91.3': 91.3,
			'Lider 92.3': 92.3,
			'Ven 94.3': 94.3,
			'Cnb 95.3': 95.3,
			'Turismo Stereo 95.7': 95.7,
			'Exitos 100.9': 100.9,
			'Deportiva 101.5': 101.5,
			'Studio 102.7': 102.7,
			'Solar 104.5': 104.5,
			'Onda 105.3': 105.3,
			'America 106.3': 106.3,
			'RCZ 107.3': 107.3,
			'ULA 107.7': 107.7
		 }
			#Lista con emisoras de banda AM
		EMISORAS_AM = {
			"Radio Mundial 550": 550,
			"Radio Fe y Alegria 620": 620,
			"Radio Mundial Los Andes 1040": 1040,
			"Radio Universidad 1160": 1160,
			"Radio Cumbre 1370": 1370,
			"Radio Merida 1490": 1490
		}
		var_FM = StringVar()
		var_AM = StringVar()
		var_AM.set(EMISORAS_AM.keys()[0])
		var_FM.set(EMISORAS_FM.keys()[0])


		opt_FM = OptionMenu(self.master, var_FM, *EMISORAS_FM.keys())
		opt_FM.place(x = 70, y =80)
		opt_FM.config(state = DISABLED)
		opt_AM = OptionMenu(self.master, var_AM, *EMISORAS_AM.keys())
		opt_AM.place(x = 240, y = 80)
		opt_AM.config(state = DISABLED)

		#Radiobuttons

		var_banda = StringVar(self.master)
		var_encendido = StringVar(self.master)
		opt_ban_AM = Radiobutton(self.master, text = "AM", variable = var_banda, value = 'AM', command = lambda: enable_opt_AM())
		opt_ban_AM.place(x = 55, y = 130)
		opt_ban_FM = Radiobutton(self.master, text = "FM", variable = var_banda, value = "FM", command = lambda: enable_opt_FM())
		opt_ban_FM. place( x = 100, y = 130)
		opt_si = Radiobutton(self.master, text = "SI", variable = var_encendido, value = "SI", command = lambda: enable_buttons())
		opt_si.place(x = 110, y = 10)
		opt_no = Radiobutton(self.master, text = "NO", variable = var_encendido, value = "NO", command = lambda: disable_buttons())
		opt_no. place( x = 150, y = 10)

		#Botones
		btn_configurar = Button(self.master, text = "CONFIGURAR", width = 10, command = lambda: imprimir_configuracion())
		btn_configurar.place(x = 100, y = 170)
		btn_salir = Button(self.master, text = "SALIR", command = self.master.destroy, width = 7)
		btn_salir.place(x = 220, y = 170)

		def imprimir_configuracion():
			if var_encendido.get() == 'SI':
				if var_banda.get() == 'FM': 
					self.config = {'volumen': volumen.get(), 'emisora': EMISORAS_FM[var_FM.get()], 'banda': var_banda.get()}
				else:
					self.config= {'volumen': volumen.get(), 'emisora': EMISORAS_AM[var_AM.get()], 'banda': var_banda.get()}
			else:
				self.config = {'encendido': 'no'}
			self.master.destroy()
				#print configuracion.keys(), "", configuracion.values()

		def enable_opt_FM():
			opt_FM.config(state = NORMAL)
			opt_AM.config(state = DISABLED)


		def enable_opt_AM():
			opt_AM.config(state = NORMAL)
			opt_FM.config(state = DISABLED)

		def disable_buttons():
			txt_volumen.config(state=DISABLED)
			opt_ban_FM.config(state=DISABLED)
			opt_ban_AM.config(state=DISABLED)
			opt_AM.config(state=DISABLED)
			opt_FM.config(state=DISABLED)
			volumen.set("")

		def enable_buttons():
			txt_volumen.config(state=NORMAL)
			opt_ban_FM.config(state=NORMAL)
			opt_ban_AM.config(state=NORMAL)

		self.master.mainloop()
			
	def correr(self):
		pass
		
	def get_config(self):
		return self.config



# radio = Tk()
# radio.title("CONFIGURACION_RADIO")
# radio.geometry("480x220")
# conf = config_radio(radio)
# radio.mainloop()