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

# Base for all buttons the player can click on
class Button(object):
    def __init__(self, x, y, width, height, action = "", color = None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.action = action
        self.color = color

    def draw(self, canvas):
        # Draws the rectangle of the button
        if(self.color != None):
            canvas.create_rectangle(self.x, self.y,
                                    self.x + self.width, self.y + self.height,
                                    width = 0,
                                    fill = self.color)

    def checkInBounds(self, mouseX, mouseY):
        return (mouseX > self.x and mouseX < self.x + self.width and
                mouseY > self.y and mouseY < self.y + self.height)
        
# Button that also displays text
class TextButton(Button):
    def __init__(self, x, y, width, height,
                 font, text, textColor, activeColor, action, offset = 0, color = None):
        super().__init__(x, y, width, height, action, color)
        self.text = text
        self.font = font
        self.textColor = textColor
        self.activeColor = activeColor
        self.offset = offset

    def draw(self, canvas):
        super().draw(canvas)
        canvas.create_text(self.x + self.width/2, self.y + self.height/2 + self.offset,
                           text = self.text,
                           font = self.font,
                           fill = self.textColor,
                           activefill = self.activeColor)

# Buttons that display an image
class ImageButton(Button):
    def __init__(self, x, y, width, height, action, sprites):
        super().__init__(x, y, width, height, action, None)
        # Active is image displayed when moused over
        # sprites holds both the regular and the active image
        image, active = sprites
        self.image = image.resize((width, height))
        self.active = active.resize((width, height))

    def draw(self, canvas):
        canvas.create_image(self.x, self.y,
                            image = ImageTk.PhotoImage(self.image),
                            activeimage = ImageTk.PhotoImage(self.active),
                            anchor = "nw")

class LockableButton(ImageButton):
    def __init__(self, x, y, width, height, action, lockSprites, unlockSprite):
        self.lockSprites = lockSprites
        self.unlockSprites = unlockSprite
        image, active = self.lockSprites
        self.isLocked = False # If locked, the unlock button should appear.
                              # Else, the lock button should appear
        self.lockedColor = "deep sky blue" # the button glows this color when locked

        super().__init__(x, y, width, height, action, self.lockSprites)
    
    def lock(self):
        self.isLocked = not self.isLocked
        (self.image, self.active) = self.unlockSprite # The unlock button is always shaded in

    def draw(self, canvas):
        if(self.isLocked):
            canvas.create_oval(self.x, self.y,
                               self.x + self.width, self.y + self.height,
                               width = 0,
                               fill = self.lockedColor)
        super().draw(canvas)


# Buttons that has both images and text -> the generate! button
class GenerateButton(Button):
    def __init__(self, x, y, width, height,
             font, text, textColor, activeColor, margins, action, image = None, color = None):
        super().__init__(x, y, width, height, action, color)
        self.text = text
        self.font = font
        self.textColor = textColor
        self.activeColor = activeColor
        size = min(width, height)
        self.image = image.resize((size, size))
        self.xMargin, self.yMargin = margins

    def draw(self, canvas):
        super().draw(canvas)
        canvas.create_image(self.x + self.xMargin,
                            self.y + self.height / 2,
                            image = ImageTk.PhotoImage(self.image),
                            anchor = "w")
        canvas.create_text(self.x + self.image.width + self.xMargin * 2,
                           self.y + self.height / 2 ,
                           text = self.text,
                           font = self.font,
                           fill = self.textColor,
                           activefill = self.activeColor,
                           anchor = "w")

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

        self.nameFont = "Verdana 10 italic"
        self.nameColor = "white"
        self.convertedName = TextureReader.convertBlockNames(self.block.name)

        self.createButtons()

    def createButtons(self):
        side = self.width // 5 # The side length of each button
        y = self.y + self.height + self.margins * 2
        x = self.x + self.width - side

        # The Move Button (2)
        action = "Drag"
        moveButton = ImageButton(x, y, side, side, action, self.icons["drag"])
        x -= (side + self.margins)
            
        # The Search Button (1)
        action = "Search"
        searchButton = ImageButton(x, y, side, side, action, self.icons["search"])
        x -= (side + self.margins)

        # The Lock Button (0)
        action = "Lock"
        lockButton = LockableButton(x, y, side, side, action,
                                    self.icons["lock"], self.icons["unlock"])
        
        self.buttons = [lockButton, searchButton, moveButton]
    
    # Determines which button has been clicked
    def checkInBounds(self, mouseX, mouseY):
        for i in range(len(self.buttons)):
            if(self.buttons[i].checkInBounds(mouseX, mouseY)):
                return i
        return False

    def draw(self, app, canvas, scale = 8):
        canvas.create_rectangle(self.x, self.y,
                                self.x + self.width, self.y + self.height,
                                width = 0,
                                fill = "dark slate blue")
        canvas.create_text(self.x + self.margins, self.y + self.margins,
                           text = self.convertedName,
                           font = self.nameFont,
                           fill = self.nameColor,
                           anchor = "nw")
        self.block.draw(app, canvas, self.x + self.width/2, self.y + self.height/2, scale)
        
        for button in self.buttons:
            button.draw(canvas)

    def setBlock(self, block):
        self.block = block
        self.convertedName = TextureReader.convertBlockNames(self.block.name)


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
            print("button checked!")
            if button.checkInBounds(mouseX, mouseY): # If a button was in bounds
                print("in bounds!")
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