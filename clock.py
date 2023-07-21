import time
import os
import pigpio
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306


def clockApp(pi, buttons, debounce):

    # font
    FONT_PATH = "fonts/Roboto-Regular.ttf"
    FONT_SIZE_1 = 18
    FONT_SIZE_2 = 12
    font1 = ImageFont.truetype(FONT_PATH, FONT_SIZE_1)
    font2 = ImageFont.truetype(FONT_PATH, FONT_SIZE_2)
        
    # Define the size of the OLED screen
    SCREEN_WIDTH = 128
    SCREEN_HEIGHT = 64
    
    # Initialize the OLED screen
    serial = i2c(port=1, address=0x3C)
    device = ssd1306(serial)

    # debounce
    while (pi.read(buttons[4]) == 1):
        pass # do nothing
    
    while (pi.read(buttons[4]) == 0):
        background = Image.new("1", (SCREEN_WIDTH, SCREEN_HEIGHT), "white")
        draw = ImageDraw.Draw(background)

        currentTime = datetime.today().strftime("%I:%M %p") 
        currentDate = datetime.today().strftime("%B %d, %Y")
        draw.text((20, 20), currentTime, font=font1, fill="black")
        draw.text((50, 50), currentDate, font=font2, fill="black")

        device.display(background) # diplay on OLED
    print("closing clock app...")
