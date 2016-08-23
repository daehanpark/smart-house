import pygame
from player import *
from mapa import tmx
import interacciones

from Tkinter import *
from datetime import datetime, timedelta
from Ambiente import Ambiente
from Dispositivo import Dispositivo
from Usuario import Usuario
from ventanas.config_TV import config_tv
from ventanas.config_aire import config_aire
from ventanas.config_luz import config_luz
from ventanas.config_radio import config_radio
from ventanas.config_PC import config_PC

from tipoambiente.difuso import Difuso

class Game(object):
    def __init__(self, screen):
        #Inicializacion de los dispositivos
        tv= Dispositivo(0,{'volumen':0,'canal':0},900)
        aire = Dispositivo(1,{'temperatura':0,'velocidad':0},600)
        luz = Dispositivo(2,{'intensidad':0},600)
        radio = Dispositivo(3,{'emisora': '88.0.', 'banda':'FM', 'volumen':0},3000)
        computador = Dispositivo(4,{'sist_op':'linux'},36000) #10 Horas

        self.ambiente = Ambiente(600) #Tiempo en segundos
        self.ambiente.agregar_dispositivo(tv)
        self.ambiente.agregar_dispositivo(aire)
        self.ambiente.agregar_dispositivo(luz)
        self.ambiente.agregar_dispositivo(radio)
        self.ambiente.agregar_dispositivo(computador)
        
        self.contador = 0
        self.screen = screen
        self. constTime = 1
        self.keyPressed = None
        self.opacity = 1
        #Inicializacion de las ventanas de configuracion
        #de los dispositivos 
        
        self.__crear_cuadros_texto()
    
        #se crea una superficie de el tamano de la ventana para las luces
        self.blackRect = pygame.Surface(self.screen.get_size())
        #se rellena con el color 0 negro
        self.blackRect.fill((0,0,0))
        self.font = pygame.font.SysFont("Myriad Pro", 48)
        
        
        self.difuso = Difuso()
        

    def __crear_cuadros_texto(self):
        #Retangulos blancos donde iran los datos de los disposititvos
        self.linea_div = pygame.Surface((1024, 5))
        self.rect1 = pygame.Surface((200,168))
        self.rect2 = pygame.Surface((200,168))
        self.rect3 = pygame.Surface((200,168))
        self.rect4 = pygame.Surface((200,168))
        self.rect5 = pygame.Surface((200,168))
        
        #Rectangulos negros dentro de los blancos
        self.rect1_in = pygame.Surface((196,164))
        self.rect2_in = pygame.Surface((196,164))
        self.rect3_in = pygame.Surface((196,164))
        self.rect4_in = pygame.Surface((196,164))
        self.rect5_in = pygame.Surface((196,164))
        #Rellenado blanco 
        self.linea_div.fill((255,255,255))
        self.rect1.fill((255,255,255))
        self.rect2.fill((255,255,255))
        self.rect3.fill((255,255,255))
        self.rect4.fill((255,255,255))
        self.rect5.fill((255,255,255))
        #Rellenado de Negro
        self.rect1_in.fill((0,0,0))
        self.rect2_in.fill((0,0,0))
        self.rect3_in.fill((0,0,0))
        self.rect4_in.fill((0,0,0))
        self.rect5_in.fill((0,0,0))
        #Se crean los titulos para cada dispositivo
        self.fontRecuadros = pygame.font.SysFont("Myriad Pro", 30)
        self.titulo_TV = self.fontRecuadros.render("TV", 1, (255, 255, 255), (0, 0, 0))
        self.titulo_Radio = self.fontRecuadros.render("Radio", 1, (255, 255, 255), (0, 0, 0))
        self.titulo_PC = self.fontRecuadros.render("PC", 1, (255, 255, 255), (0, 0, 0))
        self.titulo_Luz = self.fontRecuadros.render("Luz", 1, (255, 255, 255), (0, 0, 0))
        self.titulo_Aire = self.fontRecuadros.render("Aire", 1, (255, 255, 255), (0, 0, 0))
    
    def initArea(self, mapFile):
        """Carga los mapas e inicializa los sprites"""

        self.tilemap = tmx.load(mapFile, screen.get_size())
        self.tvs = tmx.SpriteLayer()
        self.lamps = tmx.SpriteLayer()
        self.pcs = tmx.SpriteLayer()
        self.players = tmx.SpriteLayer()
        self.objects = tmx.SpriteLayer()
        self.radios = tmx.SpriteLayer()
        self.aires = tmx.SpriteLayer()
        
        #Se agregan a la lista de capas (layers ), todas las imagenes que se van a colocar sobre el mapa en tiempo real.
        startCell = self.tilemap.layers['triggers'].find('playerStart')[0]
    
        self.player = Player((startCell.px, startCell.py), startCell['playerStart'], self.screen, self.players)
        self.tv = interacciones.sprite_TV( self.ambiente.get_dispositivos()[0].encendido,self.screen, (64, 96) , self.tvs)
        self.pc = interacciones.sprite_PC( self.ambiente.get_dispositivos()[4].encendido,self.screen, (384, 96) , self.pcs)
        self.lamp1 = interacciones.sprite_Lamp( self.ambiente.get_dispositivos()[2].encendido,self.screen, (32, 96) , self.lamps)
        self.lamp2 = interacciones.sprite_Lamp( self.ambiente.get_dispositivos()[2].encendido,self.screen, (512, 96) , self.lamps)
        self.lamp3 = interacciones.sprite_Lamp( self.ambiente.get_dispositivos()[2].encendido,self.screen, (32, 448) , self.lamps)
        self.lamp4 = interacciones.sprite_Lamp( self.ambiente.get_dispositivos()[2].encendido,self.screen, (480, 448) , self.lamps)
        self.radio = interacciones.sprite_Radio( self.ambiente.get_dispositivos()[3].encendido,self.screen, (288, 96) , self.radios)
        self.aire = interacciones.sprite_Aire( self.ambiente.get_dispositivos()[1].encendido,self.screen, (480, 384) , self.aires)
        
        self.tilemap.layers.append(self.players)
        self.tilemap.layers.append(self.tvs)
        self.tilemap.layers.append(self.pcs)
        self.tilemap.layers.append(self.lamps)
        self.tilemap.layers.append(self.radios)
        self.tilemap.layers.append(self.aires)

        self.tilemap.set_focus(self.player.rect.x, self.player.rect.y)  
    
    def set_constTime(self):
        #Se establece la contante por la que se multiplicara el tiempo siendo introducido con el teclado 
        # 1,2,3,4,5 siendo 5 la maxima (por definir las escalas finales)
        if self.keyPressed == 49:
            self.ambiente.aumentar_reloj_ambiente(300)
            if(self.ambiente.is_ambiente_solo()):
                self.ambiente.aumentar_tiempo_solo(300)
            if(self.ambiente.is_nueva_config()):
                    self.ambiente.aumentar_tiempo_config(300)
        elif self.keyPressed == 50:
            self.ambiente.aumentar_reloj_ambiente(3600)
            if(self.ambiente.is_ambiente_solo()):
                self.ambiente.aumentar_tiempo_solo(3600)
            if(self.ambiente.is_nueva_config()):
                    self.ambiente.aumentar_tiempo_config(3600)
        elif self.keyPressed == 51:
            self.constTime = 1
            self.delta = 1
        elif self.keyPressed == 52:
            self.constTime = 5
            self.delta = 5
        elif self.keyPressed == 53:
            self.constTime = 10
            self.delta = 10
    
    def update_Game_Clock(self):
        #Se evalua a que velocidad se quiere el reloj con set_Constime
        #Luego se imprime el reloj siendo aumentado cada 30 frames.
        #Por ahora se imprimen el reloj del sistema y el de el ambiente solo para comparar
        self.set_constTime()
        if self.contador < 10:
            self.contador += self.constTime
        else:
            self.ambiente.aumentar_reloj_ambiente(5)
            if(self.ambiente.is_ambiente_solo()):
                self.ambiente.aumentar_tiempo_solo(5)
            if(self.ambiente.is_nueva_config()):
                    self.ambiente.aumentar_tiempo_config(5)
            
            self.contador = 0
        printReloj = self.font.render(self.ambiente.get_hora_actual(), 1, (255, 255, 255), (0, 0, 0))
        dia = self.font.render(self.ambiente.get_dia_actual_esp(), 1, (255, 255, 255), (0, 0, 0))
        
        
        
        #Imprimir nombre del usuario actual
        usuario=self.ambiente.get_usuario_actual()
        if(usuario!=None):
            user = self.font.render("Usuario: "+usuario, 1, (255, 255, 255), (0, 0, 0))
        else:            
            user = self.font.render("AMBIENTE SOLO", 1, (255, 255, 255), (0, 0, 0))
        screen.blit(dia, (0, 0))
        screen.blit(printReloj, (200, 0))
        screen.blit(user, (0, 50))
        
        dispo =self.ambiente.get_dispositivos()
        self.difuso.setInput(int(dispo[1].get_atributo("temperatura")),int(dispo[0].get_atributo("volumen")),int(dispo[2].get_atributo("intensidad")))
        tipo_a = self.font.render("Tipo de ambiente: "+self.difuso.getOutput(), 1, (255, 255, 255), (0, 0, 0))
        screen.blit(tipo_a, (500,0))
        

    def update_Layout(self):
        #Aqui se colocan los recuadros sobre los que se imprimen las cadenas de texto luego
        screen.blit(self.linea_div, (0,570))
        screen.blit(self.rect1, (3,579))  
        screen.blit(self.rect2, (207,579))
        screen.blit(self.rect3, (411,579))
        screen.blit(self.rect4, (615,579))
        screen.blit(self.rect5, (819,579))      
        screen.blit(self.rect1_in, (5,581))
        screen.blit(self.rect2_in, (209,581))      
        screen.blit(self.rect3_in, (413,581))      
        screen.blit(self.rect4_in, (617,581))      
        screen.blit(self.rect5_in, (821,581))

    def update_Layout_Devices(self):
        #Se Asignan los valores a imprimir, por ahora son asignados a mano, la base de dato los dara
        #y si es posible se obviara el metodo Asignar datos
        posX = 20
        for dispo in self.ambiente.get_dispositivos():
            if(not dispo.encendido):
                aux = self.fontRecuadros.render("Estado: OFF", 1, (255,255,255), (0,0,0))
                screen.blit(aux, (20+(204*dispo.tipo_index), 601))
            else:
                posY = 621
                for atrib,valor in dispo.get_estado_actual().iteritems():
                    aux = self.fontRecuadros.render((atrib+": "+str(valor)), 1, (255, 255, 255), (0, 0, 0))
                    screen.blit(aux, (posX, posY))
                    posY+=20
            posX+=204
                    
        #Se colocan los rectangulos con los Titulos sobre la pantalla en sus posiciones indicadas
        screen.blit(self.titulo_TV, (10,581))
        screen.blit(self.titulo_Aire, (214,581))
        screen.blit(self.titulo_Luz, (418,581))
        screen.blit(self.titulo_Radio, (622,581))
        screen.blit(self.titulo_PC, (826,581))

    def main(self):

        clock = pygame.time.Clock()
        self.initArea('mapa/ambiente.tmx')

        while 1:
                       
            #Se evalua cual es el valor de la opacidad, depende de cual sea se asigna con set_alpha (0-255). self.enAmbiente es un booleano
            #que indica si el usuario se encuentra dentro del ambiente
            dt = clock.tick(30)
            #CAPTURA DE ENTRADA
            self.keyPressed = None
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    self.keyPressed = event.key
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return
            #UPDATES DE EL SIMULADOR
            ##AQUI SE ACTUALIZA EL AMBIENTE, 
            #SE HACEN LAS COMPARACIONES DE LAS BANDERAS
            # Y SE HACEN LOS CAMBIOS A LA BD O AL AMBIENTE
            
                
            
            self.tilemap.update(dt, self)
            screen.fill((0,0,0))
            self.tilemap.draw(self.screen)
            #ACTUALIZACION DEL DISPLAY
            #con screen blit se coloca una imagen sobre screen, en este caso el rectangulo negro que se creo al inicio, y al que se le 
            #modifico la opacidad. Se coloca de ultimo para que no sea sobreescrito por nada
            screen.blit(self.blackRect, (0,0))
            self.update_Game_Clock()
            if(self.ambiente.is_ambiente_solo()):
                self.ambiente.verificar_dispositivos_a_apagar()
                
            if(self.ambiente.expiro_tiempo_nueva_configuracion()):
                self.ambiente.agente_decidio=False
                self.ambiente.penalizar_preferencias()
                self.ambiente.guardar_estado_ambiente()
            
            #print "MIN-SEC: ",self.ambiente.get_min_sec()
            if(self.ambiente.get_min_sec()=="00:00" and not self.ambiente.is_ambiente_solo()):    
                self.ambiente.llegada_usuario(self.ambiente.get_usuario(),False)
                    
            
            
            self.update_Layout()
            self.update_Layout_Devices()

            pygame.display.flip()

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1024, 720) )
    pygame.display.set_caption("SmartHouse")
    Game(screen).main()