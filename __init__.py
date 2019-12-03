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
from _PresetMode import *

from Buttons import *
from BlockPanel import *
from SearchPanel import *
from PresetPanel import *

#################################################
# THIS IS THE MAIN FILE TO BE RUN!
#
#
#              THE MODAL APP
#
# The ModalApp ties the two modes together, and also initializes some important
# dictionaries, such as the paths to the files.
#
# Citation: The Mode and ModalApp classes come from cmu-112-graphics, from Course Notes: Animations Part 2
#################################################

class BlockPaletteGenerator(ModalApp):
    def appStarted(self):

        # Edit links to UI images here!!!
        self.paths = {
            "textures" : "Block-textures-vanilla-1.14.4",
            "Bg_Normal" : "ui-images/Bg_normal_2.png",
            "Bg_Alternate" : "ui-images/Bg_alternate_2.png",
            "search" : "ui-images/search-icon.png",
            "drag" : "ui-images/drag-icon.png",
            "lock" : "ui-images/lock-icon.png",
            "unlock" : "ui-images/unlock-icon.png",
            "generate" : "ui-images/generate-icon.png",
            "generateButton" : "ui-images/generate-button.png",
            "leftButton" : "ui-images/LeftArrow.png",
            "rightButton" : "ui-images/RightArrow.png"
        }

        self.ui_images = dict() # Creates a dictionary of the UI images
        for key in self.paths:
            if(key == "textures"): continue
            elif(key in ["search", "drag", "unlock", "lock", "leftButton", "rightButton"]):
                # These need additional "grayed out" icons. With separate keys.
                self.createInactiveIcons(key)
            else:
                self.ui_images[key] = Image.open(self.paths[key]).convert("RGBA")

        self.createReaderAndGenerator()
        self.generator = GeneratorMode()
        self.presets = PresetMode()
        self.setActiveMode(self.generator)
        self.timerDelay = 1000

    def createReaderAndGenerator(self):
        path = self.paths["textures"]
        self.myReader = TextureReader(50, path)
        self.blocks = self.myReader.parseFiles(path)
        print("Texture Loading Complete!")
        self.myGen = BlockGenerator(self.blocks, noiseEpsilon = 2)
        self.state = State([self.blocks["acacia_leaves"] for _ in range(5)])

    def createInactiveIcons(self, key):
        activeIcon = Image.open(self.paths[key]).convert("RGBA")

        if(key == "lock"):
        # In the case of lock, there is no inactive image, so the process terminates early
            activeIcon = self.scaleImage(activeIcon, 2)
            self.ui_images[key] = activeIcon
            return None
        
        colorMask = Image.new('RGBA', (activeIcon.width, activeIcon.height), 
                              color = "gray")
        inactiveIcon = Image.composite(colorMask, activeIcon, activeIcon)
        
        activeIcon = self.scaleImage(activeIcon, 2)
        inactiveIcon = self.scaleImage(inactiveIcon, 2)
        
        newKey = "inactive-" + key

        self.ui_images[key] = activeIcon
        self.ui_images[newKey] = inactiveIcon

def main():
    myPaletteGenerator = BlockPaletteGenerator(title = "Minecraft Block Palette Generator",
                                               width = 900, height = 700)

if __name__ == "__main__":
    main()