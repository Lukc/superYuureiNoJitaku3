import pygame
import pygame.locals
import shared

class Hero() :


    def __init__(self, spritePath) :

        self.x = shared.map.width  * shared.tileSize / 2 
        self.y = shared.map.height * shared.tileSize / 2 
       
        self.loadSprites(spritePath)
       
        self.orientation       = "front"
        self.currentSpriteStep = 0
        self.currentSpriteStepTempo = shared.heroWalkingSpriteTempo
        self.busy = False
        
        self.immunityTempo     = -1
        
        self.updateCurrentSprite()
        
    def position(self) :

        return (self.x, self.y)

    def loadSprites(self, path) :

        self.sprites          = {}
        self.sprites["front"] = []
        self.sprites["right"] = []
        self.sprites["left"]  = []
        self.sprites["back"]  = []
        self.sprites["attack-front"] = []
        self.sprites["attack-right"] = []
        self.sprites["attack-left"]  = []
        self.sprites["attack-back"]  = []
        
        spritesImage = pygame.image.load(path)
      
        self.sprites["front"].append(self.getSprite(spritesImage, 0, 0))
        self.sprites["front"].append(self.getSprite(spritesImage, 0, 1))
        self.sprites["left"] .append(self.getSprite(spritesImage, 1, 0))
        self.sprites["left"] .append(self.getSprite(spritesImage, 1, 1))
        self.sprites["back"] .append(self.getSprite(spritesImage, 2, 0))
        self.sprites["back"] .append(self.getSprite(spritesImage, 2, 1))
        self.sprites["right"].append(self.getSprite(spritesImage, 3, 0))
        self.sprites["right"].append(self.getSprite(spritesImage, 3, 1))
 
        self.sprites["attack-front"].append(self.getSprite(spritesImage, 4,  0, 3))
        self.sprites["attack-front"].append(self.getSprite(spritesImage, 4,  3, 3))
        self.sprites["attack-front"].append(self.getSprite(spritesImage, 4,  6, 3))
        self.sprites["attack-left"] .append(self.getSprite(spritesImage, 7,  0, 3))
        self.sprites["attack-left"] .append(self.getSprite(spritesImage, 7,  3, 3))
        self.sprites["attack-left"] .append(self.getSprite(spritesImage, 7,  6, 3))
        self.sprites["attack-back"] .append(self.getSprite(spritesImage, 10, 0, 3))
        self.sprites["attack-back"] .append(self.getSprite(spritesImage, 10, 3, 3))
        self.sprites["attack-back"] .append(self.getSprite(spritesImage, 10, 6, 3))
        self.sprites["attack-right"].append(self.getSprite(spritesImage, 13, 0, 3))
        self.sprites["attack-right"].append(self.getSprite(spritesImage, 13, 3, 3))
        self.sprites["attack-right"].append(self.getSprite(spritesImage, 13, 6, 3))



    def getSprite(self, spritesImage, x, y, s = 1) :
        return spritesImage.subsurface((x * shared.tileSize, y * shared.tileSize,
                                        s * shared.tileSize, s * shared.tileSize))


    def render(self) :
       
        spriteW = self.currentSprite.get_width()
        spriteH = self.currentSprite.get_height()
        
        shared.view.blit(self.currentSprite, (self.x - spriteW/2,  self.y-spriteH/2))


    def look(self, direction) :

        if (self.busy) : 
            return

        self.orientation = direction
        
        self.updateCurrentSprite()

    def move(self, direction) :
        
        if (self.busy) :
            return

        self.look(direction)

        if   (self.orientation == "back" ) : dx, dy =  0, -shared.heroWalkingSpeed
        elif (self.orientation == "front") : dx, dy =  0, +shared.heroWalkingSpeed
        elif (self.orientation == "left" ) : dx, dy = -shared.heroWalkingSpeed, 0
        elif (self.orientation == "right") : dx, dy = +shared.heroWalkingSpeed, 0
        
        if (shared.map.getWalkability(self.x+dx, self.y+dy)) :
            self.x += dx
            self.y += dy

        self.spriteUpdate()

    def attackKeyHandler(self) :

        if (self.busy) :
            return

        self.busy = "attack"
        self.currentSpriteStepTempo = shared.heroAttackSpriteTempo
        self.updateCurrentSprite()
        
    def emmitDamage(self) :


        if (self.busy != "attack") :
            return [ ]

        if   (self.orientation == "back" ) : hittedNeighbour = [ (1, 0), (0.7,-0.7),  ( 0,-1) ][self.currentSpriteStep]
        elif (self.orientation == "front") : hittedNeighbour = [ (-1,0), (-0.7, 0.7), ( 0, 1) ][self.currentSpriteStep]
        elif (self.orientation == "left" ) : hittedNeighbour = [ (0,-1), (-0.7,-0.7), (-1, 0) ][self.currentSpriteStep]
        elif (self.orientation == "right") : hittedNeighbour = [ (0,-1), ( 0.7,-0.7), ( 1, 0) ][self.currentSpriteStep]
        
        hittedPosition = (self.x + hittedNeighbour[0]*shared.tileSize, 
                          self.y + hittedNeighbour[1]*shared.tileSize)

        return [ shared.Damage(source=self, position=hittedPosition,
            radius=shared.tileSize*0.7, value=1) ]



    def receiveDamage(self, damage) :
        
        if (self.immunityTempo >= 0) :
            return

        print "Hero took "+str(damage.value)+" damages !"
        self.immunityTempo = 10




    def update(self) :
   
        if (self.immunityTempo >= 0) :
            self.immunityTempo -= 1

        if (self.busy) :
            self.spriteUpdate()
     
    def spriteUpdate(self) :
        
        self.currentSpriteStepTempo -= 1
        
        if (self.currentSpriteStepTempo >= 0) :
            return
        
        self.currentSpriteStep += 1

        if not (self.busy) :
            self.currentSpriteStepTempo = shared.heroWalkingSpriteTempo
            spriteName = self.orientation
        else :
            self.currentSpriteStepTempo = shared.heroAttackSpriteTempo
            spriteName = self.busy+"-"+self.orientation
        
        if (self.currentSpriteStep >= len(self.sprites[spriteName])) :
            self.currentSpriteStep = 0
        
        if (self.busy) and (self.currentSpriteStep == 0) :
            self.busy = False
        
        self.updateCurrentSprite()

    def updateCurrentSprite(self) :

        if not (self.busy) :
            spriteName = self.orientation
        else :
            spriteName = self.busy+"-"+self.orientation
        
        self.currentSprite = self.sprites[spriteName][self.currentSpriteStep]
