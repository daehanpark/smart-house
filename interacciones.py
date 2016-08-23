import sys
import struct
import pygame
from pygame.locals import *
from pygame import Rect
from xml.etree import ElementTree
from base64 import b64decode
from zlib import decompress

class anim_Dispositivo(pygame.sprite.Sprite):
    def __init__(self, state, screen, location, *groups):
        super(anim_Dispositivo, self).__init__(*groups)
        self.state = state
        self.location = location
        self.screen = screen
        self.contadorAnim = 0
        self.imageHeight = 256


    def set_sprite(self, state, image, imageHeight):
        self.image = image
        if state == False:
            self.image.scroll(0, 0)
            self.contadorAnim = 0
        else :
            if self.contadorAnim < 10 :
                self.image.scroll(0, -imageHeight/4)
                self.contadorAnim +=1
            elif self.contadorAnim >= 10 and self.contadorAnim < 20:
                self.image.scroll(0, imageHeight/2)
                self.contadorAnim +=1
            else:
                self.image.scroll(0, imageHeight*3/4)
                self.contadorAnim +=1
        if self.contadorAnim == 30:
            self.contadorAnim = 0


class sprite_TV(anim_Dispositivo):
    def __init__(self, state,screen, location, *groups):
        super(sprite_TV, self).__init__(state,screen,location,*groups)
        self.imageTV = pygame.image.load('sprites/spriteTv.png')
        self.imageDefaultTV = self.imageTV.copy()
        self.rect = pygame.Rect(self.location, (128,64))
        super(sprite_TV, self).set_sprite(state, self.imageTV, self.imageHeight)
        
       
    def update(self, dt, game):
        self.imageTV = self.imageDefaultTV.copy()
        super(sprite_TV, self).set_sprite(game.ambiente.get_dispositivos()[0].encendido, self.imageTV, self.imageHeight)
 

class sprite_PC(anim_Dispositivo):
    def __init__(self, state,screen, location, *groups):
        super(sprite_PC, self).__init__(state,screen,location,*groups)
        self.imagePC = pygame.image.load('sprites/pcfrontSprite.png')
        self.imageDefaultPC = self.imagePC.copy()
        self.rect = pygame.Rect(self.location, (128,64))
        self.imageWidth = 128
        self.imageHeight = 256
        super(sprite_PC, self).set_sprite(state, self.imagePC, self.imageHeight)
        
    def update(self, dt, game):
        self.imagePC = self.imageDefaultPC.copy()
        super(sprite_PC, self).set_sprite(game.ambiente.get_dispositivos()[4].encendido, self.imagePC, self.imageHeight)
       
class sprite_Lamp(anim_Dispositivo):
    def __init__(self, state,screen, location, *groups):
        super(sprite_Lamp, self).__init__(state,screen,location,*groups)
        self.imageLamp = pygame.image.load('sprites/spriteLamp.png')
        self.imageDefaultLamp = self.imageLamp.copy()
        self.rect = pygame.Rect(self.location, (32,64))
        super(sprite_Lamp, self).set_sprite(state, self.imageLamp, self.imageHeight)
        
  
    def update(self, dt, game):
#AQUI CAMBIAR PARA QUE LEA EL VALOR DE INTENSIDAD DEL DISPOSITIVO
        if(game.ambiente.get_dispositivos()[2].encendido):
            valor = 200 - int(game.ambiente.get_dispositivos()[2].get_estado_actual()['intensidad'])
            #print valor
        else:
            valor = 200
            #print "APAGADO Y : ",valor
        game.blackRect.set_alpha(valor)
            
        self.imageLamp = self.imageDefaultLamp.copy()
        super(sprite_Lamp, self).set_sprite(game.ambiente.get_dispositivos()[2].encendido, self.imageLamp, self.imageHeight)
       
class sprite_Radio(anim_Dispositivo):
    def __init__(self, state,screen, location, *groups):
        super(sprite_Radio, self).__init__(state,screen,location,*groups)
        self.imageRadio = pygame.image.load('sprites/spriteRadio.png')
        self.imageDefaultRadio = self.imageRadio.copy()
        self.rect = pygame.Rect(self.location, (128,64))
        super(sprite_Radio, self).set_sprite(state, self.imageRadio, self.imageHeight)

  
    def update(self, dt, game):
        self.imageRadio = self.imageDefaultRadio.copy()
        super(sprite_Radio, self).set_sprite(game.ambiente.get_dispositivos()[3].encendido, self.imageRadio, self.imageHeight)

class sprite_Aire(anim_Dispositivo):
    def __init__(self, state,screen, location, *groups):
        super(sprite_Aire, self).__init__(state,screen,location,*groups)
        self.imageAire = pygame.image.load('sprites/spriteAire.png')
        self.imageDefaultAire = self.imageAire.copy()
        self.rect = pygame.Rect(self.location, (128,64))
        super(sprite_Aire, self).set_sprite(state, self.imageAire, self.imageHeight)

  
    def update(self, dt, game):
        self.imageAire = self.imageDefaultAire.copy()
        super(sprite_Aire, self).set_sprite(game.ambiente.get_dispositivos()[1].encendido, self.imageAire, self.imageHeight)