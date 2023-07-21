import time
import os
import pigpio
import random
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306

dinoA = [0x2]
dinoB = [0x2]
dinoC = [0x2]
treeA = [0x2]
treeB = [0x2]
treeC = [0x2]
birdA = [0x2]
birdB = [0x2]

class player:
    def __init__(self):
        self.x = 18
        self.y = 27
        self.spriteSize = 20
        self.isJump = False
        self._jumpCount = 40 # change current count at jump end
        self._currentCount = 0
        self._jumpDiv = 4
        self._jumpSpeed = 3

    def render(self, draw, bg):
            DINO_1 = "assets/dino_default.png"
            sprite = Image.open(DINO_1).convert("1").resize((self.spriteSize, self.spriteSize))
            bg.paste(sprite, (self.x - (self.spriteSize // 2), self.y - (self.spriteSize // 2)))

    def jump(self):    
        if self.isJump == True: # run if jump flag is set
            if self._currentCount > 0:
                if self._currentCount > (self._jumpCount // 2): # going up
                    self.y -= self._jumpDiv
                else:
                    self.y += self._jumpDiv # going down
                self._currentCount -= self._jumpSpeed
            else:
                self.isJump = False
                self._currentCount = 40

    def dinoJump(self):
        self.isJump = True # set jump flag

class tree:
    def __init__(self):
        self.x = random.randint(128, 256)
        self.y = 37
        self.height = 12
        self.width = 3
        self.speed = 1

    def render(self, draw):
        draw.rectangle(((self.x, self.y - self.height), (self.x + self.width, self.y)), fill="white")

    def move(self):
        if self.x + self.width > 0:
            self.x -= (2 * self.speed)
        else:
            self.x = random.randint(128, 256)

#class bird:

class ground:
    def __init__(self):
        self.width = random.randint(2, 10)
        self.y = random.randint(37, 50)
        self.x = random.randint(128, 256)
        self.speed = 1

    def render(self, draw):
        draw.line(((self.x, self.y), (self.x + self.width, self.y)), fill="white")

    def move(self):
        if self.x + self.width > 0:
            self.x -= (2 * self.speed)
        else:
            self.x = random.randint(128, 256)
            self.y = random.randint(37, 50)
            self.width = random.randint(2, 12)
        
    

def dinoApp(pi, buttons, debounce):

    # font
    FONT_PATH = "fonts/Roboto-Regular.ttf"
    FONT_SIZE = 18
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
        
    # Define the size of the OLED screen
    SCREEN_WIDTH = 128
    SCREEN_HEIGHT = 64
    
    # Initialize the OLED screen
    serial = i2c(port=1, address=0x3C)
    device = ssd1306(serial)

    # Game setup
    player1 = player()
    tree1 = tree()
    ground1 = ground()
    ground2 = ground()
    ground3 = ground()
    ground4 = ground()

    # debounce
    while (pi.read(buttons[4]) == 1):
        pass # do nothing
        
    while (pi.read(buttons[4]) == 0):
        background = Image.new("1", (SCREEN_WIDTH, SCREEN_HEIGHT), "black")
        draw = ImageDraw.Draw(background)

        # Stage
        draw.line(((0, 35),(128, 35)), fill="white")

        if (pi.read(buttons[0]) == 1):
            time.sleep(debounce)
            if (pi.read(buttons[0]) == 1):
                player1.dinoJump()
                
        player1.jump()
        player1.render(draw, background)

        tree1.move()
        tree1.render(draw)

        ground1.move()
        ground2.move()
        ground3.move()
        ground4.move()
        ground1.render(draw)
        ground2.render(draw)
        ground3.render(draw)
        ground4.render(draw)


        device.display(background)
