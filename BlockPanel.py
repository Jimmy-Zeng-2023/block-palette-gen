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
# The BlockPanel is implemented in __init__.py. It contains a background, a block,
# three buttons, and the block's name.
#################################################

# A panel that holds the block and the corresponding buttons
class BlockPanel(object):
    def __init__(self, x, y, width, height, icons, block = None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.block = block
        self.margins = 2
        self.icons = icons # Icons is a dict of icons for the 3 buttons
        self.isLocked = False
        self.isSearching = False

        self.nameFont = "Verdana 10 italic"
        self.nameColor = "white"
        self.convertedName = TextureReader.convertBlockNames(self.block.name)

        self.createButtons()

    def createButtons(self):
        side = 32 # The side length of each button
        y = self.y + self.height + self.margins * 2
        x = self.x + self.width - side

        # The Drag Button (2)
        active = self.icons["drag"]
        inactive = self.icons["inactive-drag"]
        self.dragButton = ImageButton(x, y, side, side, inactive, active)
        x -= (side + self.margins)
            
        # The Search Button (1)
        active = self.icons["search"]
        inactive = self.icons["inactive-search"]
        self.searchButton = ImageButton(x, y, side, side, inactive, active)
        x -= (side + self.margins)

        # The Lock Button (0)
        activeUnlock = self.icons["unlock"]
        inactiveUnlock = self.icons["inactive-unlock"]
        lock = self.icons["lock"]
        self.lockButton = LockButton(x, y, side, side, lock, inactiveUnlock, activeUnlock)
    
    # Determines which button has been clicked
    def checkInBounds(self, mouseX, mouseY):
        if(self.isSearching): return
        # When searching, buttons do not function
        if(self.dragButton.checkInBounds(mouseX, mouseY)):
            return "drag"
        elif(self.searchButton.checkInBounds(mouseX, mouseY)):
            return "search"
        elif(self.lockButton.checkInBounds(mouseX, mouseY)):
            self.lockPanel()
            return "lock"

    def lockPanel(self):
        self.isLocked == True
        self.lockButton.lock()

    def draw(self, app, canvas, scale = 8):
        if(self.isSearching): # When searching, the panel extends to meet with the search panel.
            y2 = self.y + self.height + 40
        else:
            y2 = self.y + self.height
    
        canvas.create_rectangle(self.x, self.y,
                                self.x + self.width, y2,
                                width = 0,
                                fill = "SlateBlue3")
        canvas.create_text(self.x + self.margins, self.y + self.margins,
                           text = self.convertedName,
                           font = self.nameFont,
                           fill = self.nameColor,
                           anchor = "nw")
        self.block.draw(app, canvas, self.x + self.width/2, self.y + self.height/2, scale)
        
        if(not self.isSearching):  # When searching, these buttons should not appear
            self.dragButton.draw(canvas)
            self.searchButton.draw(canvas)
            self.lockButton.draw(canvas)

    def setBlock(self, block):
        self.block = block
        self.convertedName = TextureReader.convertBlockNames(self.block.name)

    def __eq__(self, other):
        return (isinstance(other, BlockPanel) and
               self.x == other.x)