#################################################
# 15-112 Term Project: Minecraft Block Palette Generator by Jimmy Zeng

# Inspired by online color palette generators like Colormind.io, this project
# aims to generate a list of minecraft blocks that work well with each other in
# any build based on their textures and colors.
#
# Your name: Jimmy Zeng
# Your andrew id: jimmyzen
#################################################

from cmu_112_graphics import * # From Class Notes: Animation Part 1
from tkinter import *
from PIL import Image
import random, math, copy, string, time, os
from tkinter.font import *

# My other classes
from Block import *
from Buttons import *
from TextureReader import *

#################################################
# The PresetPanel Stores 5 blocks made as a preset to load into the generator
#################################################

class PresetPanel(object):
    # Used in Preset Mode to load into the generator.
    def __init__(self, width, height, blocks, name):
            self.width = width
            self.height = height
            self.blocks = blocks # List of 5 block objects to display
            self.name = name # Name of the preset
            self.nameFont = "Verdana 20 bold italic"
            self.nameColor = "white"

            self.color = "gray20" #SlateBlue4"
            self.color2 = "SlateBlue4"
            self.scale = 5 # Scale for the blocks to be drawn at
            self.blockGap = 20
            self.textX = 10
            self.topMargin = 5
            self.blockX = 220

            #self.convertedName = TextureReader.convertBlockNames(self.block.name)
    
    def checkInBounds(self, mouseX, mouseY):
        if(mouseX > self.x and mouseX < self.x + self.width and
           mouseY > self.y and mouseY < self.y + self.height):
            return self.blocks
        else:
            return None

    def draw(self, app, canvas, x, y):
        # Draw the panel at the X, Y location
        # Draw panel rectangle
        self.x = x
        self.y = y # Sadly, the x and y do need to be stored for bound calculations 
        canvas.create_rectangle(x, y,
                                x + self.width, y + self.height,
                                fill = self.color,
                                width = 0)
        canvas.create_rectangle(x + 5, y + 5,
                                x + self.width - 10, y + self.height - 10,
                                fill = self.color2,
                                width = 0)

        canvas.create_text(x + self.textX,
                           y + self.height//2,
                           text = self.name,
                           font = self.nameFont,
                           fill = self.nameColor,
                           anchor = "w")

        blockX = x + self.blockX
        blockY = y + self.height // 2
        dx = (self.width - self.blockX) // 5

        for block in self.blocks:
            block.draw(app, canvas,
                       blockX + dx // 2,
                       blockY,
                       self.scale)
            blockX += dx
                            
        