import pygame
pygame.init()

screenX,screenY = 500,500
bgcolour = (45,45,45)

screen = pygame.display.set_mode((screenX,screenY))
screen.fill(bgcolour)
clock = pygame.time.Clock()

teamColours = {
    "Enemy" : (255,0,0),
    "Player" : (0,0,255)
    }

def Draw(sprite):
    xPos = sprite.xPos
    yPos = sprite.yPos

    xSize = sprite.xSize
    ySize = sprite.ySize
    
    team = sprite.team

    pygame.draw.rect(screen,teamColours[team],(xPos-(xSize/2),yPos-(ySize/2),xSize,ySize) )

class sprite():
    def __init__(self,xPos,yPos,xSize,ySize,team,hp,dmg,velocity,maxVelocity,acceleration,deceleration):

        self.xPos = xPos
        self.yPos = yPos
        
        self.xSize = xSize
        self.ySize = ySize
        
        self.team = team
        self.hp = hp
        self.dmg = dmg

        self.velocity = velocity
        self.maxVelocity = maxVelocity
        self.acceleration = acceleration

        self.deceleration = deceleration

    def ChangeVelocity(self,axis,mult):
        if axis == "Y":
            mult *= -1

        axis = dict(X=0,Y=1)[axis]
        
        self.velocity[axis] = self.velocity[axis] + (self.acceleration[axis] * mult) #change velocity
        
        self.velocity[axis] = min(self.maxVelocity[axis],max(self.velocity[axis],self.maxVelocity[axis]*-1)) #fit within bounds

    def AprochZeroVelocity(self,axis):

        axis = dict(X=0,Y=1)[axis]
        
        if self.velocity[axis] > 0:
            self.velocity[axis] = max(self.velocity[axis]-self.deceleration[axis],0)#decelerate if travelling right
        elif self.velocity[axis] < 0:
            self.velocity[axis] = min(self.velocity[axis]+self.deceleration[axis],0) #decelerate if travelling left

    def Move(self):
        self.xPos = max(0,min(self.xPos+self.velocity[0],screenX))
        self.yPos = max(0,min(self.yPos+self.velocity[1],screenY))

    
player = sprite(
    xPos = screenX//2,
    yPos = screenY//2,
    xSize = 25,
    ySize = 25,
    velocity = [0,0],
    maxVelocity = [2,2],
    acceleration = [0.5,0.5],
    deceleration = [0.0625,0.0625],
    team = "Player",
    hp = 100,
    dmg = None
    )

enemy = sprite(
    xPos = screenX//2,
    yPos = 50,
    xSize = 50,
    ySize = 25,
    velocity = [0,0],
    maxVelocity = [0,0],
    acceleration = [0,0],
    deceleration = [0,0],
    team = "Enemy",
    hp = 100,
    dmg = None
    )

EntityList = [player,enemy]

run = True
while run:  
    clock.tick(60)
    screen.fill(bgcolour)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                continue
    
    pressedkeys = pygame.key.get_pressed()
    
    if pressedkeys[pygame.K_a]:
        player.ChangeVelocity("X",-1)
    if pressedkeys[pygame.K_d]:
        player.ChangeVelocity("X",+1)
    if ( (not pressedkeys[pygame.K_a]) and (not pressedkeys[pygame.K_d]) ):
        player.AprochZeroVelocity("X")

    if pressedkeys[pygame.K_w]:
        player.ChangeVelocity("Y",+1)
    if pressedkeys[pygame.K_s]:
        player.ChangeVelocity("Y",-1)
    if ( (not pressedkeys[pygame.K_w]) and (not pressedkeys[pygame.K_s]) ):
        player.AprochZeroVelocity("Y")
    

    
    player.Move()
    
    for Entity in EntityList:
        Draw(Entity)
    
    pygame.display.flip()



        
pygame.quit()
quit()
