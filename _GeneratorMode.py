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
from GeneratorMode import *
from PresetMode import *

from Buttons_Panels.Buttons import *
from Buttons_Panels.BlockPanel import *
from Buttons_Panels.SearchPanel import *
from Buttons_Panels.PresetPanel import *

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

#################################################
# The GeneratorMode is the basic Mode for generating block palettes.
#
# Citation: The Mode and ModalApp classes come from cmu-112-graphics, from Course Notes: Animations Part 2
#################################################
class GeneratorMode(Mode):
    # Final frontend app
    def appStarted(self):

        path = self.app.paths["textures"]
        self.myReader = TextureReader(50, path)
        self.blocks = self.myReader.parseFiles(path)
        print("Loading Complete!")
        self.myGen = BlockGenerator(self.blocks)
        self.state = State([self.blocks[0] for _ in range(5)])

        self.ui = {
            "smallFont" : "Verdana 10",
            "medFont" : "Verdana 12 bold",
            "largeFont" : "Verdana 18 bold",
            "genModeButton" : (79, 55, 172, 50),
            "presetButton" : (290, 55, 154, 50),
            "generateButton" : (690, 430, 200, 50),
            "panels" : (20, 170, 200)
        }

        self.setBackground()
        self.topLevelButtons = []
        self.createButtons()
        self.createPanels()
        self.generatePalette()
        self.createSearchPanel()

##################################
#     appStarted() Helpers       #
##################################        

    def setBackground(self):
        self.background = self.app.ui_images["Bg_Normal"]
        self.bgMiddle = self.background.crop((480, 0, 1400, 1009))

    def createPanels(self):
        self.panels = []
        panelX, panelY, panelHeight = self.ui["panels"]
        panelWidth = (self.width - 2*panelX) // 5
        
        for block in self.state.blocks:
            panel = BlockPanel(panelX, panelY,
                               panelWidth - 10,
                               panelHeight,
                               self.app.ui_images,
                               block = block)
            self.panels.append(panel)
            panelX += panelWidth

    def createButtons(self):
        x, y, width, height = self.ui["genModeButton"]
        self.genModeButton = ImageButton(x, y, width, height)
        
        x, y, width, height = self.ui["presetButton"]
        self.presetButton = ImageButton(x, y, width, height)

        x, y, width, height = self.ui["generateButton"]
        x = self.width - self.ui["panels"][0] - width
        sprite = self.app.ui_images["generateButton"]
        self.generateButton = ImageButton(x, y, width, height, sprite)

    def createSearchPanel(self): pass
        # Makes the search panel. but keeps it offscreen (with negative coords?)

    def makeSearchPanelVisible(self): pass
        # Change the coords on the panel to make it on screen, with extra box towards the panel its changing.

##################################
#      Controller Helpers        #
##################################

    def updatePanels(self):
        for i in range(len(self.state.blocks)):
            block = self.state.blocks[i]
            panel = self.panels[i]
            panel.setBlock(block)

    def generatePalette(self):
        self.state = self.myGen.generate(self.state)
        self.updatePanels()

    def changeMode(self):
        self.app.setActiveMode(self.app.presets)
        self.app.sizeChanged()
    
    def checkButtons(self, mouseX, mouseY):
        if(self.genModeButton.checkInBounds(mouseX, mouseY)):
            pass
        elif(self.presetButton.checkInBounds(mouseX, mouseY)):
            self.changeMode()
        elif(self.generateButton.checkInBounds(mouseX, mouseY)):
            self.generatePalette()

        for i in range(len(self.panels)):
            panel = self.panels[i]
            if(panel.checkInBounds(mouseX, mouseY) == "lock"):
                if(i not in self.state.locked):
                    self.state.locked.add(i)
                else:
                    self.state.locked.remove(i)
            elif(panel.checkInBounds(mouseX, mouseY) == "search"):
                self.makeSearchPanelVisible()

        # TODO:
        if(self.searching):
            self.searchPanel checkinbounds
    
    def sizeChanged(self):
        if(self.app.width > 900):
            self.createPanels()
            self.createButtons()


##################################
#     Top Level Controllers      #
##################################

    def timerFired(self): pass
        # Used for animations

    def keyPressed(self, event):
        if(event.key == 'r'):
            self.generatePalette()
    
    def mousePressed(self, event):
        print(event.x, event.y)
        self.checkButtons(event.x, event.y)

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

    def drawBlockPanels(self, canvas):
        for panel in self.panels:
            panel.draw(self, canvas)

    def drawButtons(self, canvas):
        self.genModeButton.draw(canvas)
        self.presetButton.draw(canvas)
        self.generateButton.draw(canvas)

    def redrawAll(self, canvas):
        # Background
        self.drawBg(canvas)
        # Blocks
        self.drawBlockPanels(canvas)
        # Buttons
        self.drawButtons(canvas)
        # Animations