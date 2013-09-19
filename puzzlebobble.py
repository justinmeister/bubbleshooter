import math, pygame, sys, os, copy, time, random
from pygame.locals import *

## Constants, yo ##

FPS          = 30
WINDOWWIDTH  = 640
WINDOWHEIGHT = 480
TEXTHEIGHT   = 20
BUBBLERADIUS = 20
BUBBLEWIDTH  = BUBBLERADIUS * 2
BUBBLELAYERS = 5
BUBBLEYADJUST = 7
STARTX = WINDOWWIDTH / 2
STARTY = WINDOWHEIGHT - 27


RIGHT = 'right'
LEFT  = 'left'
BLANK = '.'

## COLORS ##

#            R    G    B
GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)
BLACK    = (  0,   0,   0)
COMBLUE  = (233, 232, 255)

BGCOLOR    = WHITE
COLORLIST = [RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN]
     

class Bubble(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.rect = pygame.Rect(0, 0, 40, 40)
        self.rect.centerx = STARTX
        self.rect.centery = STARTY + 20
        self.speed = 10
        self.color = COLORLIST[random.randint(0, len(COLORLIST)-1)]
        self.radius = BUBBLERADIUS
        self.angle = 0

    def update(self):

        if self.angle == 90:
            xmove = 0
            ymove = self.speed * -1
        elif self.angle < 90:
            xmove = self.xcalculate(self.angle)
            ymove = self.ycalculate(self.angle)
        elif self.angle > 90:
            xmove = self.xcalculate(180 - self.angle) * -1
            ymove = self.ycalculate(180 - self.angle)
        

        self.rect.x += xmove
        self.rect.y += ymove


    def draw(self):
        pygame.draw.circle(DISPLAYSURF, self.color, (self.rect.x, self.rect.y), self.radius)
        pygame.draw.circle(DISPLAYSURF, GRAY, (self.rect.x, self.rect.y), self.radius, 1)


    def xcalculate(self, angle):
        radians = math.radians(angle)
        
        xmove = math.cos(radians)*(self.speed)
        return xmove

    def ycalculate(self, angle):
        radians = math.radians(angle)
        
        ymove = math.sin(radians)*(self.speed) * -1
        return ymove



    def drawNextBubble(self):
        nextRect = pygame.Rect(0, 0, 40, 40)
        nextRect.bottom = WINDOWHEIGHT
        nextRect.right = WINDOWWIDTH
        circlePos = nextRect.center

        pygame.draw.circle(DISPLAYSURF, self.color, circlePos, BUBBLERADIUS)
        pygame.draw.circle(DISPLAYSURF, GRAY, circlePos, BUBBLERADIUS, 1)

    def getNewBubbleColor(self):
        self.color = COLORLIST[random.randint(0, len(COLORLIST)-1)]



class Arrow(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.angle = 90
        arrowImage = pygame.image.load('Arrow.png')
        arrowRect = arrowImage.get_rect()
        self.image = arrowImage
        self.transformImage = self.image
        self.rect = arrowRect
        self.rect.centerx = STARTX - 20
        self.rect.centery = STARTY
        


    def update(self, direction):
        
        if direction == LEFT and self.angle < 180:
            self.angle += 2
        elif direction == RIGHT and self.angle > 0:        
            self.angle -= 2

        self.transformImage = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.transformImage.get_rect()
        self.rect.centerx = STARTX - 20
        self.rect.centery = STARTY

        
    def draw(self):
        DISPLAYSURF.blit(self.transformImage, self.rect)
        


def main():
    global FPSCLOCK, DISPLAYSURF, DISPLAYRECT, MAINFONT
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Puzzle Bobble')
    MAINFONT = pygame.font.SysFont('Helvetica', TEXTHEIGHT)
    DISPLAYSURF, DISPLAYRECT = makeDisplay()
    

    while True:
        runGame()
        


def runGame():
    direction = None
    launchBubble = False

    arrow = Arrow()
    newBubble = None
    bubbleArray = makeBubbleArray()
    
    

    while True:
        DISPLAYSURF.fill(BGCOLOR)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
                
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT):
                    direction = LEFT
                elif (event.key == K_RIGHT):
                    direction = RIGHT
                    
            elif event.type == KEYUP:
                direction = None
                if event.key == K_SPACE:
                    launchBubble = True
                elif event.key == K_ESCAPE:
                    terminate()

        if launchBubble == True:
            if newBubble == None:
                newBubble = Bubble()
                newBubble.angle = arrow.angle

            newBubble.update()
            newBubble.draw()
            
            if newBubble.rect.y < 0:
                newBubble = None
                launchBubble = False
            elif newBubble.rect.right >= WINDOWWIDTH + 22:
                newBubble.angle = 180 - newBubble.angle
            elif newBubble.rect.left <= 18:
                newBubble.angle = 180 - newBubble.angle
            

        arrow.update(direction)
        arrow.draw()
        
        drawBubbleArray(bubbleArray)
        pygame.display.update()

        
    


def showNextBubble(color):
    nextRect = pygame.Rect(0, 0, 40, 40)
    nextRect.bottom = WINDOWHEIGHT
    nextRect.right = WINDOWWIDTH
    circlePos = nextRect.center

    pygame.draw.circle(DISPLAYSURF, color, circlePos, BUBBLERADIUS)
    pygame.draw.circle(DISPLAYSURF, GRAY, circlePos, BUBBLERADIUS, 1)


def makeBubbleArray():
    bubbleArray = []
    for row in range(BUBBLELAYERS):
        collumn = []
        for i in range(16):
            newBubble = Bubble()
            collumn.append(newBubble)
        bubbleArray.append(collumn)

    setArrayPos(bubbleArray)

    return bubbleArray


def setArrayPos(bubbleArray):
    for row in range(len(bubbleArray)):
        for column in range(len(bubbleArray[row])):
            bubbleArray[row][column].rect.x = (BUBBLEWIDTH * column)
            bubbleArray[row][column].rect.y = (BUBBLEWIDTH * row)

    for row in range(1, len(bubbleArray), 2):
        for column in range(len(bubbleArray[row])):
              bubbleArray[row][column].rect.x += BUBBLERADIUS

    for row in range(1, len(bubbleArray)):
        for column in range(len(bubbleArray[row])):
            bubbleArray[row][column].rect.y -= BUBBLEYADJUST * row

    deleteExtraBubbles(bubbleArray)


def deleteExtraBubbles(bubbleArray):
    for row in range(len(bubbleArray)):
        for column in range(len(bubbleArray[row])):
            if bubbleArray[row][column].rect.right > WINDOWWIDTH:
                del bubbleArray[row][column]
            


def drawBubbleArray(bubbleArray):
    for row in range(len(bubbleArray)):
        for column in range(len(bubbleArray[row])):
            bubble = bubbleArray[row][column]

            pygame.draw.circle(DISPLAYSURF, bubble.color, bubble.rect.center, BUBBLERADIUS)
            pygame.draw.circle(DISPLAYSURF, GRAY, bubble.rect.center, BUBBLERADIUS, 1)
            


def makeDisplay():
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    DISPLAYRECT = DISPLAYSURF.get_rect()
    DISPLAYSURF.fill(BGCOLOR)
    DISPLAYSURF.convert()
    pygame.display.update()

    return DISPLAYSURF, DISPLAYRECT
    
 
def terminate():
    pygame.quit()
    sys.exit()
        
        
        
if __name__ == '__main__':
    main()
