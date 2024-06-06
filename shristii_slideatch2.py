import sys
import os
import pygame
import random

# Add the path to simpleGE.py
sys.path.append(r'C:\Users\Khadka\OneDrive\Documents')

import simpleGE as sg

class Coin(sg.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("astronaut.png")  # Changed from "Coin.png" to "astronaut.png"
        self.setSize(25, 25)
        self.reset()
        
    def reset(self):
        self.y = 10
        self.x = random.randint(0, self.screenWidth)
        self.dy = random.randint(3, 8)
        
    def checkBounds(self):
        if self.bottom > self.screenHeight:
            self.reset()

class Spaceship(sg.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("spaceship.png")
        self.setSize(50, 50)
        self.position = (320, 400)
        self.moveSpeed = 5
    
    def process(self):
        if self.isKeyPressed(pygame.K_LEFT):
            self.x -= self.moveSpeed
        if self.isKeyPressed(pygame.K_RIGHT):
            self.x += self.moveSpeed

class LblScore(sg.Label):
    def __init__(self):
        super().__init__()
        self.text = "Score: 0"
        self.center = (100, 30)
        
class LblTime(sg.Label):
    def __init__(self):
        super().__init__()
        self.text = "Time Left: 10"
        self.center = (500, 30)

class Game(sg.Scene):
    def __init__(self):
        super().__init__()
        self.setImage("background.png")
        
        self.timer = sg.Timer()
        self.timer.totalTime = 10
        self.score = 0
        
        self.sndCoin = sg.Sound("coin.wav")
        
        self.spaceship = Spaceship(self)
        self.coins = []
        for i in range(10):
            self.coins.append(Coin(self))
            
        self.lblScore = LblScore()
        self.lblTime = LblTime()
        
        self.sprites = [self.spaceship,
                        self.coins,
                        self.lblScore, 
                        self.lblTime]
        
    def process(self):
        for coin in self.coins:
            if self.spaceship.collidesWith(coin):
                self.sndCoin.play()
                coin.reset()
                self.score += 1
                self.lblScore.text = f"Score: {self.score}"
                
        self.lblTime.text = f"Time Left: {self.timer.getTimeLeft():.2f}"
        if self.timer.getTimeLeft() < 0:
            print(f"Final Score: {self.score}")
            self.stop()

class Instructions(sg.Scene):
    def __init__(self, score):
        super().__init__()
        self.setImage("background.png")
        
        self.response = "Play"
        
        self.instructions = sg.MultiLabel()
        self.instructions.textLines = [
        "You are in the Spaceship.",
        "Move with the left and right arrow keys",
        "and catch as many astronauts as you can",
        "in only ten seconds",
        "",
        "Good Luck!"]
        
        self.instructions.center = (320, 240)
        self.instructions.size = (500, 250)
        
        self.prevScore = score
        self.lblScore = sg.Label()
        self.lblScore.text = f"Last score: {self.prevScore}"
        self.lblScore.center = (320, 400)
        
        self.btnPlay = sg.Button()
        self.btnPlay.text = "Play (up)"
        self.btnPlay.center = (100, 400)
        
        self.btnQuit = sg.Button()
        self.btnQuit.text = "Quit (down)"
        self.btnQuit.center = (550, 400)
        
        self.sprites = [self.instructions,
                        self.lblScore,
                        self.btnQuit,
                        self.btnPlay]
        
    def process(self):
        if self.btnQuit.clicked:
            self.response = "Quit"
            self.stop()
        if self.btnPlay.clicked:
            self.response = "Play"
            self.stop()

        if self.isKeyPressed(pygame.K_UP):
            self.response = "Play"
            self.stop()
        if self.isKeyPressed(pygame.K_DOWN):
            self.response = "Quit"
            self.stop()

def main():
    keepGoing = True
    score = 0
    while keepGoing:
        instructions = Instructions(score)
        instructions.start()
                
        if instructions.response == "Play":    
            game = Game()
            game.start()
            score = game.score
        else:
            keepGoing = False
    
if __name__ == "__main__":
    main()
