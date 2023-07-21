import time
import os
import pigpio
import random
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306



class Ball:
    def __init__(self, device):
        self.device = device
        self.x = self.device.width // 2
        self.y = self.device.height // 2
        self.radius = 2
        self.speed_x = random.choice([-2, 2])
        self.speed_y = random.choice([-2, 2])
        self.gameOver = False
        
    def move(self, p1, p2):
        self.x += self.speed_x
        self.y += self.speed_y
        
        if self.y - self.radius <= 0 or self.y + self.radius >= self.device.height:
            self.speed_y *= -1

        p1Range = range(p1.y, p1.y + p1.height)
        p2Range = range(p2.y, p2.y + p2.height)

        if (self.x <= 6) and (self.y in p1Range):
            p1.score += 1
            self.speed_x *= -1
        elif (self.x >= (self.device.width - 6)) and (self.y in p2Range):
            p2.score += 1
            self.speed_x *= -1
        #else:
        #  self.gameOver = True
            
        
    def draw(self, draw):
        draw.ellipse((self.x - self.radius, self.y - self.radius, self.x + self.radius, self.y + self.radius), fill="white")
        
        

class Player:
    def __init__(self, device,  x):
        self.device = device
        self.x = x
        self.y = self.device.height // 2 - 5
        self.width = 2
        self.height = 15
        self.score = 0
        
    def move_up(self):
        self.y = max(0, self.y - 2)
        
    def move_down(self):
        self.y = min(self.device.height - self.height, self.y + 2)
        
    def draw(self, draw):
        draw.rectangle((self.x, self.y, self.x + self.width, self.y + self.height), fill="white")

    def aiAssist(self, ball):
        self.y = ball.y - (self.height // 2)
        

          

def pongApp(pi, buttons, debounce):

    # font
    FONT_PATH = "fonts/Roboto-Regular.ttf"
    FONT_SIZE = 12
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
        
    # Define the size of the OLED screen
    SCREEN_WIDTH = 128
    SCREEN_HEIGHT = 64
    
    # Initialize the OLED screen
    serial = i2c(port=1, address=0x3C)
    device = ssd1306(serial)

    # Game setup
    ball = Ball(device)
    player1 = Player(device, 4)
    player2 = Player(device, device.width - 6)

    # debounce
    while (pi.read(buttons[4]) == 1):
        pass # do nothing
        
    while (pi.read(buttons[4]) == 0):
        background = Image.new("1", (SCREEN_WIDTH, SCREEN_HEIGHT), "black")
        draw = ImageDraw.Draw(background)

        ball.move(player1, player2)

        
        if (pi.read(buttons[0]) == 1):
            time.sleep(debounce)
            if (pi.read(buttons[0]) == 1):
                player1.move_up()
        if (pi.read(buttons[1]) == 1):
            time.sleep(debounce)
            if (pi.read(buttons[1]) == 1):
                player1.move_down()

        # Stage
        draw.rectangle(device.bounding_box, outline="white")
        draw.line(((device.width / 2, 0), (device.width / 2, device.height)), fill="white")
        
        ball.draw(draw)
        player1.draw(draw)
        player2.draw(draw)
        player2.aiAssist(ball)

        device.display(background)

        if ball.gameOver:
            for i in range(3):
                _GameOverBg = Image.new("1", (SCREEN_WIDTH, SCREEN_HEIGHT), "white")
                _draw = ImageDraw.Draw(_GameOverBg)
                _draw.text((30, 20), "GAME OVER", font=font, fill="black")
                device.display(_GameOverBg)
                time.sleep(1)
            break
        #draw.text((device.width - 30), "Player 2", font=font, fill="white")
