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
from _PresetMode import *

from Buttons import *
from BlockPanel import *
from SearchPanel import *
from PresetPanel import *

#################################################
#
#              -= THE GENERATOR MODE =-
#
# The Generator Mode is the main mode of the application.
# It is responsible for generate color palettes, locking, searching, and dragging.
# It also displays a series of help messages.
#
# Citation: The Mode and ModalApp classes come from cmu-112-graphics, from Course Notes: Animations Part 2
#################################################
class GeneratorMode(Mode):
    # Final frontend app
    def appStarted(self):

        self.blocks = self.app.blocks
        self.myGen = self.app.myGen

        self.ui = {
            "smallFont" : "Verdana 10",
            "medFont" : "Verdana 12 bold",
            "largeFont" : "Verdana 18 bold",
            "genModeButton" : (79, 55, 172, 50),
            "presetButton" : (290, 55, 154, 50),
            "generateButton" : (670, 430, 200, 50),
            "panels" : (20, 170, 200),
            "helpPanel" : (20, 430, 50, "gold", "Verdana 12"),
            "showHelpPanel" : True
        }

        # Info for dragging
        self.dragPanel = None
        self.dragStart = 0
        self.dragDelta = 0

        # Creates all the different UI elements
        self.setBackground()
        self.createButtons()
        self.createPanels()
        self.createSearchPanel()
        self.createHelpPanel()

        # Generates the first palette!
        self.generatePalette()

##################################
#     appStarted() Helpers       #
##################################        

    def setBackground(self):
        self.background = self.app.ui_images["Bg_Normal"]
        self.bgMiddle = self.background.crop((480, 0, 1400, 1009))

    def createPanels(self):
        # Block Panels hold the 3D block images
        self.panels = []
        panelX, panelY, panelHeight = self.ui["panels"]
        panelWidth = (self.width - 2*panelX) // 5
        
        for block in self.app.state.blocks:
            panel = BlockPanel(panelX, panelY,
                               panelWidth - 10,
                               panelHeight,
                               self.app.ui_images,
                               block = block)
            self.panels.append(panel)
            panel.setDeltaGrid(panelWidth)

            panelX += panelWidth

    def createButtons(self):
        # There are 3 top-level buttons: 2 for changing modes, and 1 for generating
        x, y, width, height = self.ui["genModeButton"]
        self.genModeButton = ImageButton(x, y, width, height)
        
        x, y, width, height = self.ui["presetButton"]
        self.presetButton = ImageButton(x, y, width, height)

        x, y, width, height = self.ui["generateButton"]
        x = self.width - self.ui["panels"][0] - width - 30
        sprite = self.app.ui_images["generateButton"]
        self.generateButton = ImageButton(x, y, width, height, sprite)

    def createSearchPanel(self):
        # Makes the search panel. (starts off invisible)
        self.searching = False
        x = self.ui["panels"][0]
        y = self.ui["panels"][1] + self.ui["panels"][2] + 40
        width = self.width - x*2 - 10
        height = self.height - y - 10
        self.searchPanel = SearchPanel(x, y, width, height, self.blocks, self.app.ui_images)
        
        self.searchingIndex = None # This is the block panel currently searching
        self.searchFail = False
        self.searchFailCounter = 0

    def createHelpPanel(self):
        # A series of helpful messages!
        lockIcon =  self.app.ui_images["unlock"]
        searchIcon = self.app.ui_images["search"]
        dragIcon = self.app.ui_images["drag"]
        self.dummyIcons = [lockIcon, searchIcon, dragIcon]

        self.helpText = ("Lock a block to keep it constant while generating.\n" + 
            "Search for a specific block.\n" +
            "Drag the order of the blocks around.")
        
        self.bottomText = ("Use the 'Generate!' button to make a new color palette!\n" + 
            "   -> locked blocks won't be replaced.\n" +
            "Use the 'Presets' button to load in pre-built color palettes!")

    def toggleSearchPanel(self):
        # Make the search panel visible on screen.
        self.searchPanel.visible = not self.searchPanel.visible
        self.panels[self.searchingIndex].isSearching = not self.panels[self.searchingIndex].isSearching
        self.searching = not self.searching

    def endSearch(self):
        # Terminates a search
        if(self.searching):
            self.searching = False
            self.searchPanel.visible = False
            self.panels[self.searchingIndex].isSearching = False
            self.searchingIndex = None

##################################
#      Controller Helpers        #
##################################

    def updatePanels(self):
        # When the state changes, the block panels must change their items as well.
        for i in range(len(self.app.state.blocks)):
            block = self.app.state.blocks[i]
            panel = self.panels[i]
            panel.setBlock(block)

    def generatePalette(self):
        # When the generate button is pressed
        self.app.state = self.myGen.generate(self.app.state)
        self.updatePanels()

    def changeMode(self):
        # When the presets button is pressed
        self.app.setActiveMode(self.app.presets)
        self.app.sizeChanged()
    
    def checkSearching(self, mouseX, mouseY):
        # Runs when the search panel is active.
        # Returns True if the search panel needs to be closed.
        selectedBlock = self.searchPanel.checkButtonClick(self, mouseX, mouseY)
        if(selectedBlock == "searchFailed"):
            # User searched by typing in a phrase, but that phrase cannot be recognized. 
            self.searchFail = True
            self.searchFailCounter += 3 * 20
            return False
        elif(selectedBlock == None):
            return False
        elif(selectedBlock == "exit"):
            # Click out of bounds
            self.toggleSearchPanel()
            self.searchingIndex = None
            return True
        else:
            # A search has completed
            assert(isinstance(selectedBlock, Block))
            #print(f"Detected click on {selectedBlock}")

            self.panels[self.searchingIndex].setBlock(selectedBlock)
            self.app.state.blocks[self.searchingIndex] = selectedBlock
            self.app.state.locked.add(self.searchingIndex)
            self.panels[self.searchingIndex].lockButton.lock(forceLock = True)
            
            self.endSearch()
            return True

    def checkButtons(self, mouseX, mouseY):
        # Checks the 3 top-level buttons
        searchFinish = False
        if(self.searching):
            # The searching check must run first to stop the panel from closing instantly
            searchFinish = self.checkSearching(mouseX, mouseY)

        if(self.genModeButton.checkInBounds(mouseX, mouseY)):
            pass
        elif(self.presetButton.checkInBounds(mouseX, mouseY)):
            self.changeMode()
        elif(searchFinish): return
            # If the search finished, end here
         
        elif(self.generateButton.checkInBounds(mouseX, mouseY) and not self.searching):
            # The generate button should be halted as well
            self.generatePalette()

    def checkPanels(self, mouseX, mouseY):
        # Checks the block panels and the search panel
        for i in range(len(self.panels)):
            panel = self.panels[i]
            if(i == self.searchingIndex):
                # If the search menu is open on this panel, these buttons won't be visible.
                continue

            elif(panel.checkInBounds(mouseX, mouseY) == "lock"):
                if(i not in self.app.state.locked):
                    self.app.state.locked.add(i)
                else:
                    self.app.state.locked.remove(i)
                #print(f"New locked indices = {self.app.state.locked}")

            elif(panel.checkInBounds(mouseX, mouseY) == "search"):
                self.searchingIndex = i
                self.toggleSearchPanel()
            
            elif(panel.checkInBounds(mouseX, mouseY) == "drag"):
                self.dragPanel = panel
                self.dragStart = mouseX # On the drag, we only care about the x coordinates.
                self.dragPanelStartX = self.dragPanel.x

    def findOtherPanelsX(self, curPanel):
        # Used by mouseDragged. As the user drags
        result = []
        for panel in self.panels:
            if(panel != self.dragPanel and panel != curPanel):
                result.append(panel.x + panel.deltaX)
        return result

##################################
#     Top Level Controllers      #
##################################

    def timerFired(self):
        # Used for animations

        # Counts down from 100 ticks to 0 ticks, then swaps away the message
        if self.searchFailCounter > 0:
            self.searchFailCounter -= 1
        else:
            self.searchFail = False

    def keyPressed(self, event):
        if(event.key == 'r'):
            self.generatePalette()
        elif(event.key == 'f'):
            print(f"New locked indices = {self.app.state.locked}")
    
    def mousePressed(self, event):
        #print(event.x, event.y)
        #print(self.searching, self.searchingIndex)
        self.checkButtons(event.x, event.y)
        self.checkPanels(event.x, event.y)

    def mouseDragged(self, event):
        # Used in dragging
        if(self.dragPanel == None): return

        self.dragPanel.deltaX = event.x - self.dragStart

        # Checks each panel to see if they needs to be moved to make space        
        oldLeft = self.dragPanelStartX
        newLeft = self.dragPanelStartX + self.dragPanel.deltaX
        oldRight = oldLeft + self.dragPanel.width
        newRight = newLeft + self.dragPanel.width
        for panel in self.panels:
            if(panel == self.dragPanel): continue # Exclude the panel being dragged

            panelMid = panel.x + panel.width//2 + panel.deltaX
            otherPanelsX = self.findOtherPanelsX(panel)
            minX = self.ui["panels"][0]
            maxX = self.width - self.ui["panels"][0]

            # Actually shifts the panels
            if(oldRight < panelMid and newRight > panelMid):
                panel.decDelta(otherPanelsX, minX, maxX) # Shift panel left
            elif(oldLeft > panelMid and newLeft < panelMid):
                panel.incDelta(otherPanelsX, minX, maxX) # Shift panel right

    def mouseReleased(self, event):
        # Used for dragging
        if(self.dragPanel != None):
            # Snaps the current panel to the grid
            self.dragPanel.deltaX = event.x - self.dragStart
            self.dragPanel.shiftInSteps()
            
            #print("Deltas Locked in! New X =", end = " ")
            for panel in self.panels:
                panel.lockInDelta()
                #print(panel.x, end = " ")
            
            self.dragStart = 0
            self.dragPanel = None
        
    def sizeChanged(self):
        # Resizes the UI when size of the window change
        if(self.app.width > 900):
            self.createPanels()
            self.createButtons()

            # Just so the panel doesn't destroy the info
            #prevStats = self.searching, self.searchingIndex, self.searchPanel.visible
            self.createSearchPanel()
            #self.searching, self.searchingIndex, self.searchPanel.visible = prevStats

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

    def drawHelpPanel(self, canvas):
        # Drawing the icons and texts used in the help panel
        if(self.searching or 
           self.ui["showHelpPanel"] == False): return

        startX, startY, textX, color, font = self.ui["helpPanel"]
        x = startX
        y = startY
        titleH = 40
        canvas.create_text(x, y + titleH // 2,
                           text = "Button Explanations:",
                           font = self.ui["largeFont"],
                           fill = color,
                           anchor = 'w')
        y += titleH

        dy = self.dummyIcons[0].height
        for icon in self.dummyIcons:
            canvas.create_image(x, y, image = ImageTk.PhotoImage(icon), anchor = 'nw')
            y += dy

        x = startX + textX
        y = startY + titleH
        for line in self.helpText.splitlines():
            canvas.create_text(x, y + dy//2, text = line, font = font, fill = color, anchor = 'w')
            y += dy

        x = startX
        y = startY + titleH + 3 * dy
        for line in self.bottomText.splitlines():
            canvas.create_text(x, y + dy//2, text = line, font = font, fill = 'white', anchor = 'w')
            y += dy

    def drawSearchPanel(self, canvas):
        self.searchPanel.draw(self, canvas)

        if(self.searchFail):
            canvas.create_text(self.width//2,
                               200,
                               text = "Sorry! We couldn't find that block. :(",
                               font = self.ui["largeFont"],
                               fill = "red2",
                               anchor = "n")

    def redrawAll(self, canvas):
        # Background
        self.drawBg(canvas)
        # Blocks
        self.drawBlockPanels(canvas)
        # Buttons
        self.drawButtons(canvas)
        # Not Implemented: Animations for generating
        # Help Panel
        self.drawHelpPanel(canvas)
        # Search Panel
        self.drawSearchPanel(canvas)