import pygame
import time
from sys import exit

class App:
    def startGame(self):
        while True:
            lineSpace = 30
            # events
            for event in pygame.event.get():
                # close game event
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                # click game events
                if event.type == pygame.MOUSEBUTTONUP:
                    # restart button event
                    if self.restartBtn.collidepoint(event.pos):
                        # clear lines of text and stop typing
                        for line in range(12):
                            self.messageTxt[line] = self.font.render('', False, self.textColor)
                        self.typing = False
                        self.lineNum = 0
                        self.lineBonus = 0
                        self.writtenText = ''
                    # next line button event                      and if last line isnt already written
                    elif self.nextLineBtn.collidepoint(event.pos) and self.writtenText != self.lines[len(self.lines) - 1]:
                        self.typing = True
                        self.startTime = round(time.time() * 1000)
                        self.writtenText = ''
                        
            self.screen.fill('black')
            #draw game
            self.screen.blit(self.messageColorBox, (30, 30))
            for line in range(12):
                self.screen.blit(self.messageTxt[line], (30 + 20, 20 + lineSpace))
                lineSpace += 30
            self.screen.blit(self.BtnBgColorBox, (75, 432))
            self.screen.blit(self.nextLineTxt, (75 + 20, 432 + 12))
            self.screen.blit(self.BtnBgColorBox, (290, 432))
            self.screen.blit(self.restartTxt, (290 + 20, 432 + 12))
            
            # time letters
            if self.typing:
                if self.lineNum < 12:
                    # repeat until typed every letter on the line
                    if len(self.writtenText) != len(self.lines[self.lineNum + self.lineBonus]):
                        # if delay has happened
                        if self.startTime + self.delay <= round(time.time() * 1000):
                            # add next letter to be typed and if next letter is space add it too
                            self.writtenText = self.writtenText + self.lines[self.lineNum + self.lineBonus][len(self.writtenText)]
                            if len(self.writtenText) < len(self.lines[self.lineNum + self.lineBonus]):
                                if self.lines[self.lineNum + self.lineBonus][len(self.writtenText)] == ' ':
                                    self.writtenText = self.writtenText + self.lines[self.lineNum + self.lineBonus][len(self.writtenText)]
                            # print typed letters
                            self.messageTxt[self.lineNum] = self.font.render(self.writtenText, False, self.textColor)
                            # reset startTime for new delay check
                            self.startTime += self.delay
                    else:
                        if self.lineNum + self.lineBonus != len(self.lines) - 1:
                            self.typing = False
                            self.lineNum += 1
                else:
                    for line in range(11):
                        self.messageTxt[line] = self.font.render(self.lines[line + 1 + self.lineBonus], False, self.textColor)
                    self.lineNum = 11
                    self.lineBonus += 1
                
            # update game 60fps
            pygame.display.update()
            self.clock.tick(60)
                
    def __init__(self):
        super().__init__()
        pygame.init()
        pygame.display.set_caption('message box')
        # set variables
        self.screen = pygame.display.set_mode((500, 500))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('./fonts/Pixeltype.ttf', 35)
        self.textColor = 'forestgreen'
        self.buttonBgColor = 'grey25'
        self.messageTxt = []
        self.lines = []
        self.typing = False
        self.delay = 10
        self.writtenText = ''
        self.lineNum = 0
        self.lineBonus = 0
        charsRemoved = 0
        
        #40 max chars
        # put lines from file into array
        file = open('messages.txt', 'a')
        file = open('messages.txt', 'r')
        for line in file:
            self.lines.append('')
            for char in range(len(line)):
                if line[char] != '\n':
                    self.lines[len(self.lines) - 1] += line[char]
                if len(self.lines[len(self.lines) - 1]) == 40:
                    # if word is longer than 40 characters cut it to the next line
                    if ' ' not in self.lines[len(self.lines) - 1]:
                        print('poob')
                        self.lines.append('')
                    # if everything isnt written already
                    elif len(line) - 1 != char:
                        # if 33rd char is a space or enter                 : go to new line
                        if line[char + 1] == ' ' and line[char + 1] == '\n':
                            self.lines.append('')
                        # if 33rd char is a letter
                        else:
                            # remove last char untill its a space
                            while True:
                                if self.lines[len(self.lines) - 1][len(self.lines[len(self.lines) - 1]) - 1] == ' ':
                                    break
                                else:
                                    self.lines[len(self.lines) - 1] = self.lines[len(self.lines) - 1][:-1]
                                    charsRemoved += 1
                            self.lines.append('')
                            for removedChar in reversed(range(charsRemoved)):
                                self.lines[len(self.lines) - 1] += line[char - removedChar]
                            charsRemoved = 0
        file.close()

        # create everything on screen
        self.BtnBgColorBox = pygame.Surface((135, 45))
        self.BtnBgColorBox.fill(self.buttonBgColor)
        
        self.messageColorBox = pygame.Surface((440, 380))
        self.messageColorBox.fill(self.buttonBgColor)
        for _ in range(12):
            self.messageTxt.append(self.font.render('', False, self.textColor))
        
        self.nextLineTxt = self.font.render('Next Line', False, self.textColor)
        self.nextLineBtn = pygame.Rect(75, 432, 135, 45)
        
        self.restartTxt = self.font.render('Restart', False, self.textColor)
        self.restartBtn = pygame.Rect(290, 432, 135, 45)

        # run game loop
        self.startGame()

if __name__ == "__main__":
    app = App()