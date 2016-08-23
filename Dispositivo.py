#Un dispositivo es de solo un tipo durante su existencia
#Un dispositivo no puede agregar nuevos atributos luego de creado
#De necesitar otro atributo, seria otro dispositivo
class Dispositivo:
	#tupla con los tipos de dispositivos que tendra la simulacion
	tipos= ('televisor','aire','luz','radio','computador')
	#inicializa la clase dispositivo
	def __init__(self, tipo_index, atributos, tiempoApagado=-1):

		self.tipo_index=tipo_index
		self.__tiempoApagado = tiempoApagado #EN SEGUNDOS
		self.encendido = False
		#Atributos es un diccionario <clave,valor> = <nombre_atributo, valor_actual>
		self.__atributos= atributos

	#configura el valor de un atributo especifico
	def __configurar_atributo(self, atributo, valor):
		if(atributo == 'encendido' and valor == 'no'):
			self.encendido = False
		else:
			self.encendido = True
			self.__atributos[atributo] = valor

	#configura los valores de los atributos para cada dispositivos
	def configurar_dispositivo(self, configuraciones):
		for atrib,valor in configuraciones.iteritems():
			self.__configurar_atributo(atrib,valor)
		
	#retorna una lista con los nombres de los atributos de un dispositivo
	def get_lista_atributos(self):
		return self.__atributos.keys()

	#retornar estado actual, teniendo en cuenta la condicion de usar "encendido" como  discriminante
	def get_estado_actual(self):
		if(self.encendido):
			return self.__atributos
		else:
			return {'encendido': 'no'}

	#retorna el tiempo en el que un dispositivo espera para ser apagado si no esta siendo usado
	def get_tiempo_apagado(self):
		return self.__tiempoApagado

	def set_tiempo_apagado(self,tiempo):
		self.__tiempoApagado = tiempo

	def get_tipo(self):
		return self.tipos[self.tipo_index]
	
	def get_tipo_index(self):
		return self.tipo_index
	
	def get_atributo(self,atrib):
		return self.__atributos[atrib]

#Descomentar para probar los metodos de la clase

# tv = Dispositivo(0,{'volumen': 20, 'canal': 55}, 15)
# luz = Dispositivo(2,{'intensidad': 20,'velocidad':35},10)
# tv.encendido=True
# print tv.get_tipo()
# print luz.get_tipo()
# print tv.get_estado_actual()
# tv.configurar_dispositivo({'canal': 60,'volumen':44})
# print tv.get_estado_actual()
# tv.configurar_dispositivo({'canal': 12})
# print tv.get_estado_actual()
# print tv.get_tiempo()
# print luz.get_estado_actual()