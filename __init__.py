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
from TextureReader import *
from BlockGenerator import *
from Buttons import *
from Panels import *

#################################################
# TODO: QUESTIONS FOR DINA
# 
# 1. How to avoid having 10 + variable constructors?
# 2. Best way to organize button actions?
#       - Button do own action, or app do action?
# 3. Organize subclasses?
#       - Subclass for each type of button? Or generic subclasses?
# 4. Generator hold frame object or App hold?
# 5. Getting good fonts in tkinter?

# Lock button
# Polish algorithm
# Do rest of UI
# Send Dina video of project tonight (before 1130)
#################################################

# Modes and ModalApp classes inherited from cmu-112-graphics
# Class Notes: Animation Part 1
class GeneratorMode(Mode):
    # Final frontend app
    def appStarted(self):

        path = self.app.paths["textures"]
        self.myReader = TextureReader(50, path)
        self.blocks = self.myReader.parseFiles(path)
        print("Loading Complete!")
        self.myGen = BlockGenerator(self.blocks)

        self.panelXMargin = 20
        self.panelYMargin = 150
        self.panelHeight = 200
        self.margins = {}

        self.ui = {
            "smallFont" : "Verdana 10",
            "medFont" : "Verdana 12 bold",
            "largeFont" : "Verdana 18 bold",
            "genModeButton" : (66, 10, 96, 38),
            "presetButton" : (198, 10, 96, 38),
            "generateButton" : (570, 450, 200, 50)
        }

        self.setBackground()
        self.topLevelButtons = []
        self.createPanels()
        self.createButtons()

##################################
#     appStarted() Helpers       #
##################################        

    def setBackground(self):
        self.background = self.app.ui_images["Bg_Normal"]

    def createPanels(self):
        self.panels = []
        panelWidth = (self.width - 2*self.panelXMargin) // 5
        panelHeight = self.panelHeight
        panelX = self.panelXMargin
        panelY = self.panelYMargin

        for block in self.myGen.state.blocks:
            panel = BlockPanel(panelX, panelY,
                               panelWidth - 10,
                               panelHeight,
                               self.app.ui_images,
                               block = block)
            self.panels.append(panel)
            panelX += panelWidth

    def createButtons(self):
        x, y, width, height = self.ui["genModeButton"]
        genModeButton = TextButton(x, y, width, height,
                                    action = None,
                                    text = "Generator",
                                    font = self.ui["medFont"], 
                                    textColor = "white",
                                    activeColor = "white",
                                    offset = 5)
        
        self.topLevelButtons.append(genModeButton)

        x, y, width, height = self.ui["presetButton"]
        presetButton = TextButton(x, y, width, height,
                                    action = "changeMode",
                                    text = "Presets",
                                    font = self.ui["medFont"], 
                                    textColor = "white",
                                    activeColor = "white",
                                    offset = 5)
        self.topLevelButtons.append(presetButton)

        x, y, width, height = self.ui["generateButton"]
        icon = Image.open(self.app.paths["generate"]).convert("RGBA")
        generateButton = GenerateButton(x, y, width, height,
                                    action = "generate",
                                    text = "Generate!",
                                    font = self.ui["largeFont"],
                                    textColor = "gray15",
                                    activeColor = "white",
                                    image = icon,
                                    color = "dark slate blue",
                                    margins = (5,5))
        self.topLevelButtons.append(generateButton) 

##################################
#      Controller Helpers        #
##################################

    def updatePanels(self):
        for i in range(len(self.myGen.state.blocks)):
            block = self.myGen.state.blocks[i]
            panel = self.panels[i]
            panel.setBlock(block)

    def generatePalette(self):
        self.myGen.generate() # Save state in App or in Generator?
        self.updatePanels()

    def changeMode(self):
        self.app.setActiveMode(self.app.presets)
    
    def checkButtons(self, mouseX, mouseY):
        for button in self.topLevelButtons:
            if button.checkInBounds(mouseX, mouseY): # If a button was in bounds
                if button.action == "generate":
                    self.generatePalette()
                elif button.action == "changeMode":
                    self.changeMode()


##################################
#     Top Level Controllers      #
##################################

    def timerFired(self): pass
        # Used for animations

    def keyPressed(self, event):
        if(event.key == 'r'):
            self.myGen.generate() # Save state in App or in Generator?
            self.updatePanels()
    
    def mousePressed(self, event):
        self.checkButtons(event.x, event.y)

##################################
#         View Functions         #
##################################

    def drawBg(self, canvas):
        canvas.create_image(0, 0,
                            image = ImageTk.PhotoImage(self.background),
                            anchor = "nw")

    def drawBlockPanels(self, canvas):
        for panel in self.panels:
            panel.draw(self, canvas)

    def drawButtons(self, canvas):
        for button in self.topLevelButtons:
            button.draw(canvas)

    def redrawAll(self, canvas):
        # Background
        self.drawBg(canvas)
        # Blocks
        self.drawBlockPanels(canvas)
        # Buttons
        self.drawButtons(canvas)
        # Animations

###################################################################
#                       The Preset Mode                           #
###################################################################

class PresetMode(Mode):
    # Changes the state
    def appStarted(self):
        
        self.ui = {
            "smallFont" : "Verdana 10",
            "medFont" : "Verdana 12 bold",
            "largeFont" : "Verdana 18 bold",
            "genModeButton" : (66, 10, 96, 38),
            "presetButton" : (198, 10, 96, 38)
        }

        self.setBackground()
        self.createButtons()

##################################
#     appStarted() Helpers       #
################################## 

    def setBackground(self):
        self.background = self.app.ui_images["Bg_Alternate"]

    def createButtons(self):
        self.topLevelButtons = []
        x, y, width, height = self.ui["genModeButton"]
        genModeButton = TextButton(x, y, width, height,
                                    action = "changeMode",
                                    text = "Generator",
                                    font = self.ui["medFont"], 
                                    textColor = "white",
                                    activeColor = "white",
                                    offset = 5)
        
        self.topLevelButtons.append(genModeButton)

        x, y, width, height = self.ui["presetButton"]
        presetButton = TextButton(x, y, width, height,
                                    action = None,
                                    text = "Presets",
                                    font = self.ui["medFont"], 
                                    textColor = "white",
                                    activeColor = "white",
                                    offset = 5)
        self.topLevelButtons.append(presetButton)

##################################
#      Controller Helpers        #
##################################

    def changeMode(self):
        self.app.setActiveMode(self.app.generator)
    
    def checkButtons(self, mouseX, mouseY):
        for button in self.topLevelButtons:
            if button.checkInBounds(mouseX, mouseY): # If a button was in bounds
                if button.action == "changeMode":
                    self.changeMode()

##################################
#     Top Level Controllers      #
##################################

    def mousePressed(self, event):
        self.checkButtons(event.x, event.y)

##################################
#         View Functions         #
##################################

    def drawBg(self, canvas):
        canvas.create_image(0, 0,
                            image = ImageTk.PhotoImage(self.background),
                            anchor = "nw")

    def drawButtons(self, canvas):
        for button in self.topLevelButtons:
            button.draw(canvas)

    def redrawAll(self, canvas):
        self.drawBg(canvas)
        self.drawButtons(canvas)


class BlockPaletteGenerator(ModalApp):
    def appStarted(self):
        self.paths = {
            "textures" : "Block-textures-vanilla-1.14.4",
            "Bg_Normal" : "ui-images/Bg_normal.png",
            "Bg_Alternate" : "ui-images/Bg_alternate.png",
            "search" : "ui-images/search-icon.png",
            "drag" : "ui-images/drag-icon.png",
            "lock" : "ui-images/lock-icon.png",
            "unlock" : "ui-images/unlock-icon.png",
            "generate" : "ui-images/generate-icon.png",
        }

        self.ui_images = dict() # Creates a dictionary of the UI images
        for key in self.paths:
            if(key == "textures"): continue
            elif(key in ["search", "drag", "lock", "unlock"]):
                self.ui_images[key] = self.createIcons(key)
            else:
                self.ui_images[key] = Image.open(self.paths[key]).convert("RGBA")

        self.generator = GeneratorMode()
        self.presets = PresetMode()
        self.setActiveMode(self.generator)
        self.state = State([], [])
        self.timerDelay = 1000

    def createIcons(self, key):
        if(key == "unlock"):
            unlockIcon = Image.open(self.paths[key]).convert("RGBA")
            return (unlockIcon, unlockIcon)
        else:
            activeIcon = Image.open(self.paths[key]).convert("RGBA")
            colorMask = Image.new('RGBA', (activeIcon.width, activeIcon.height), 
                                   color = "gray")
            inactiveIcon = Image.composite(colorMask, activeIcon, activeIcon)
            return (inactiveIcon, activeIcon)


def main():
    myPaletteGenerator = BlockPaletteGenerator(width = 800, height = 600)

if __name__ == "__main__":
    main()