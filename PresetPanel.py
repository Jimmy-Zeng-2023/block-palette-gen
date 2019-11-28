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
    # Needs list of 5 blocks
    def __init__(self, x, y, width, height, icons, blocks):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.block = block
            self.margins = 2
            self.icons = icons # Icons is a dict of icons for the 3 buttons
            self.isLocked = False

            self.nameFont = "Verdana 10 italic"
            self.nameColor = "white"
            self.convertedName = TextureReader.convertBlockNames(self.block.name)

            self.createButtons()