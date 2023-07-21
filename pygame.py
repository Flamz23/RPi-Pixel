import time
import os
import pigpio
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306

import clock
import dino
import pong

class Pygame:

    def __init__(self):

        # define image paths
        self.PI_LOGO = "assets/pi_logo.png"

        # font
        self.FONT_PATH = "fonts/Roboto-Regular.ttf"
        self.FONT_SIZE = 12
        self.font = ImageFont.truetype(self.FONT_PATH, self.FONT_SIZE)
    
        # Define the size of the OLED screen
        self.SCREEN_WIDTH = 128
        self.SCREEN_HEIGHT = 64

        # Initialize the OLED screen
        self.serial = i2c(port=1, address=0x3C)
        self.device = ssd1306(self.serial)

        # main menu state
        self.options = ["Clock", "Dino", "Pong", "Invaders", "Breaker"]
        self.numOptions = len(self.options)
        self.highlighted = 0
        self.selectedIndex = 0
        self.optionChosen = False

        self.SPLASH_DELAY = 1

        # UP, DOWN, LEFT, RIGHT, SEL_1, SEL_2
        self.buttons = [20, 21, 25, 24, 12]
        self.numButtons = len(self.buttons)
        self.debounce = 0.02

        self.SplashScreen()
        self.IOconfig()
        self.Launcher()



    def IOconfig(self):

         self.pi = pigpio.pi()

         for i in range(self.numButtons):
            self.pi.set_mode(self.buttons[i], pigpio.INPUT) # set pins as input
            self.pi.set_pull_up_down(self.buttons[i], pigpio.PUD_DOWN) # enable pull-down resistor

         print("I0 setup complete!")



    def SplashScreen(self):

        # Load the image
        splash = Image.open(self.PI_LOGO).convert("1")

        # Create a new image to use as the background
        background = Image.new("1", (self.SCREEN_WIDTH, self.SCREEN_HEIGHT), "white")
        size = [min(self.device.size)] * 2
        pos = ((self.device.width - size[0]) // 2, self.device.height - size[1])

        background.paste(splash, pos)
        self.device.display(background)       
        time.sleep(self.SPLASH_DELAY) # aesthetic delay
        self.device.clear()



    def MainUI(self, draw, bg):

        currentTime = datetime.today().strftime("%I:%M")
        draw.text((96, 3), currentTime, font=self.font, fill="white")

        # Load the UI image
        logo = Image.open(self.PI_LOGO).convert("1").resize((37, 37))        
        bg.paste(logo, (80, 25))



    def MainMenu(self):

        # Define the position to start the list
        x = 3 # int((self.SCREEN_WIDTH - self.FONT_SIZE) / 2)
        y = int((self.SCREEN_HEIGHT - (self.numOptions * self.FONT_SIZE)) / 2)

        while (self.optionChosen == False):

            # Create a new image to use as the background
            background = Image.new("1", (self.SCREEN_WIDTH, self.SCREEN_HEIGHT), "black")

            # Draw the list of fruits on the background
            draw = ImageDraw.Draw(background)

            self.MainUI(draw, background) # add time and other ui elements

            for i,option in enumerate(self.options):
                posX = x
                posY = y + (i * self.FONT_SIZE)

                # draw to screen
                draw.text((posX, posY), option, font=self.font, fill="white")

                # Draw the box around the selected option
                if i == self.selectedIndex:
                    self.highlighted = posY
                    draw.rectangle((posX - 2, posY, posX + 50, posY + self.FONT_SIZE + 1), outline="white")
                
            self.device.display(background) # display image on OLED

            # Move the box down the list when the button is pressed
            if self.pi.read(self.buttons[1]) == 1:
                time.sleep(self.debounce)
                if (self.pi.read(self.buttons[1])) == 1:
                    self.selectedIndex += 1            
                    if self.selectedIndex >= self.numOptions: # roll-over
                        self.selectedIndex = 0                  
            elif self.pi.read(self.buttons[0]) == 1:
                time.sleep(self.debounce)
                if  (self.pi.read(self.buttons[0])) == 1:
                    self.selectedIndex -= 1
                    if self.selectedIndex < 0: # roll-over
                        self.selectedIndex = self.numOptions - 1

            # Select app to open
            if self.pi.read(self.buttons[4]) == 1:
                time.sleep(self.debounce)
                if (self.pi.read(self.buttons[4])) == 1:
                    self.optionChosen = True


            # selection box roll-over    
            if self.highlighted >= y + ((self.numOptions - 1) * self.FONT_SIZE):
                self.highlighted = y                
            elif self.highlighted < y:
                self.highlighted = y + ((self.numOptions - 1) * self.FONT_SIZE)
            else:
                self.highlighted += self.FONT_SIZE

            # print(f"selected: {self.selectedIndex}, highlighted: {self.highlighted}")

    def Launcher(self): 
        if self.optionChosen:
            if self.selectedIndex == 0:
                print(f"opening {self.options[self.selectedIndex]} app...")
                clock.clockApp(self.pi, self.buttons, self.debounce)
            elif self.selectedIndex == 1:
                print(f"opening {self.options[self.selectedIndex]} app...")
                dino.dinoApp(self.pi, self.buttons, self.debounce)
            elif self.selectedIndex == 2:
                print(f"opening {self.options[self.selectedIndex]} app...")
                pong.pongApp(self.pi, self.buttons, self.debounce)
            elif self.selectedIndex == 3:
                print(f"opening {self.options[self.selectedIndex]} app...")
            elif self.selectedIndex == 4:
                print(f"opening {self.options[self.selectedIndex]} app...")
            


        self.optionChosen = False # reset
        print("returning to main menu...")
        

PG = Pygame()
while True:
    PG.MainMenu()
    PG.Launcher()
