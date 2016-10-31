from math import sqrt
from sets import Set

import pygame
from pygame.locals import *


tileSize               = 16

heroWalkingSpriteTempo = 4
heroWalkingSpeed       = 2
heroAttackSpriteTempo  = 2

ennemyWalkingSpeed     = 0.5
ennemyKnockBack        = 6



def distance(pos1, pos2) :
    
    dx = pos1[0] - pos2[0]
    dy = pos1[1] - pos2[1]

    return sqrt(dx*dx+dy*dy)

def directionToVector(d, mag) :

    if (d == "back" ) or (d == "up"  ) : return (0, -mag)
    if (d == "front") or (d == "down") : return (0, +mag)
    if (d == "left" ) :                  return (-mag, 0)
    if (d == "right") :                  return (+mag, 0)

    return (0,0)

def isWalkable(source, pos, ignoreEnnemies = False, ignoreList = [ ]) :

    if not (map.isWalkable(pos)) : 
        return False

    if ((source != hero) 
    and (hero not in ignoreList)
    and (distance(hero.position(), pos) < tileSize)) : 
        return False 
    
    if not (ignoreEnnemies) :
        for ennemy in ennemies :
            if  ((source != ennemy)
            and  (ennemy not in ignoreList)
            and  (distance(ennemy.position(), pos) < tileSize)) : 
                return False

    return True

class Damage() :

    def __init__(self, source, position, radius, value) :
    
        self.source   = source
        self.position = position
        self.radius   = radius
        self.value    = value

    def makeDamageText(self, insideColor = (255,255,255), outsideColor=(0,0,0)) :

        textIn   = damageFont.render(str(self.value), 1, insideColor )
        textOut  = damageFont.render(str(self.value), 1, outsideColor)
        size = textIn.get_width() + 2, textIn.get_height() + 2
        s = pygame.Surface(size, pygame.SRCALPHA, 32)
        s.blit(textOut,(0,0))    
        s.blit(textOut,(2,2))    
        s.blit(textOut,(2,0))    
        s.blit(textOut,(0,2))    
        s.blit(textIn, (1,1))    

        return s



projectiles = Set()
ennemies = Set()
