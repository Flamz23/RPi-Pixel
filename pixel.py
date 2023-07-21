"""
File: pixel/pixel.puy

Control a OLED Display.

Dependencies:
  pip3 install luma.oled
"""
import time
import os
from pathlib import Path
from PIL import Image
from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.oled.device import ssd1306  # , ssd1309, ssd1325, ssd1331, sh1106
from luma.core.render import canvas
from luma.core.sprite_system import framerate_regulator
from luma.core.interface.serial import i2c, spi

serial = i2c(port=1, address=0x3C)

# class Pixel:

#     # OLED display is using I2C at address 0x3C
#     serial = i2c(port=1, address=0x3C)
#     device = ssd1306(serial)

#     def __init__(self):
#         self.device.clear()
#         print("Screen Dimensions (WxH):", self.device.size)


def main():

    if device.width < 96 or device.height < 64:
        raise ValueError(f"Unsupported mode: {device.width}x{device.height}")

    regulator = framerate_regulator()  # enable frame regulator

    # show splash screen
    img_path = str(Path(__file__).resolve(
    ).parent.joinpath('assets', 'pi_logo.png'))
    logo = Image.open(img_path)
    size = [min(*device.size)] * 2
    pos = ((device.width - size[0]) // 2, device.height - size[1])

    background = Image.new("RGB", device.size, "white") # create background
    background.paste(logo, pos)
    device.display(background.convert(device.mode))

    time.sleep(6)

def menu():
    highlight = 0
    selected = False

    # Create home screen menu
    while not selected:

        # Top Menu
        


if __name__ == '__main__':
    try:
        device = ssd1306(serial)
        main()

    except KeyboardInterrupt:
        pass
