#Memorygame pictures from http://www.clker.com
import pygame
import random
import os

from pygame.constants import WINDOWEVENT_HIDDEN

class Card:
    def __init__(self, pos: int, pos2: int, picListIndex: int):
        self.pos = pos
        self.pos2 = pos2
        self.picListIndex = picListIndex
        self.f = False

class Button:
    def __init__(self, text: str, posX: int, posY: int, width: int, height: int):
        self.text = text
        self.posX = posX
        self.posY = posY
        self.width = width
        self.height = height

class MemoryGame:
    def __init__(self):
        pygame.init() #initializing the constructor
        self.width, self.height = 385, 200 #initial screen size -> screen is resized during the game
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        pygame.display.set_caption('The Flippery Flip Memory Game')
        pygame.display.flip()
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("coolveticarg", 25)
        self.numOfPairs = {" 3":[3, [268, 184]]," 8":[8, [352, 352]], "10":[10, [436, 352]], "15":[15, [520, 436]], "18":[18, [520, 520]], "21":[21, [604, 520]], "28":[28, [688, 604]], "32":[32, [688, 688]]}
        self.xMouse, self.yMouse = 0, 0
        self.status = "new" #"1st card" "2nd card" "OK" "end"
        self.pairs = 0
        self.cardOneFieldIndex = 64
        self.cardTwoFieldIndex = 64
        self.newGameButton = Button("NEW GAME", 40, self.height/2-5, 134, 35)
        self.endButton = Button("END", 40, self.height-45, 55, 35)

        self.picturesAll = [] #all pictures from pictures directory
        self.picList = [] #selected pictures from picturesAll
        self.picsReady = [] #cards that have been found
        self.gameBoard = [] #all card items
        self.gameField = [[10,10],[94,10],[178,10],[10,94],[94,94],[178,94],[262,10],[262,94],[10,178],[94,178],[178,178],[262,178],[10,262],[94,262],[178,262],[262,262],[346,10],[346,94],[346,178],[346,262],[10,346],[94,346],[178,346],[262,346],[346,346],[430,10],[430,94],[430,178],[430,262],[430,346],[10,430],[94,430],[178,430],[262,430],[346,430],[430,430],[514,10],[514,94],[514,178],[514,262],[514,346],[514,430],[10,514],[94,514],[178,514],[262,514],[346,514],[430,514],[514,514],[598,10],[598,94],[598,178],[598,262],[598,346],[598,430],[598,514],[10,598],[94,598],[178,598],[262,598],[346,598],[430,598],[514,598],[598,598],[1000,1000]] #contains position coordinates
        self.scoreBoard = [0,0] #pairs, flips

        self.loadPictures()
        self.newGame()
        print(pygame.font.get_fonts())

        while True: #while the game runs:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.xMouse = pygame.mouse.get_pos()[0]
                    self.yMouse = pygame.mouse.get_pos()[1]
                    if self.status != "new":
                        if self.status == "1st card":
                            self.status = "2nd card"
                            self.cardOneFieldIndex = self.detectMauseXY(self.xMouse, self.yMouse) #index from 0 to number of pairs -1
                            self.refresh()
                        elif self.status == "2nd card":
                            self.cardTwoFieldIndex = self.detectMauseXY(self.xMouse, self.yMouse) #index from 0 to number of pairs -1
                            self.refresh()
                        elif self.status == "OK":
                            self.cardOneFieldIndex, self.cardTwoFieldIndex = 64, 64
                            self.status = "1st card"
                            self.refresh()
                        elif self.status == "end":
                            self.choice(self.xMouse, self.yMouse)
                    elif self.status == "new":  #once, at the beginning of a new game
                        self.selectPictures(self.xMouse, self.yMouse)

            if len(self.picsReady)/2 == len(self.picList) and self.status != "new" and self.status != "end":
                self.status = "end"
                self.gameEnd() #8


    # 9 END OR CONTINUE = RESET & NEWGAME
    def choice(self, x, y):
        if y >= self.endButton.posY and y <= self.endButton.posY+35:
            if x >= self.endButton.posX and x <= self.endButton.posX+55:
                exit()    
        elif y >= self.newGameButton.posY and y <= self.newGameButton.posY+35:
            if x >= self.newGameButton.posX and x <= self.newGameButton.posX+134:
                self.xMouse, self.yMouse = 0, 0
                self.status = "new"
                self.pairs = 0
                self.cardOneFieldIndex = 64
                self.cardTwoFieldIndex = 64
                self.picList.clear()
                self.picsReady.clear()
                self.gameBoard.clear()
                self.scoreBoard = [0,0]
                self.width, self.height = 385, 200 #back to initial screen size
                self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
                self.newGame()


    # 8 ALL PAIRS HAVE BEEN FOUND, DISPLAY
    def gameEnd(self):
        self.width, self.height = 385, 200
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        self.screen.fill((0,120,90))
        textSurface = self.font.render("VICTORY", True, (255, 255, 0))
        textRect = textSurface.get_rect()
        textRect.center = ((self.width/2), 20)
        self.screen.blit(textSurface, textRect)

        score = "You found all " + str(self.scoreBoard[0]) + " pairs in " + str(self.scoreBoard[1]) + " flips"
        textSurface = self.font.render(score, True, (255, 255, 0))
        textRect = textSurface.get_rect()
        textRect.center = ((self.width/2), 50)
        self.screen.blit(textSurface, textRect)

        buttonRender = self.font.render(self.newGameButton.text, True, (255, 255, 0))
        pygame.draw.rect(self.screen, (0, 102, 204), (self.newGameButton.posX-1, self.newGameButton.posY-1, self.newGameButton.width+1, self.newGameButton.height+1))
        pygame.draw.rect(self.screen, (0, 90, 120), (self.newGameButton.posX, self.newGameButton.posY, self.newGameButton.width, self.newGameButton.height))
        self.screen.blit(buttonRender, (45, self.height/2-4))

        buttonRender = self.font.render(self.endButton.text, True, (255, 255, 0))
        pygame.draw.rect(self.screen, (0, 102, 204), (self.endButton.posX-1, self.endButton.posY-1, self.endButton.width+1, self.endButton.height+1))
        pygame.draw.rect(self.screen, (0, 90, 120), (self.endButton.posX, self.endButton.posY, self.endButton.width, self.endButton.height))
        self.screen.blit(buttonRender, (45, self.height-44))
        pygame.display.flip()
        return


    # 7 -> 6. REFRESH THE DISPLAY AFTER A MOUSE CLICK (AFTER THE BOARD HAS BEEN ARRANGED)
    def refresh(self):
        self.screen.fill((0,0,0))
        textToPrint = "Select a card"
        card1, card2 = self.cardOneFieldIndex, self.cardTwoFieldIndex  #index from 0 to number of pairs -1
        for i in range(self.pairs *2): #Draw the "backsides" of all cards
            if i not in self.picsReady:
                pygame.draw.rect(self.screen, (0, 120, 90), (self.gameField[i][0], self.gameField[i][1], 80, 80))
        for card in self.gameBoard: #for the first card...
            if card.pos == card1 or card.pos2 == card1:
                if card1 not in self.picsReady:
                    pygame.draw.rect(self.screen, (255, 255, 255), (self.gameField[card1][0], self.gameField[card1][1], 80, 80))
                    self.screen.blit(self.picturesAll[card.picListIndex], (self.gameField[card1][0], self.gameField[card1][1]))
                    pic1 = self.picturesAll[card.picListIndex]
                    break
        for card in self.gameBoard:
            if card.pos == card2 or card.pos2 == card2:
                if card1 == card2:
                    return
                if card2 not in self.picsReady:
                    pygame.draw.rect(self.screen, (255, 255, 255), (self.gameField[card2][0], self.gameField[card2][1], 80, 80))
                    self.screen.blit(self.picturesAll[card.picListIndex], (self.gameField[card2][0], self.gameField[card2][1]))
                    pic2 = self.picturesAll[card.picListIndex]
                    try:
                        if pic1 == pic2:
                            self.scoreBoard[0] += 1
                            self.scoreBoard[1] += 1
                            self.picsReady.append(card1)
                            self.picsReady.append(card2)
                            textToPrint = "YOU FIND A PAIR!"
                        else:
                            self.scoreBoard[1] += 1
                            textToPrint = "Not a pair..."
                        pygame.draw.rect(self.screen, (0, 102, 204), (self.okButton.posX-1, self.okButton.posY-1, self.okButton.width+1, self.okButton.height+1))
                        pygame.draw.rect(self.screen, (0, 90, 120), (self.okButton.posX, self.okButton.posY, self.okButton.width, self.okButton.height))
                        buttonRender = self.font.render(self.okButton.text, True, (255, 255, 0))
                        self.screen.blit(buttonRender, (self.okButton.posX +1, self.okButton.posY))
                        self.status = "OK"
                    except (UnboundLocalError):
                        self.status = "1st card"
                        pass
                break
        textRender = self.font.render(textToPrint, True, (0, 255, 0))
        self.screen.blit(textRender, (10, self.height -37))
        pygame.display.flip()


    # 6 -> 7. WHILE THE GAME RUNS, RETURN SELECTED FIELD
    def detectMauseXY(self, x: int, y: int):
        if x >= 10 and x <= self.width - 10:
            if y >= 10 and y <= self.height - 40:
                for field in self.gameField:
                    if field[0] <= x and field[0]+80 >= x:
                        if field[1] <= y and field[1] + 80 >= y:
                            self.xMouse, self.yMouse = 0, 0 #return mause coordinates to 0, so they don't interfere with the game
                            return (self.gameField.index(field))


    # 5. CREATE CARD OBJECTS BASED ON PICTURES AND NUMBERS AND APPEND THEM TO A LIST self.gameBoard[], THE WINDOW IS REZISED
    def arrangeBoard(self, numbers: list):
        random.shuffle(numbers)
        index = 0
        for pictureIndex in self.picList: 
            self.gameBoard.append(Card(numbers[index], numbers[index+1], pictureIndex))
            index += 2
        for val in self.numOfPairs.values(): # adjust the screen size based on number of cards in play
            if val[0] == len(self.picList):
                self.width = val[1][0]
                self.height = val[1][1] + 40               
                self.okButton = Button("OK", self.width - 50, self.height - 36, 35, 30)
                self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        self.xMouse, self.yMouse = 0, 0 #return mause coordinates to 0, so they don't interfere with the game
        self.refresh()
        self.status = "1st card"


    # 3. FUNCTION GET MOUSE COORDINATES AND DETERMINES THE NUMBER OF PAIRS TO BE PLAYED 
    # AND THE PICTURES ARE RANDOMLY SELECTED FROM self.picturesAll[]
    def selectPictures(self, x: int, y: int):
        if y >= 50 and y <= 84:
            for val in self.numOfPairs.values():
                if val[2] <= x and val[2]+34 >= x:
                    self.pairs = val[0]
                    break
        else:        
            return
        self.xMouse, self.yMouse = 0, 0 #return mause coordinates to 0, so they don't interfere with the game
        if self.pairs != 0:
            if len(self.picturesAll) > 0:
                self.picList = random.sample(range(40), self.pairs)
                numbers = self.createList(0, self.pairs) 
                self.arrangeBoard(numbers)
                self.status = "1st card"
                return
            else:
                self.pairs = 0
                return
        else:
            self.pairs = 0
            return


    # 2. AT THE BEGINNING OF THE GAME, SELECT THE NUMBER OF PAIRS YOU WANT TO PLAY BY MOUSE CLICK
    def newGame(self):
        self.screen.fill((0,120,90))
        textStart = self.font.render("CHOOSE THE NUMBER OF PAIRS!", True, (255, 255, 0))
        self.screen.blit(textStart, (18, 10))
        x, y = 12, 50
        for choice in self.numOfPairs:
            textNOP = self.font.render(choice, True, (0, 0, 0))
            self.numOfPairs[choice].append(x)
            pygame.draw.rect(self.screen, (160, 160, 160), (x, y, 34, 34))
            pygame.draw.rect(self.screen, (200, 200, 200), (x+1, y+1, 32, 32))
            self.screen.blit(textNOP, (x + 6, y + 2))
            x += 46
        pygame.display.flip()
        return


    # 1. PICTURES ARE LOADED AT THE BEGINNING OF THE PROGRAM
    def loadPictures(self):
        for filename in os.listdir("pictures"):
            if filename.endswith(".png"):
                self.picturesAll.append(pygame.image.load("pictures/" + filename))
                continue
            else:
                continue


    # 4. CREATES A LIST OF NUMBERS IN A SELECTED RANGE
    def createList(self, r1, r2):
        return list(range(r1, (r2 * 2))) 


if __name__ == "__main__":
    MemoryGame()

