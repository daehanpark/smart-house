import pygame
from ventanas.config_TV import config_tv
from ventanas.config_aire import config_aire
from ventanas.config_PC import config_PC
from ventanas.config_radio import config_radio
from ventanas.config_luz import config_luz
from Usuario import Usuario
from ventanas.usuario import ventana_usuario
from Ambiente import Ambiente

class Player(pygame.sprite.Sprite):
    def __init__(self, location, orientation,screen, *groups):
        super(Player, self).__init__(*groups)
        self.image = pygame.image.load('sprites/player.png')
        self.imageDefault = self.image.copy()
        self.rect = pygame.Rect(location, (64,64))
        self.orient = orientation 
        self.holdTime = 0
        self.walking = False
        self.dx = 0
        self.step = 'rightFoot'
        self.usuario= Usuario()
        # Set default orientation
        self.setSprite()
        self.screen = screen
        self.door=False
        
    def setSprite(self):
        # Resets the player sprite sheet to its default position 
        # and scrolls it to the necessary position for the current orientation
        self.image = self.imageDefault.copy()
        if self.orient == 'up':
            self.image.scroll(0, -64)
        elif self.orient == 'down':
            self.image.scroll(0, 0)
        elif self.orient == 'left':
            self.image.scroll(0, -128)
        elif self.orient == 'right':
            self.image.scroll(0, -192)
        
    def update(self, dt, game):
        key = pygame.key.get_pressed()
        # Setting orientation and sprite based on key input: 
        if key[pygame.K_UP]:
            if not self.walking:
                if self.orient != 'up':
                    self.orient = 'up'
                    self.setSprite()
                self.holdTime += dt
        elif key[pygame.K_DOWN]:
            if not self.walking:
                if self.orient != 'down':
                    self.orient = 'down'
                    self.setSprite()    
                self.holdTime += dt
        elif key[pygame.K_LEFT]:
            if not self.walking:
                if self.orient != 'left':
                    self.orient = 'left'
                    self.setSprite()
                self.holdTime += dt
        elif key[pygame.K_RIGHT]:
            if not self.walking:
                if self.orient != 'right':
                    self.orient = 'right'
                    self.setSprite()
                self.holdTime += dt
        else:
            self.holdTime = 0
            self.step = 'rightFoot'
        # Walking mode enabled if a button is held for 0.1 seconds
        if self.holdTime >= 100:
            self.walking = True
        lastRect = self.rect.copy()
        # Walking at 8 pixels per frame in the direction the player is facing 
        if self.walking and self.dx < 64:
            if self.orient == 'up':
                self.rect.y -= 8
            elif self.orient == 'down':
                self.rect.y += 8
            elif self.orient == 'left':
                self.rect.x -= 8
            elif self.orient == 'right':
                self.rect.x += 8
            self.dx += 8
        # Collision detection:
        # Reset to the previous rectangle if player collides
        # with anything in the foreground layer
        #Colisiones
        if len(game.tilemap.layers['triggers'].collide(self.rect, 
                                                        'solid')) > 0:
            self.rect = lastRect

        #Verificacion de colisiones con los artefactos.
        if len(game.tilemap.layers['triggers'].collide(self.rect, 
                                                        'tv')) > 0:
            self.rect = lastRect
        if len(game.tilemap.layers['triggers'].collide(self.rect, 
                                                        'lamp')) > 0:
            self.rect = lastRect
        if len(game.tilemap.layers['triggers'].collide(self.rect, 
                                                        'radio')) > 0:
            self.rect = lastRect
        if len(game.tilemap.layers['triggers'].collide(self.rect, 
                                                        'air')) > 0:
            self.rect = lastRect
        if len(game.tilemap.layers['triggers'].collide(self.rect, 
                                                        'pc')) > 0:
            self.rect = lastRect
        
        #Estas colisiones son usadas para evaluar si el usuario deja el ambiente o entra a el
        if len(game.tilemap.layers['triggers'].collide(self.rect, 
                                                        'in')) > 0:
            if(self.door == False):
                game.ambiente.llegada_usuario(self.usuario,True)
                print "LLEGADA DE USUARIO"
                self.door = True
        
        if len(game.tilemap.layers['triggers'].collide(self.rect, 
                                                        'out')) > 0:
            if(self.door == True):
                game.ambiente.salida_usuario()
                print "SALIDA DE USUARIO"
                self.door=False
        
        if len(game.tilemap.layers['triggers'].collide(self.rect, 
                                                        'playerStart')) > 0 and game.keyPressed == 13:
            #ASIGNAR EL USUARIO
            #print "ESTOY PARADO SOBRE LA POSICION DEL JUGADOR"
            ventana_user= ventana_usuario()
            nombre_user = ventana_user.get_nombre()
            query="""SELECT id FROM usuarios WHERE nombre='%s'"""% (nombre_user)
            if(len(game.ambiente.database.run_query(query))>0):
                id=game.ambiente.database.run_query(query)[0][0]
            else:
                query = """INSERT INTO usuarios(nombre) VALUES ('%s')""" % (nombre_user)
                game.ambiente.database.run_query(query)
                query="""SELECT id FROM usuarios WHERE nombre='%s'"""% (nombre_user)
                id=game.ambiente.database.run_query(query)[0][0]
            print "EL ID ES :",id
            self.usuario = Usuario(id, nombre_user)



        #Interacciones, evalua que algun artefacto este alrededor de el y se presione la tecla ENTER
        if len(game.tilemap.layers['triggers'].whatsup(self.rect, self.orient, 'tv')) > 0 and game.keyPressed == 13:
            # print "Estoy interactuando con el TV"
            #game.configtv.correr()
            game.configtv = config_tv()
            if(game.configtv.get_config()!=None): #None es si presiono SALIR
                game.ambiente.obtener_pref_a_penalizar(game.ambiente.get_dispositivos()[0].get_estado_actual(),game.configtv.get_config(),game.ambiente.get_dispositivos()[0].get_tipo())
                game.ambiente.get_dispositivos()[0].configurar_dispositivo(game.configtv.get_config())
                game.ambiente.cambio_en_configuracion()
            #print "Prueba a"

        elif (len(game.tilemap.layers['triggers'].whatsup(self.rect, self.orient, 'pc')) > 0) and game.keyPressed == 13:
            # print "Estoy interactuando con la PC"
            #  game.configpc.correr()
            game.configpc = config_PC()
            if(game.configpc.get_config()!=None):#Si se realizo un cambio

                game.ambiente.obtener_pref_a_penalizar(game.ambiente.get_dispositivos()[4].get_estado_actual(),game.configpc.get_config(),game.ambiente.get_dispositivos()[4].get_tipo())
                game.ambiente.get_dispositivos()[4].configurar_dispositivo(game.configpc.get_config())
                game.ambiente.cambio_en_configuracion()
            #print "Prueba b"
            

        elif (len(game.tilemap.layers['triggers'].whatsup(self.rect, self.orient, 'radio')) > 0)  and game.keyPressed == 13:
            # print "Estoy interactuando con el RADIO"
            # game.configradio.correr()
            game.configradio = config_radio()
            if(game.configradio.get_config()!=None):
                game.ambiente.obtener_pref_a_penalizar(game.ambiente.get_dispositivos()[3].get_estado_actual(),game.configradio.get_config(),game.ambiente.get_dispositivos()[3].get_tipo())
                game.ambiente.get_dispositivos()[3].configurar_dispositivo(game.configradio.get_config())
                game.ambiente.cambio_en_configuracion()
            #print "Prueba c"
            
        elif (len(game.tilemap.layers['triggers'].whatsup(self.rect, self.orient, 'air')) > 0)  and game.keyPressed == 13:
            # print "Estoy interactuando con el AIRE"
            #game.configaire.correr()
            game.configaire = config_aire()
            if(game.configaire.get_config()!=None):
                game.ambiente.obtener_pref_a_penalizar(game.ambiente.get_dispositivos()[1].get_estado_actual(),game.configaire.get_config(),game.ambiente.get_dispositivos()[1].get_tipo())
                game.ambiente.get_dispositivos()[1].configurar_dispositivo(game.configaire.get_config())
                game.ambiente.cambio_en_configuracion()
            #print "Prueba d"
            

        #Para el manejo de la luz, evalua si el jugador se encuentra a lado de la lampara y presiona enter mas una de las teclas del 1 al cuatro
        elif (len(game.tilemap.layers['triggers'].whatsup(self.rect, self.orient, 'lamp')) > 0) and game.keyPressed == 13:
            #game.configluz.correr()
            game.configluz = config_luz()
            if(game.configluz.get_config()!=None):
                game.ambiente.obtener_pref_a_penalizar(game.ambiente.get_dispositivos()[2].get_estado_actual(),game.configluz.get_config(),game.ambiente.get_dispositivos()[2].get_tipo())
                game.ambiente.get_dispositivos()[2].configurar_dispositivo(game.configluz.get_config())
                game.ambiente.cambio_en_configuracion()
            #print "Prueba e"

        # Switch to the walking sprite after 32 pixels 
        if self.dx == 32:
            # Self.step keeps track of when to flip the sprite so that
            # the character appears to be taking steps with different feet.
            if (self.orient == 'up' or 
                self.orient == 'down') and self.step == 'leftFoot':
                self.image = pygame.transform.flip(self.image, True, False)
                self.step = 'rightFoot'
            else:
                self.image.scroll(-64, 0)
                self.step = 'leftFoot'
        # After traversing 64 pixels, the walking animation is done
        if self.dx == 64:
            self.walking = False
            self.setSprite()    
            self.dx = 0
        
        game.tilemap.set_focus(self.rect.x, self.rect.y)