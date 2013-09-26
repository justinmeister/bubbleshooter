import math, pygame, sys, os, copy, time, random
from pygame.locals import *

## Constants, yo ##

FPS          = 60
WINDOWWIDTH  = 640
WINDOWHEIGHT = 480
TEXTHEIGHT   = 20
BUBBLERADIUS = 20
BUBBLEWIDTH  = BUBBLERADIUS * 2
BUBBLELAYERS = 5
BUBBLEYADJUST = 7
STARTX = WINDOWWIDTH / 2
STARTY = WINDOWHEIGHT - 27
ARRAYWIDTH = 16
ARRAYHEIGHT = 14


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
    def __init__(self, color, row=0, column=0):
        pygame.sprite.Sprite.__init__(self)

        self.rect = pygame.Rect(0, 0, 30, 30)
        self.rect.centerx = STARTX
        self.rect.centery = STARTY
        self.speed = 10
        self.color = color
        self.radius = BUBBLERADIUS
        self.angle = 0
        self.row = row
        self.column = column
        
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
        pygame.draw.circle(DISPLAYSURF, self.color, (self.rect.centerx, self.rect.centery), self.radius)
        pygame.draw.circle(DISPLAYSURF, GRAY, (self.rect.centerx, self.rect.centery), self.radius, 1)


    def xcalculate(self, angle):
        radians = math.radians(angle)
        
        xmove = math.cos(radians)*(self.speed)
        return xmove

    def ycalculate(self, angle):
        radians = math.radians(angle)
        
        ymove = math.sin(radians)*(self.speed) * -1
        return ymove





class Arrow(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.angle = 90
        arrowImage = pygame.image.load('Arrow.png')
        arrowRect = arrowImage.get_rect()
        self.image = arrowImage
        self.transformImage = self.image
        self.rect = arrowRect
        self.rect.centerx = STARTX
        self.rect.centery = STARTY
        


    def update(self, direction):
        
        if direction == LEFT and self.angle < 180:
            self.angle += 2
        elif direction == RIGHT and self.angle > 0:        
            self.angle -= 2

        self.transformImage = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.transformImage.get_rect()
        self.rect.centerx = STARTX
        self.rect.centery = STARTY

        
    def draw(self):
        DISPLAYSURF.blit(self.transformImage, self.rect)


class Score(object):
    def __init__(self):
        self.total = 0
        self.font = pygame.font.SysFont('Helvetica', 15)
        self.render = self.font.render('Score: ' + str(self.total), True, BLACK, WHITE)
        self.rect = self.render.get_rect()
        self.rect.left = 5
        self.rect.bottom = WINDOWHEIGHT - 5
        
        
    def update(self, deleteList):
        self.total += ((len(deleteList)) * 10)
        self.render = self.font.render('Score: ' + str(self.total), True, BLACK, WHITE)

    def draw(self):
        DISPLAYSURF.blit(self.render, self.rect)
        
        


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
    newBubble = None
    
    arrow = Arrow()
    arrowTop = arrow.rect.top
    bubbleArray = makeBubbleArray()
    
    nextBubble = Bubble(getRandomColor())
    nextBubble.rect.right = WINDOWWIDTH - 5
    nextBubble.rect.bottom = WINDOWHEIGHT - 5

    score = Score()
    
   
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
                newBubble = Bubble(nextBubble.color)
                newBubble.angle = arrow.angle

            newBubble.update()
            newBubble.draw()
            
            
            if newBubble.rect.right >= WINDOWWIDTH - 5:
                newBubble.angle = 180 - newBubble.angle
            elif newBubble.rect.left <= 5:
                newBubble.angle = 180 - newBubble.angle


            launchBubble, newBubble, score = stopBubble(bubbleArray, newBubble, launchBubble, score)

                            
            if launchBubble == False:
                nextBubble = Bubble(getRandomColor())
                nextBubble.rect.right = WINDOWWIDTH - 5
                nextBubble.rect.bottom = WINDOWHEIGHT - 5
                            
        nextBubble.draw()
        
        arrow.update(direction)
        arrow.draw()
        
        setArrayPos(bubbleArray)
        drawBubbleArray(bubbleArray)

        score.draw()
        
        pygame.display.update()
        FPSCLOCK.tick(FPS)



def stopBubble(bubbleArray, newBubble, launchBubble, score):
    deleteList = []
    
    for row in range(len(bubbleArray)):
        for column in range(len(bubbleArray[row])):
            
            if (bubbleArray[row][column] != BLANK and newBubble != None):
                if (pygame.sprite.collide_rect(newBubble, bubbleArray[row][column])) or newBubble.rect.top < 0:
                    if newBubble.rect.top < 0:
                        newRow, newColumn = addBubbleToTop(bubbleArray, newBubble)
                        
                    elif newBubble.rect.centery >= bubbleArray[row][column].rect.centery:

                        if newBubble.rect.centerx >= bubbleArray[row][column].rect.centerx:
                            if row == 0 or (row) % 2 == 0:
                                newRow = row + 1
                                newColumn = column
                                if bubbleArray[newRow][newColumn] != BLANK:
                                    newRow = newRow - 1
                                bubbleArray[newRow][newColumn] = copy.copy(newBubble)
                                bubbleArray[newRow][newColumn].row = newRow
                                bubbleArray[newRow][newColumn].column = newColumn
                                
                            else:
                                newRow = row + 1
                                newColumn = column + 1
                                if bubbleArray[newRow][newColumn] != BLANK:
                                    newRow = newRow - 1
                                bubbleArray[newRow][newColumn] = copy.copy(newBubble)
                                bubbleArray[newRow][newColumn].row = newRow
                                bubbleArray[newRow][newColumn].column = newColumn
                                                    
                        elif newBubble.rect.centerx < bubbleArray[row][column].rect.centerx:
                            if row == 0 or row % 2 == 0:
                                newRow = row + 1
                                newColumn = column - 1
                                if bubbleArray[newRow][newColumn] != BLANK:
                                    newRow = newRow - 1
                                bubbleArray[newRow][newColumn] = copy.copy(newBubble)
                                bubbleArray[newRow][newColumn].row = newRow
                                bubbleArray[newRow][newColumn].column = newColumn
                            else:
                                newRow = row + 1
                                newColumn = column
                                if bubbleArray[newRow][newColumn] != BLANK:
                                    newRow = newRow - 1
                                bubbleArray[newRow][newColumn] = copy.copy(newBubble)
                                bubbleArray[newRow][newColumn].row = newRow
                                bubbleArray[newRow][newColumn].column = newColumn
                                
                            
                    elif newBubble.rect.centery < bubbleArray[row][column].rect.centery:
                        if newBubble.rect.centerx >= bubbleArray[row][column].rect.centerx:
                            if row == 0 or row % 2 == 0:
                                newRow = row - 1
                                newColumn = column
                                if bubbleArray[newRow][newColumn] != BLANK:
                                    newRow = newRow + 1
                                bubbleArray[newRow][newColumn] = copy.copy(newBubble)
                                bubbleArray[newRow][newColumn].row = newRow
                                bubbleArray[newRow][newColumn].column = newColumn
                            else:
                                newRow = row - 1
                                newColumn = column + 1
                                if bubbleArray[newRow][newColumn] != BLANK:
                                    newRow = newRow + 1
                                bubbleArray[newRow][newColumn] = copy.copy(newBubble)
                                bubbleArray[newRow][newColumn].row = newRow
                                bubbleArray[newRow][newColumn].column = newColumn
                            
                        elif newBubble.rect.centerx <= bubbleArray[row][column].rect.centerx:
                            if row == 0 or row % 2 == 0:
                                newRow = row - 1
                                newColumn = column - 1
                                if bubbleArray[newRow][newColumn] != BLANK:
                                    newRow = newRow + 1
                                bubbleArray[newRow][newColumn] = copy.copy(newBubble)
                                bubbleArray[newRow][newColumn].row = newRow
                                bubbleArray[newRow][newColumn].column = newColumn
                                
                            else:
                                newRow = row - 1
                                newColumn = column
                                if bubbleArray[newRow][newColumn] != BLANK:
                                    newRow = newRow + 1
                                bubbleArray[newRow][newColumn] = copy.copy(newBubble)
                                bubbleArray[newRow][newColumn].row = newRow
                                bubbleArray[newRow][newColumn].column = newColumn


                    popBubbles(bubbleArray, newRow, newColumn, newBubble.color, deleteList)
                    
                    if len(deleteList) >= 3:
                        for pos in deleteList:
                            row = pos[0]
                            column = pos[1]
                            bubbleArray[row][column] = BLANK
                        score.update(deleteList)

                    launchBubble = False
                    newBubble = None

    return launchBubble, newBubble, score

                    

def addBubbleToTop(bubbleArray, bubble):
    posx = bubble.rect.centerx
    leftSidex = posx - BUBBLERADIUS

    columnDivision = math.modf(float(leftSidex) / float(BUBBLEWIDTH))
    column = int(columnDivision[1])
    print columnDivision[0]

    if columnDivision[0] < 0.5:
        bubbleArray[0][column] = copy.copy(bubble)
    else:
        column += 1
        bubbleArray[0][column] = copy.copy(bubble)

    row = 0
    

    return row, column
    
    


def popBubbles(bubbleArray, row, column, color, deleteList):
    if row < 0 or column < 0 or row > (len(bubbleArray)-1) or column > (len(bubbleArray[0])-1):
        return

    elif bubbleArray[row][column] == BLANK:
        return
    
    elif bubbleArray[row][column].color != color:
        return

    for bubble in deleteList:
        if bubbleArray[bubble[0]][bubble[1]] == bubbleArray[row][column]:
            return

    deleteList.append((row, column))

    if row == 0:
        popBubbles(bubbleArray, row,     column - 1, color, deleteList)
        popBubbles(bubbleArray, row,     column + 1, color, deleteList)
        popBubbles(bubbleArray, row + 1, column,     color, deleteList)
        popBubbles(bubbleArray, row + 1, column - 1, color, deleteList)

    elif row % 2 == 0:
        
        popBubbles(bubbleArray, row + 1, column,         color, deleteList)
        popBubbles(bubbleArray, row + 1, column - 1,     color, deleteList)
        popBubbles(bubbleArray, row - 1, column,         color, deleteList)
        popBubbles(bubbleArray, row - 1, column - 1,     color, deleteList)
        popBubbles(bubbleArray, row,     column + 1,     color, deleteList)
        popBubbles(bubbleArray, row,     column - 1,     color, deleteList)

    else:
        popBubbles(bubbleArray, row - 1, column,     color, deleteList)
        popBubbles(bubbleArray, row - 1, column + 1, color, deleteList)
        popBubbles(bubbleArray, row + 1, column,     color, deleteList)
        popBubbles(bubbleArray, row + 1, column + 1, color, deleteList)
        popBubbles(bubbleArray, row,     column + 1, color, deleteList)
        popBubbles(bubbleArray, row,     column - 1, color, deleteList)



def makeBubbleArray():
    bubbleArray = []

    for row in range(ARRAYHEIGHT):
        column = []
        for i in range(ARRAYWIDTH):
            column.append(BLANK)
        bubbleArray.append(column)

    for row in range(BUBBLELAYERS):
        for column in range(len(bubbleArray[row])):
            newBubble = Bubble(getRandomColor(), row, column)
            bubbleArray[row][column] = newBubble 
            
    setArrayPos(bubbleArray)
    return bubbleArray



def setArrayPos(bubbleArray):
    for row in range(ARRAYHEIGHT):
        for column in range(len(bubbleArray[row])):
            if bubbleArray[row][column] != BLANK:
                bubbleArray[row][column].rect.x = (BUBBLEWIDTH * column) + 5
                bubbleArray[row][column].rect.y = (BUBBLEWIDTH * row) + 5

    for row in range(1, ARRAYHEIGHT, 2):
        for column in range(len(bubbleArray[row])):
            if bubbleArray[row][column] != BLANK:
                bubbleArray[row][column].rect.x += BUBBLERADIUS

    for row in range(1, ARRAYHEIGHT):
        for column in range(len(bubbleArray[row])):
            if bubbleArray[row][column] != BLANK:
                bubbleArray[row][column].rect.y -= BUBBLEYADJUST * row

    deleteExtraBubbles(bubbleArray)



def deleteExtraBubbles(bubbleArray):
    for row in range(ARRAYHEIGHT):
        for column in range(len(bubbleArray[row])):
            if bubbleArray[row][column] != BLANK:
                if bubbleArray[row][column].rect.right > WINDOWWIDTH:
                    bubbleArray[row][column] = BLANK
            


def drawBubbleArray(bubbleArray):
    for row in range(ARRAYHEIGHT):
        for column in range(len(bubbleArray[row])):
            if bubbleArray[row][column] != BLANK:
                bubble = bubbleArray[row][column]
                pygame.draw.circle(DISPLAYSURF, bubble.color, bubble.rect.center, BUBBLERADIUS)
                pygame.draw.circle(DISPLAYSURF, GRAY, bubble.rect.center, BUBBLERADIUS, 1)



def getRandomColor():
    return COLORLIST[random.randint(0, len(COLORLIST)-1)]

                    

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
