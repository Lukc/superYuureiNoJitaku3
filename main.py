
import shared as s
import tileset, map, view, game, hero, ennemy, combatManager, visionManager
import pygame
from pygame.locals import *


from combatManager import CombatManager
from visionManager import VisionManager

def main() :

    s.tileset       = tileset.Tileset("assets/tileset.png", "assets/tileset_mask.png");
    
    s.view          = view.View("Test", (20,20))
    
    s.combatManager = combatManager.CombatManager()
    s.visionManager = visionManager.VisionManager()

    s.map           = map.Map("assets/map.json")
    s.hero          = hero.Hero("assets/hero.png")
    
    s.ennemies.add(ennemy.Ennemy((40,40)))
    s.ennemies.add(ennemy.Ennemy((100,30)))
    
    
    g               = game.Game()
        
    s.damageFont    = pygame.font.Font("./assets/bitdust2.ttf",14)
    
    while True :
        g.mainLoop()

main()
