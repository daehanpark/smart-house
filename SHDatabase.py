import MySQLdb

class SHDatabase:
	def __init__(self, DB_HOST="localhost", DB_USER="root", DB_PASS="", DB_NAME="smarthouse"):
		self.datos = [DB_HOST, DB_USER, DB_PASS, DB_NAME]

	def run_query(self, query=''): 
		conn = MySQLdb.connect(*self.datos) # Conectar a la base de datos 
		cursor = conn.cursor()         # Crear un cursor 
		cursor.execute(query)          # Ejecutar una consulta 
		if query.upper().startswith('SELECT'): 
			data = cursor.fetchall()   # Traer los resultados de un select 
		else: 
			conn.commit()              # Hacer efectiva la escritura de datos 
			data = None 
		cursor.close()                 # Cerrar el cursor 
		conn.close()                   # Cerrar la conexion 
		return data

# 	def getPrefDiaHora(self,usuario,dia,hora):
# 		query = """SELECT A.nombre_atributo, A.nombre_dispositivo,P.valor,UP.popularidad
# 					FROM usuarios U, preferencias P, atributos A, usuarios_preferencias UP
# 					WHERE U.usuario='%s' AND U.id=UP.id_usuario AND UP.id_preferencia=P.id AND P.id_atributo=A.id AND P.dia='%s' AND P.hora<='%s'""" % (usuario,dia,hora)
# 		return self.run_query(query)
# 
# 	def getPref(self,usuario):
# 		query = """SELECT A.nombre_atributo, A.nombre_dispositivo,P.valor,UP.popularidad
# 					FROM usuarios U, preferencias P, atributos A, usuarios_preferencias UP
# 					WHERE U.usuario='%s' AND U.id=UP.id_usuario AND UP.id_preferencia=P.id AND P.id_atributo=A.id""" % (usuario)
# 		return self.run_query(query)
# 
# 	def seleccionarPopulares(self, list):
# 		populares = {}
# 		for elem in list:
# 			if(populares.has_key(elem[1]+elem[0])):
# 				if(populares[elem[1]+elem[0]][3] < elem[3] ):
# 					populares[elem[1]+elem[0]] = elem
# 			else:
# 				populares[elem[1]+elem[0]] = elem
# 		return populares.values()
# 
# 	def insertarPreferencia(self,dispositivos):
# 		for tipo, dispo in dispositivos.iteritems():
# 			print type(tipo)
# 			print type(dispo)
# 			print tipo
# 			print dispo
# 			for atrib, valor in dispo.atributos.iteritems():
# 				if(self.preferencia_existe(tipo,atrib,valor)):
# 					print "YA EXISTE LA PREFERENCIA"
# 
# 				else:
# 					print "NO EXISTE LA PREFERENCIA"
# 					query = """SELECT A.id
# 					FROM atributos A
# 					WHERE A.nombre_atributo = '%s' AND A.nombre_dispositivo='%s'""" % (atrib,tipo)
# 					id_atrib= int(self.run_query(query)[0][0])
# 					print "VALOR DE ID ATRIB: ",id_atrib
# 					query ="""INSERT INTO preferencias(id_atributo,valor,hora,dia) VALUES('%s','%s','%s','%s')"""%(id_atrib,valor,'23:00:00','tuesday')
# 					self.run_query(query)
# 
# #Ojo, aqui verifica si la preferencia existe, NO si ya esta asociada a ese usuario o no, ese metodo falta
# #Tambien falta que se compare con el dia y la hora
# 	def preferencia_existe(self,tipo,atrib,valor):
# 		query = """SELECT P.id, A.nombre_atributo, A.nombre_dispositivo, P.valor
# 					FROM preferencias P, atributos A
# 					WHERE P.id_atributo=A.id AND A.nombre_atributo = '%s' AND A.nombre_dispositivo='%s' AND P.valor='%d'""" % (atrib,tipo,int(valor))
# 		print """CANTIDAD DE PREFERENCIAS DE TIPO: (tipo,atrib,valor): ('%s','%s','%d'): '%d'"""%(tipo,atrib,int(valor),len(self.run_query(query)))
# 		return (len(self.run_query(query))>0)
# 
# 
# 	def getminMaxHour(self,hora):
# 		time = str(hora)+":00:00"
# 		print time
# 		query = """SELECT *
# 					FROM preferencias P
# 					WHERE P.hora='%s' """ % (time)
# 		result=self.run_query(query)
# 		print "CANTIDAD DE RESULTADOS: %d"%len(result)
# 		print result
# 		return time
# 
# 
# class Dispositivo:
# 	def __init__(self,atributos):
# 		self.atributos = atributos
# 
# 	def configurar(self,atributo, valor):
# 		self.atributos[atributo] = valor


# hola = SHDatabase()
# tv = Dispositivo({'volumen': 24, 'canal':50})
# luz = Dispositivo({'intensidad': 63})
# #radio = Dispositivo({'volumen': 54, 'emisora':102.4,'banda': "FM"})
# disp = {'televisor' :tv,'luz': luz}
# #hola.insertarPreferencia(disp,'luz')
# hola.getminMaxHour(20)
# print "ANTES DE CONFIGURAR"
# #radio.configurar('emisora',92.3)
# #disp[2].configurar('emisora',92.3)
# print "DESPUES DE CONFIGURAR"
# hola.insertarPreferencia(disp)
# 
# while raw_input("Desea continuar haciendo consultas?")!="no":
# 	usuario = raw_input()
# 	pref_david = hola.getPrefDiaHora(usuario,"monday","20:53:32")
# 	print pref_david
# 	if len(pref_david) <=0:
# 		print "NO HAY PREFERENCIAS PARA ESTE DIA Y HORA... BUSCANDO PREFERENCIAS DE CUALQUIER DIA Y HORA..."
# 		pref_david = hola.getPref(usuario)
# 		print "Antes \n\n"
# 		print hola.seleccionarPopulares(pref_david)
# 		print "\n\nDespues "
# 
# 		if len(pref_david) <=0:
# 			print "NO HAY PREFERENCIAS PARA ESTE USUARIO... USANDO CONFIGURACION ACTUAL COMO PREFERENCIA DE USUARIO E INICIANDO CRONOMETRO DE ACEPTACION DE PREFERENCIA..."
# 	else:
# 		print "Antes \n\n"
# 		print hola.seleccionarPopulares(pref_david)
# 		print "\n\nDespues "