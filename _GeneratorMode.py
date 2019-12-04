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
import PIL
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

        #path = self.app.paths["textures"]
        #self.myReader = TextureReader(50, path)
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
            "helpPanel" : (20, 430, 50, "gold", "Verdana 12 bold")
        }

        # Info for dragging
        self.dragPanel = None
        self.dragStart = 0
        self.dragDelta = 0

        self.setBackground()
        self.createButtons()
        self.createPanels()
        self.createSearchPanel()
        self.createHelpPanel()
        self.generatePalette()

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
        x, y, width, height = self.ui["genModeButton"]
        self.genModeButton = ImageButton(x, y, width, height)
        
        x, y, width, height = self.ui["presetButton"]
        self.presetButton = ImageButton(x, y, width, height)

        x, y, width, height = self.ui["generateButton"]
        x = self.width - self.ui["panels"][0] - width - 30
        sprite = self.app.ui_images["generateButton"]
        self.generateButton = ImageButton(x, y, width, height, sprite)

    def createSearchPanel(self):
        # Makes the search panel. (not visible yet)
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
        lockIcon =  self.app.ui_images["unlock"]
        searchIcon = self.app.ui_images["search"]
        dragIcon = self.app.ui_images["drag"]
        self.dummyIcons = [lockIcon, searchIcon, dragIcon]

        self.helpText = ("Lock a block to keep it constant while generating.\n" + 
            "Search for a specific block.\n" +
            "Drag the order of the blocks around.")
        
        self.bottomText = ("Use the 'Generate!' button to make a new color palette!\n" + 
            "   locked blocks won't be replaced.\n" +
            "Use to 'Presets' button to accept pre-built color palettes!")

    def toggleSearchPanel(self):
        # Make the search panel visible on screen.
        self.searchPanel.visible = not self.searchPanel.visible
        self.panels[self.searchingIndex].isSearching = not self.panels[self.searchingIndex].isSearching
        self.searching = not self.searching

    def endSearch(self): # Terminates a search
        if(self.searching):
            self.searching = False
            self.searchPanel.visible = False
            self.panels[self.searchingIndex].isSearching = False
            self.searchingIndex = None

##################################
#      Controller Helpers        #
##################################

    def updatePanels(self):
        for i in range(len(self.app.state.blocks)):
            block = self.app.state.blocks[i]
            panel = self.panels[i]
            panel.setBlock(block)

    def generatePalette(self):
        self.app.state = self.myGen.generate(self.app.state)
        self.updatePanels()

    def changeMode(self):
        self.app.setActiveMode(self.app.presets)
        self.app.sizeChanged()
    
    def checkSearching(self, mouseX, mouseY):
        # Returns true when the search box has finished
        selectedBlock = self.searchPanel.checkButtonClick(self, mouseX, mouseY)
        if(selectedBlock == "searchFailed"): 
            self.searchFail = True
            self.searchFailCounter += 3 * 20
            return False
        elif(selectedBlock == None):
            return False
        elif(selectedBlock == "exit"):
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
        # Used by mouseDragged. During dragging
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

    def mouseDragged(self, event):
        if(self.dragPanel == None): return

        self.dragPanel.deltaX = event.x - self.dragStart
        # Move stuff
        
        oldLeft = self.dragPanelStartX
        newLeft = self.dragPanelStartX + self.dragPanel.deltaX
        oldRight = oldLeft + self.dragPanel.width
        newRight = newLeft + self.dragPanel.width
        for panel in self.panels:
            if(panel == self.dragPanel): continue # Exclude the panel being repositioned

            panelMid = panel.x + panel.width//2 + panel.deltaX
            otherPanelsX = self.findOtherPanelsX(panel)
            minX = self.ui["panels"][0]
            maxX = self.width - self.ui["panels"][0]

            if(oldRight < panelMid and newRight > panelMid):
                panel.decDelta(otherPanelsX, minX, maxX) # Shift panel left
            elif(oldLeft > panelMid and newLeft < panelMid):
                panel.incDelta(otherPanelsX, minX, maxX) # Shift panel right

    def mouseReleased(self, event):
        if(self.dragPanel != None):
            # Snaps the current panel to the grid
            self.dragPanel.deltaX = event.x - self.dragStart
            self.dragPanel.shiftInSteps()
            
            print("Deltas Locked in! New X =", end = " ")
            for panel in self.panels:
                panel.lockInDelta()
                print(panel.x, end = " ")
            
            self.dragStart = 0
            self.dragPanel = None
        
    def sizeChanged(self):
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
        if(self.searching): return

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
        # Animations
        # Help Panel
        self.drawHelpPanel(canvas)
        # Search Panel
        self.drawSearchPanel(canvas)
