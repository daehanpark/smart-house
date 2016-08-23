from SHDatabase import SHDatabase
from Dispositivo import Dispositivo
from datetime import datetime, timedelta
from Usuario import Usuario

#Clase que inicializa el ambiente y maneja el tiempo de el mismo para la simulacion
class Ambiente:
    dias=('monday','tuesday','wednesday','thursday','friday','saturday','sunday')
    database = SHDatabase()
    #Constructor, todos los tiempos en segundos
    def __init__(self,timer_config=300):
        self.__num_devices = 0
        self.__dispositivos = [] #lista de dispositivos --> LISTA no DICCTIONARIO
        self.__usuario = None
        self.__MAX_timer_config = timer_config
        self.__timer_alone = 0
        self.__timer_config = 0
        self.__ambiente_solo=True
        self.__nueva_configuracion=False        
        self.__hora_actual = datetime(2015,2,2,6,0,5) #incializa el reloj en 12:00:00 y un anio y dia arbitrario

        self.agente_decidio = False
        self.penalizar = {'televisor':{} ,'aire':{},'luz':{},'radio':{},'computador':{}}

    def is_ambiente_solo(self):
        return self.__ambiente_solo
    
    def is_nueva_config(self):
        return self.__nueva_configuracion
    
    def get_dispositivos(self):
        return self.__dispositivos
    
    def get_usuario(self):
        return self.__usuario
    
    def get_num_devices(self):
        return self.__num_devices

    def llegada_usuario(self,usuario,isLlegada):
        self.__usuario=usuario
        self.__ambiente_solo=False
        self.__timer_alone = 0
        pref= self.buscar_preferencias_usuario(False)
        if(len(pref)>0):
            self.configurarDispositivos(self.seleccionarPopulares(pref))
            self.agente_decidio =True
        elif(isLlegada):
            pref= self.buscar_preferencias_usuario(True)
            if(len(pref)>0):
                self.configurarDispositivos(self.seleccionarPopulares(pref))
                self.agente_decidio =True
        self.cambio_en_configuracion()
                
        
        
        
    def salida_usuario(self):   
        self.__ambiente_solo=True
        self.__usuario=None
        self.__nueva_configuracion=False
        

    def get_usuario_actual(self):
        if(self.__usuario==None):
            return None;
        return self.__usuario.get_nombre()
    
#     def set_usuario_actual(self, usuario):
#         self.__usuario = usuario

    #Funcion que aumenta el tiempo del ambiente la cantidad de segundos que se le pase con "tiempo_aumento"
    def aumentar_reloj_ambiente(self, tiempo_aumento):
        self.__hora_actual = self.__hora_actual + timedelta(seconds = tiempo_aumento )

    #Devuelve la variable tiempo formateada  Hora:Min:Segs.
    def get_hora_actual(self):
        return self.__hora_actual.strftime("%H:%M:%S")
    
    def get_min_sec(self):
        return self.__hora_actual.strftime("%M:%S")
    
    def get_dia_actual(self):
        return self.dias[self.__hora_actual.date().weekday()]
    
    def get_dia_actual_esp(self):
        day= self.dias[self.__hora_actual.date().weekday()]
        if(day=="monday"):
            return "lunes"
        elif(day=="tuesday"):
            return "martes"
        elif(day=="wednesday"):
            return "miercoles"
        elif(day=="thursday"):
            return "jueves"
        elif(day=="friday"):
            return "viernes"
        elif(day=="saturday"):
            return "sabado"
        elif(day=="sunday"):
            return "domingo"

    def get_estado_actual_busqueda(self):
        estado =[]
        for disp in self.__dispositivos:
            estado.insert(disp.tipo_index,str(int(disp.encendido)))
        return ''.join(estado)

    def agregar_dispositivo(self,disp):
        self.__dispositivos.insert(disp.tipo_index,disp)
        self.__num_devices+=1
    
    def apagar_dispositivo(self,dispositivo):
        self.__dispositivos[dispositivo].encendido = False
        
    #TODOS LOS TIEMPOS SE COMPARAN EN SEGUNDOS
    def verificar_dispositivos_a_apagar(self):
        for disp in self.__dispositivos:
            if(disp.get_tiempo_apagado()<=self.__timer_alone):
                print "TIEMPO APAGADO: ",disp.get_tiempo_apagado()
                print "TIEMPO SOLO: ",self.__timer_alone
                self.apagar_dispositivo(disp.get_tipo_index())
    
    def aumentar_tiempo_solo(self,delta):
        self.__timer_alone+=delta

    def aumentar_tiempo_config(self,delta):
        self.__timer_config+=delta
    
    def cambio_en_configuracion(self):
        self.__nueva_configuracion=True
        self.__timer_config =0
    
    def expiro_tiempo_nueva_configuracion(self):
        #print "TIMER CONFIG: ",self.__timer_config
        #print "TIMER CONFIG MAX: ",self.__MAX_timer_config
        return (self.__timer_config >= self.__MAX_timer_config)
    
    
    #OJO AQUI!!
    def buscar_preferencias_usuario(self,cualquier_dia_y_hora):
        query = """SELECT *
                    FROM v_preferencia_usuarios PU
                    WHERE PU.nombre_usuario='%s'""" % (self.__usuario.get_nombre())
        if(not cualquier_dia_y_hora):
            query+=" AND PU.dia='%s' AND PU.hora='%s'"% (self.get_dia_actual(),self.__hora_actual.hour)
        return self.database.run_query(query)
        #return query

    #Esta parte no me convence mucho.. pero bueno, al menos funciona .. si lo hace?
    #Se podria decir que esta funcion es como auxiliar, mientras se implementa toda la logica
    #Aqui podria llamar es una funcion que retorne el COUNT de las ocurrencias en la BD --> Solo por razones de eficiencia        
    #Otra forma es llamar esta funcion aparte, osea que no sea parte de la clase. asi si tiene resultados, ya trabaja con ellos, sino
    # realiza la otra consulta y asi
    
    def tiene_preferencias_usuario(self):
        if(len(self.buscar_preferencias_usuario(False))>0):
            return 1 #Si hay preferencias para ese dia y hora
        elif(len(self.buscar_preferencias_usuario(True))>0):
            return 2 #Hay preferencias para ese usuario, pero no para esa hora y dia
        else:
            return 0 #No hay preferencias para ese usuario



    #Filtra todos las preferencias de un usuario, para retornar solo la mas popular
    #OJO AQUI SE DEBE VERIFICAR LO DEL DISCRIMINANTE DE APAGADO.. O NO ES AQUI? 
    
    def seleccionarPopulares(self, lista_preferencias):
        populares = {}
        for elem in lista_preferencias:
            #Lo que se debe verificar es que exista 
            #el par <nombre_dispositivo,nombre_atributo>
            if(populares.has_key(elem[3]+elem[4])):
                if(populares[elem[3]+elem[4]][8] < elem[8] ):
                    populares[elem[3]+elem[4]] = elem
            else:
                populares[elem[3]+elem[4]] = elem
        return populares.values()
    
    #Esta es la planificacion 
    def configurarDispositivos(self,lista_pref): 
        #televisor','aire','luz','radio','computador'
        TV =  {}
        AIRE = {}
        LUZ = {}
        RADIO = {} 
        PC = {}
        
        for pref in lista_pref:
            if pref[3]==Dispositivo.tipos[0]:
                TV[pref[4]]=pref[5]
            elif pref[3]==Dispositivo.tipos[1]:
                AIRE[pref[4]]=pref[5]
            elif pref[3]==Dispositivo.tipos[2]:
                LUZ[pref[4]]=pref[5]
            elif pref[3]==Dispositivo.tipos[3]:
                RADIO[pref[4]]=pref[5]
            elif pref[3]==Dispositivo.tipos[4]:
                PC[pref[4]]=pref[5]

        self.__dispositivos[0].configurar_dispositivo(TV)
        self.__dispositivos[1].configurar_dispositivo(AIRE)
        self.__dispositivos[2].configurar_dispositivo(LUZ)
        self.__dispositivos[3].configurar_dispositivo(RADIO)
        self.__dispositivos[4].configurar_dispositivo(PC)
        
    def preferencia_existe(self,dispo,atrib,valor):
        query = """SELECT * FROM v_preferencia P 
        WHERE P.nombre_dispositivo = '%s' AND P.nombre_atributo='%s' AND P.valor='%s' 
        AND P.hora='%s' AND P.dia='%s'""" % (dispo,atrib,valor,self.__hora_actual.hour,self.get_dia_actual())
        resultado = self.database.run_query(query)
        if(len(resultado)>0):
            return int(resultado[0][0]) #Retornar el ID de la preferencia (SI existe es unica)
        else:
            return -1 #Si no existe la preferencia se retorna -1

    def preferencia_usuario_existe(self,id_preferencia):
        query = """SELECT * FROM v_preferencia_usuarios PU
        WHERE PU.id_usuario = '%s' AND PU.id_preferencia='%s'""" % (self.__usuario.get_id_usuario(),id_preferencia)
        resultado = self.database.run_query(query)
        if(len(resultado)>0):
            return int(resultado[0][8]) #Retornar la popularidad (Si existe la relacion es unica)
        else:
            return -1 #Si no existe la relacion se retorna -1
    
    def guardar_preferencia_usuario(self,id_preferencia):
        query ="""INSERT INTO usuarios_preferencias(id_usuario,id_preferencia,popularidad) VALUES('%s','%s','%s')"""%(self.__usuario.get_id_usuario(),id_preferencia,1)        
        self.database.run_query(query)
        
    def guardar_usuario(self,nombre):
        query ="""INSERT INTO usuarios(nombre) VALUES('%s')"""%(nombre)        
        self.database.run_query(query)
        
    def aumentar_popularidad_preferencia_usuario(self,id_preferencia,popularidad):
        query ="""UPDATE usuarios_preferencias SET popularidad='%s' 
        WHERE id_usuario = '%s' AND id_preferencia='%s'""" % (popularidad,self.__usuario.get_id_usuario(),id_preferencia)
        self.database.run_query(query)
    
    def guardar_preferencia(self,id_atributo,valor):
        dia=self.get_dia_actual()
        hora=self.__hora_actual.hour
        #print "HORA ES: ",hora
        query ="""INSERT INTO preferencias(id_atributo,valor,hora,dia) VALUES('%s','%s','%s','%s')"""%(id_atributo,valor,hora,dia)
        #Hacer que aqui me retorne el valor del ID de esa nueva preferencia, para asi poder crear la relacion con usuario
        self.database.run_query(query)
        query="""SELECT id FROM preferencias WHERE id_atributo='%s' AND
        valor='%s' AND dia='%s' AND hora='%s'"""%(id_atributo,valor,dia,hora)
        resultado= self.database.run_query(query)
        print "VALOR DE RESAULTADO: ",resultado
        return int(resultado[0][0]) #Aqui se esta  retorenando el ID de la preferencia
        
    #Metodo para recorrer la lista de dispositivos y guardar el estado
    #actual (Las preferencias y sus valores) para ese usuario
    def guardar_estado_ambiente(self):
        for dispo in self.__dispositivos:
            tipo = dispo.get_tipo()
            for atrib,valor in dispo.get_estado_actual().iteritems():
                id_pref=self.preferencia_existe(tipo, atrib, valor)
                if(id_pref!=-1):
                    popularidad=self.preferencia_usuario_existe(id_pref)
                    if(popularidad!=-1):
                        self.aumentar_popularidad_preferencia_usuario(id_pref, popularidad+1)
                    else:
                        self.guardar_preferencia_usuario(id_pref)
                else:
                    print "TIPO Y ATRIB: ",tipo,", ",atrib
                    query="""SELECT id FROM atributos WHERE nombre_dispositivo='%s' AND
                            nombre_atributo='%s'"""%(tipo,atrib)
                    id_atributo= self.database.run_query(query)[0][0]
                    print "TIPO DE ID_ATRIBUTO: ",id_atributo
                    id_pref=self.guardar_preferencia(str(id_atributo), valor)
                    self.guardar_preferencia_usuario(id_pref)
        self.__nueva_configuracion = False
        self.__timer_config =0
                           
    def insert_attribute(self, name, device):
        query = "INSERT INTO atributos (nombre_dispositivo,nombre_atributo) VALUES ('%s', '%s')" % (device, name)
        result = self.database.run_query(query)
        return result
     
    def guardar_dispositivos(self):
        for dispo in self.__dispositivos:
            for atr in dispo.get_lista_atributos():
                self.insert_attribute(atr, dispo.get_tipo())
    
    
    
    def obtener_pref_a_penalizar(self,actual,nuevo,nombre_disp):
        print "VALOR DE PENALIZAR: ",self.penalizar[nombre_disp]
        if(actual.has_key('encendido') and (not nuevo.has_key('encendido'))):
            print nombre_disp
            self.penalizar[nombre_disp]['encendido']='no'
            return;
        
        if((not actual.has_key('encendido' )) and nuevo.has_key('encendido')):
            for atrib,valor in actual.iteritems():
                self.penalizar[nombre_disp][atrib]=valor
            return;
        
        for atrib,valor in actual.iteritems():
            if(nuevo[atrib]!=valor):
                if(not self.penalizar[nombre_disp].has_key(atrib)):
                    self.penalizar[nombre_disp][atrib]=valor
    
    def penalizar_preferencias(self):
        for dispo,pref in self.penalizar.iteritems():
            for atrib,valor in pref.iteritems():
                id_pref =self.preferencia_existe(dispo,atrib,valor) 
                if(id_pref!= -1):
                    popularidad = self.preferencia_usuario_existe(id_pref)
                    if(popularidad!= -1 and popularidad>0):
                        self.aumentar_popularidad_preferencia_usuario(id_pref, popularidad-1)
    
    #METODOS POR DEFINIR.. YA CON LAS QUERY:
    # -  Verificar y agregar en tal caso lo del contador pcuando el agente configure por lo de la penalizacion
    # - OJO ->Se debe hacer una suma de ambos timer, el de modificar y el de agente configurando... creo
    # - INTEGRAR LA BUSQUEDA ( ya teniendo el estado es facil)
    # - Implementar la logica para que segun el estado final, configure el ambiente... Ir abriendo paso a la planificacion
    # - La planificacion puede ser como el diagrama en el block (Ver hoja)


    # def mostrar_valores(self):
    #     print self.__num_devices 
    #     print self.__estado_actual 
    #     print self.__usuario_nombre 
    #     print self.__timer_config
    #     print self.__timer_alone
    #     #print self.__time                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
    #     print self.__weekday
    #     print self.asignar_weekday()
    

#Descomentar para hacer prueba
#Creacion de los dispositivos del ambiente
if __name__ == '__main__':
    luz = Dispositivo(2,{'intensidad':10},600)
    tv= Dispositivo(0,{'volumen':22,'canal':33},900)
    computador = Dispositivo(4,{'sist_op':'linux'},36000) #10 Horas
    radio = Dispositivo(3,{'emisora': '103.3', 'banda':'FM', 'volumen':87},3000)
    aire = Dispositivo(1,{'temperatura':22,'velocidad':97},600)
    #aire.encendido = True
    tv.encendido = True
    aire.encendido = True
    # aire.encendido = True
    amb = Ambiente(120) #Tiempo en segundos
    amb.agregar_dispositivo(luz)
    amb.agregar_dispositivo(radio)
    amb.agregar_dispositivo(aire)
    amb.agregar_dispositivo(tv)
    amb.agregar_dispositivo(computador)
    # Guarda en la base de datos los dispositivos
    #amb.guardar_dispositivos()
    print amb.get_dia_actual()
    print type(amb.get_dia_actual())
    # amb.mostrar_valores()
    print amb.get_hora_actual()
    amb.aumentar_reloj_ambiente(3765)
    print amb.get_hora_actual()
    #amb.guardar_usuario("pedro")
    usuario = Usuario(1, "pedro")
    #amb.set_usuario_actual(usuario)
    amb.llegada_usuario(usuario)
    
    # print amb.get_time()
    print "ESTADO DEL AMBIENTE PARA LA BUSQUEDA: \n\n"
    print amb.get_estado_actual_busqueda()
    print "PREFERENCIAS: ",len(amb.buscar_preferencias_usuario(False))
    
    print "PRUEBAS DE QUERYS:"
    print "PRUEBAS DE PREFERENCIAS 1:"
    print amb.buscar_preferencias_usuario(False)
    
    print "PRUEBAS DE PREFERENCIAS 2:"
    print amb.buscar_preferencias_usuario(True)
    
    amb.guardar_estado_ambiente()
    
    print "PRUEBAS DE QUERYS:"
    print "PRUEBAS DE PREFERENCIAS 1:"
    print amb.buscar_preferencias_usuario(False)
    
    print "PRUEBAS DE PREFERENCIAS 2:"
    print amb.buscar_preferencias_usuario(True)
    
    print "PRUEBAS DE PREFERENCIAS 3 ALFA OMEGA ROJO:"
    pref=  amb.buscar_preferencias_usuario(False)
    config = amb.seleccionarPopulares(pref)
    amb.configurarDispositivos(config)
    print config
    amb.guardar_estado_ambiente()
    # insertar una preferencia
    # print "VALOR DE ID: "
    # amb.guardar_preferencia_usuario(1)