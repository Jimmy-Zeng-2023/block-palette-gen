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

# My other classes
from Block import *
from TextureReader import *
from BlockGenerator import *

# Base for all buttons the player can click on
class Button(object):
    def __init__(self, x, y, width, height,  
                 color = "gray",
                 text = "Button",
                 font = "Arial 20 bold",
                 textColor = "white"):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        self.color = color
        self.text = text
        self.font = font
        self.textColor = textColor

    def draw(self, canvas):
        canvas.create_rectange(self.x, self.y,
                               self.x + self.width, self.y + self.height,
                               width = 0,
                               fill = self.color)
        canvas.create_text(self.x + self.width/2, self.y + self.height/2,
                           text = self.text,
                           font = self.font,
                           fill = self.textColor)

    def checkInBounds(self, mouseX, mouseY):
        if(mouseX > self.x and mouseX < self.x + self.width and
           mouseY > self.Y and mouseY < self.y + self.height):
           return True
           # do what?

# A panel that holds the block and the corresponding buttons
class BlockPanel(object):
    def __init__(self, x, y, width, height, block = None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.block = block
        self.margins = 0

    def draw(self, app, canvas, scale = 8):
        canvas.create_rectangle(self.x, self.y,
                                self.x + self.width, self.y + self.height,
                                width = 0,
                                fill = "medium slate blue")
        self.block.draw(app, canvas, self.x + self.width/2, self.y + self.height/2, scale)
        # Draws buttons and block

    def setBlock(self, block):
        self.block = block


# Modes and ModalApp classes inherited from cmu-112-graphics
# Class Notes: Animation Part 1
class GeneratorMode(Mode):
    # Final frontend app
    def appStarted(self):
        path = "Block-textures-vanilla-1.14.4"
        self.myReader = TextureReader(50, path)
        self.blocks = self.myReader.parseFiles(path)
        print("Loading Complete!")
        self.myGen = BlockGenerator(self.blocks)

        self.panelXMargin = 30
        self.panelYMargin = 100
        self.panelHeight = 200
        self.createPanels()

    def createPanels(self):
        self.panels = []
        panelWidth = (self.width - 2*self.panelXMargin) // 5
        panelHeight = self.panelHeight
        panelX = self.panelXMargin
        panelY = self.panelYMargin
        for block in self.myGen.state.blocks:
            panel = BlockPanel(panelX, panelY,
                               panelWidth - 5, panelHeight,
                               block = block)
            self.panels.append(panel)
            panelX += panelWidth

    def updatePanels(self):
        for i in range(len(self.myGen.state.blocks)):
            block = self.myGen.state.blocks[i]
            panel = self.panels[i]
            panel.setBlock(block)            

    def timerFired(self): pass
        # Used for animations

    def keyPressed(self, event):
        if(event.key == 'r'):
            self.myGen.generate() # Save state in App or in Generator?
            self.updatePanels()

    def drawBg(self, canvas):
        canvas.create_rectangle(0, 0,
                                self.width,
                                self.height,
                                width = 0,
                                fill = "dark slate blue")

    def drawBlockPanels(self, canvas):
        for panel in self.panels:
            panel.draw(self, canvas)

    def drawButtons(self, canvas):
        pass

    def redrawAll(self, canvas):
        # Background
        self.drawBg(canvas)
        # Blocks
        self.drawBlockPanels(canvas)
        # Buttons
        self.drawButtons(canvas)
        # Animations

class PresetMode(Mode):
    # Changes the state
    def appStarted(self):
        self.app.generator.myGen

class BlockPaletteGenerator(ModalApp):
    def appStarted(self):
        self.generator = GeneratorMode()
        self.presets = PresetMode()
        self.setActiveMode(self.generator)
        self.state = State([], [])
        self.timerDelay = 1000

def main():
    myPaletteGenerator = BlockPaletteGenerator(width = 800, height = 600)

if __name__ == "__main__":
    main()