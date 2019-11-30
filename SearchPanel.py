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
# The SearchPanel is implemented in __init__.py. It contains a background, a block,
# three buttons, and the block's name.
#################################################

class SearchPanel(object):
    def __init__(self, x, y, width, height, blocks, icons):
        # blocks - Dict of all blocks to be displayed
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.blocks = blocks
        self.blockLst = list(self.blocks.values()) # blocks needs to be converted to an iterable list

        self.topMargin = 10 # Margin for the main list vertically
        self.buttonMargin = 5 # Margin for the buttons
        self.panelMargin = 42 # Margin for the main list
        self.borderColor = "gray20"
        self.mainColor = "SlateBlue4"

        self.icons = icons # Icons is the ui_images dictionary

        self.visible = False
        self.start = 0
        self.rows = 3
        self.cols = 9
        self.blocksPerPage = self.rows * self.cols
        self.startX = self.x + self.panelMargin
        self.startY = self.y + self.topMargin
    
        self.scale = 4
        # Side length of each block
        self.cellWidth = (self.width - 2 * self.panelMargin) // self.cols
        self.cellHeight = (self.height - 2 * self.topMargin) // self.rows

        self.createButtons()
        self.makeSimpleBlocks() # A dictionary with easier to spell names

    def createButtons(self):
        # 3 buttons, left, right, and search
        side = 32 # side length of each button

        x = self.x + self.buttonMargin
        y = self.y + self.height // 2
        inactive = self.icons["inactive-leftButton"]
        active = self.icons["leftButton"]
        self.leftButton = ImageButton(x, y, side, side, inactive, active)
        
        x = self.x + self.width - self.buttonMargin - 32
        y = self.y + self.height // 2
        inactive = self.icons["inactive-rightButton"]
        active = self.icons["rightButton"]
        self.rightButton = ImageButton(x, y, side, side, inactive, active)

        x = self.x + self.buttonMargin
        y = self.y + self.topMargin
        inactive = self.icons["inactive-search"]
        active = self.icons["search"]
        self.searchButton = ImageButton(x, y, side, side, inactive, active)

##################################
#          App Helpers           #
##################################

    def checkButtonClick(self, app, x, y):
        # Check if a button has been clicked on, and perform the acoording action
        block = None

        if(not self.checkInPanel(x, y)):
            # Exit tells the app to exit the panel instead of doing nothing
            return "exit"

        if(self.leftButton.checkInBounds(x, y)):
            self.start -= self.blocksPerPage
            if(self.start < 0):
                self.start += self.blocksPerPage

        elif(self.rightButton.checkInBounds(x, y)):
            self.start += self.blocksPerPage
            if(self.start > len(self.blockLst)):
                self.start -= self.blocksPerPage

        elif(self.searchButton.checkInBounds(x, y)):
            block = self.search(app)

        else: # Checks the main panel
            block = self.checkBlockClick(x, y)
        
        return block

    def checkInPanel(self, x, y):
        # Check if the click is inside the panel at all.
        # if not, the panel should close.
        x1 = self.x
        y1 = self.y
        x2 = self.x + self.width
        y2 = self.y + self.height
        return (x > x1 and x < x2 and
                y > y1 and y < y2)

    def getRowCol(self, x, y):
        col = x // self.cellWidth
        row = y // self.cellHeight
        return (row, col) 

    def checkBlockClick(self, x, y):
        # Check if a block has been clicked on, and return the block to App
        x1 = self.x + self.panelMargin
        y1 = self.y + self.topMargin
        x2 = self.x + self.width - self.panelMargin
        y2 = self.y + self.height - self.topMargin
        # If the click is inside the main panel but not on any block, skip this.
        if(not (x > x1 and x < x2 and
                y > y1 and y < y2)): return None

        newX = x - self.startX
        newY = y - self.startY
        row, col = self.getRowCol(newX, newY)
        blockIndex = row * self.cols + col + self.start
        return self.blockLst[blockIndex]
    
    def search(self, app):
        # Used for the search button
        key = app.getUserInput("Input the name of the block:")
        userKey = key.lower().replace(' ', '') # Capitals and spaces don't matter
        if(userKey in self.simpleBlocks):
            return self.simpleBlocks[userKey]

    def makeSimpleBlocks(self):
        self.simpleBlocks = dict() # Names of the blocks are trimmed and made simpler
        for key in self.blocks:
            block = self.blocks[key]
            convertedKey = key.lower()
            convertedKey = convertedKey.replace('_', '')
            self.simpleBlocks[convertedKey] = block

            if("block" in convertedKey):
                convertedKey1 = convertedKey.replace('block', '')
                self.simpleBlocks[convertedKey1] = block

##################################
#            Draw()              #
##################################

    def draw(self, app, canvas):
        if(not self.visible): return

        # Draws Panels
        canvas.create_rectangle(self.x, self.y,
                                self.x + self.width, self.y + self.height,
                                fill = self.borderColor,
                                width = 0)
        
        x1 = self.x + self.panelMargin
        y1 = self.y + self.topMargin
        x2 = self.x + self.width - self.panelMargin
        y2 = self.y + self.height - self.topMargin
        canvas.create_rectangle(x1, y1,
                                x2, y2,
                                fill = self.mainColor,
                                width = 0)

        # Draw Buttons
        self.leftButton.draw(canvas)
        self.rightButton.draw(canvas)
        self.searchButton.draw(canvas)

        # Draw Blocks
        self.drawBlocks(app, canvas)

    def drawBlocks(self, app, canvas):
        for i in range(self.start, self.start + self.blocksPerPage):
            row = (i - self.start) // self.cols
            col = (i - self.start) % self.cols

            if (i >= len(self.blockLst)): return
            
            block = self.blockLst[i]
            x = col * self.cellWidth + self.startX + self.cellWidth//2
            y = row * self.cellHeight + self.startY + self.cellHeight//2 # Extra to center block
            block.draw(app, canvas, x, y, self.scale)
