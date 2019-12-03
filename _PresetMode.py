#################################################
# 15-112 Term Project: Minecraft Block Palette Generator by Jimmy Zeng

# Inspired by online color palette generators like Colormind.io, this project
# aims to generate a list of minecraft blocks that work well with each other in
# any build based on their textures and colors.
#
# Your name: Jimmy Zeng
# Your andrew id: jimmyzen
#################################################

from cmu_112_graphics import * # From Class Notes: Animation Part 2
from tkinter import *
from PIL import Image
import random, math, copy, string, time, os
from tkinter.font import *

# My other classes
from Block import *
from TextureReader import *
from BlockGenerator import *
from _GeneratorMode import *

from Buttons import *
from BlockPanel import *
from SearchPanel import *
from PresetPanel import *

#################################################
#              -= THE PRESET MODE =-
#
# This alternative mode lets users choose from a few pre-created
# color palettes to jump-start their generator.
#
# Citation: The Mode and ModalApp classes come from cmu-112-graphics, from Course Notes: Animations Part 2
#################################################

class PresetMode(Mode):
    # Changes the state
    def appStarted(self):
        
        self.ui = {
            "smallFont" : "Verdana 10",
            "medFont" : "Verdana 12 bold",
            "largeFont" : "Verdana 18 bold",
            "genModeButton" : (79, 55, 172, 50),
            "presetButton" : (290, 55, 154, 50),
            "margins" : (20, 150, 100, 110)
            #            Left, top, height, gap
        }
        
        self.presetsDict = {
            "Futuristic" : ["quartz_block_top", "quartz_pillar", "cyan_terracotta", "blue_terracotta", "red_terracotta"],
            "Medieval" : ["spruce_log", "spruce_planks", "oak_planks", "cobblestone", "stone_bricks"],
            "Atlantian" : ["prismarine", "sea_lantern", "dark_prismarine", "stripped_birch_log", "brain_coral_block"],
            "Desert" : ["sandstone", "cut_sandstone", "terracotta", "chiseled_red_sandstone", "spruce_log"],
            "Arctic" : ["packed_ice", "blue_ice", "snow", "cobblestone", "stone_bricks"]
        }

        self.setBackground()
        self.createButtons()
        self.createPresetPanels()

##################################
#     appStarted() Helpers       #
################################## 

    def setBackground(self):
        self.background = self.app.ui_images["Bg_Alternate"]
        self.bgMiddle = self.background.crop((480, 0, 1400, 1009))

    def createButtons(self):
        x, y, width, height = self.ui["genModeButton"]
        self.genModeButton = ImageButton(x, y, width, height)
        
        x, y, width, height = self.ui["presetButton"]
        self.presetButton = ImageButton(x, y, width, height)

    def createPresetPanels(self):
        # "Medieval" : [acacia_leaves, oak_log...]
        presetsDict = self.presetsDict
        self.presetPanels = []

        
        leftMargin, topMargin, panelHeight, gap = self.ui["margins"]
        panelWidth = self.width - 2 * leftMargin

        for name in presetsDict:
            blockNames = presetsDict[name] # List of strings
            blocks = self.search(blockNames)
            newPanel = PresetPanel(panelWidth, panelHeight, blocks, name)
            self.presetPanels.append(newPanel)

    def search(self, blockNames): # blockNames is a list of strings
        blocks = []
        for name in blockNames:
            if(name in self.app.blocks):
                blocks.append(self.app.blocks[name])
        return blocks

##################################
#      Controller Helpers        #
##################################

    def changeMode(self):
        self.app.setActiveMode(self.app.generator)
        self.app.sizeChanged()
    
    def checkButtons(self, mouseX, mouseY):
        if(self.genModeButton.checkInBounds(mouseX, mouseY)):
            self.changeMode()
        elif(self.presetButton.checkInBounds(mouseX, mouseY)):
            pass

    def checkPanels(self, mouseX, mouseY):
        for presetPanel in self.presetPanels:
            selected = presetPanel.checkInBounds(mouseX, mouseY)
            if(selected != None):
                self.updateState(selected)

    def updateState(self, blocks):
        self.app.state.blocks = blocks
        #self.app.state.locked = {0, 1, 2, 3, 4}
        self.app.generator.updatePanels()
        self.app.generator.endSearch()
        self.app.setActiveMode(self.app.generator)
        
##################################
#     Top Level Controllers      #
##################################

    def mousePressed(self, event):
        print("Mouse clicked:", event.x, event.y)
        self.checkButtons(event.x, event.y)
        self.checkPanels(event.x, event.y)

##################################
#         View Functions         #
##################################

    def drawBg(self, canvas):
        canvas.create_image(0, 0,
                            image = ImageTk.PhotoImage(self.background),
                            anchor = "nw")
        if(self.app.width > 1400):
            # When its too big, shoehorn fixes in another background
            canvas.create_image(1400, 0,
                            image = ImageTk.PhotoImage(self.bgMiddle),
                            anchor = "nw")

    def drawButtons(self, canvas):
        self.genModeButton.draw(canvas)
        self.presetButton.draw(canvas)

    def drawPresetPanels(self, canvas):
        leftMargin, topMargin, panelHeight, gap = self.ui["margins"]
        x = leftMargin
        y = topMargin
        for presetPanel in self.presetPanels:
            presetPanel.draw(self, canvas, x, y)
            y += gap

    def redrawAll(self, canvas):
        self.drawBg(canvas)
        self.drawPresetPanels(canvas)
        self.drawButtons(canvas)