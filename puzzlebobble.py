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
        self.speed = 5
        self.color = COLORLIST[random.randint(0, len(COLORLIST)-1)]
        self.radius = BUBBLERADIUS

    def changePosition(self, degree):
        xmove = xcalculate(degree)
        ymove = ycalculate(degree)

        self.rect.x += xmove
        self.rect.y += ymove

        pygame.draw.circle(DISPLAYSURF, self.color, (self.rect.x, self.rect.y), self.radius) 

    def xcalculate(self, degree):
        radians = math.radians(degree)
        xmoveRadians = math.cos(radians)*(self.speed)
        xmove = math.degrees(xmoveRadians)

        return xmove

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

        arrowImage, arrowRect = self.makeArrow()
        self.image = arrowImage
        self.rect = arrowRect
        self.rect.centerx = DISPLAYRECT.centerx
        self.rect.bottom = DISPLAYRECT.bottom
        self.angle = 0
        self.lastRotate = time.time()


    def makeArrow(self):
        arrowImage  = pygame.image.load('Arrow.jpg')
        arrowImage  = pygame.transform.flip(arrowImage, True, False)
        arrowImage  = pygame.transform.rotate(arrowImage, 90)
        arrowRect   = arrowImage.get_rect()
        arrowWidth  = arrowRect.width / 28
        arrowHeight = arrowRect.height / 28
        arrowImage  = pygame.transform.scale(arrowImage, (arrowWidth, arrowHeight))
        arrowRect   = arrowImage.get_rect()

        return arrowImage, arrowRect


    def drawArrow(self, direction):
        
        if direction == LEFT and self.angle < 90:
            self.angle += 2
            arrowToBlit = self.rotateArrow()
            self.lastRotate = time.time()
        elif direction == RIGHT and self.angle > -90:        
            self.angle -= 2
            arrowToBlit = self.rotateArrow()
            self.lastRotate = time.time()    
        else:
            arrowToBlit = self.rotateArrow()

        DISPLAYSURF.blit(arrowToBlit, self.rect)


    def rotateArrow(self):
        arrowToBlit = pygame.transform.rotate(self.image, self.angle)
        arrowRect = arrowToBlit.get_rect()

        oldWidth = self.rect.width
        newWidth = arrowRect.width
        adjustx = (newWidth - oldWidth) / 2

        oldHeight = self.rect.height
        newHeight = arrowRect.height
        adjusty = (newHeight - oldHeight) / 2 

        arrowRect.centerx = self.rect.centerx
        arrowRect.centery = self.rect.centery 

        self.rect = arrowRect

        return arrowToBlit
        


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

    arrow = Arrow()
    newBubble = Bubble()
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
                    newBubble.getNewBubbleColor()
                elif event.key == K_ESCAPE:
                    terminate()

                       
        arrow.drawArrow(direction)
        newBubble.drawNextBubble()
        drawBubbleArray(bubbleArray)
        
        pygame.display.update()


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
