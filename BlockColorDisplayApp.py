#################################################
# 15-112 Term Project: Minecraft Block Palette Generator by Jimmy Zeng

# Inspired by online color palette generators like Colormind.io, this project
# aims to generate a list of minecraft blocks that work well with each other in
# any build based on their textures and colors.
#
# Your name: Jimmy Zeng
# Your andrew id: jimmyzen
#################################################

from cmu_112_graphics import *
from tkinter import *
from PIL import Image
from Block import *
from TextureReader import *
import random, math, copy, string, time, os

## From Class Notes: Graphics Part 2
def rgbString(red, green, blue):
    # Don't worry about how this code works yet.
    return "#%02x%02x%02x" % (red, green, blue)

#################################################
# The ColorDisplayApp allows one to go through each block in the loaded
# Texturepack and view their colors and noise. Press left and right to navigate.

# Citation: The App class comes from cmu-112-graphics, from Course Notes: Animations Part 2
#################################################
class ColorDisplayApp(App):
    def appStarted(self):
        #path = "Block-textures-vanilla-1.14.4"
        path = "Bare-bones-textures"
        self.reader = TextureReader(100, path)
        blockDict = self.reader.parseFiles(path)
        self.blocks = list(blockDict.values())
        print("Loading Complete!")
        self.i = 0
        self.printBlockNames = True
        self.printColorDetails = False
        self.unwantedBlocks = []
        self.changeTexture()
    
    def changeTexture(self):
        self.currentTexture = self.blocks[self.i].texture

        self.colors = self.currentTexture.getcolors(maxcolors = 10**6)
        
        if(self.printBlockNames):
            print()
            print(self.blocks[self.i].name, ", i =", self.i)

        if(self.printColorDetails):
            for (count, color) in self.colors:
                print(f"{color} with count {count}")

        self.currentTexture = self.scaleImage(self.currentTexture, 3)

    def keyPressed(self, event):
        if(event.key == 'Right' and self.i < len(self.blocks) - 1):
            self.i += 1
            self.changeTexture()
        elif(event.key == "Left" and self.i > 0):
            self.i -= 1
            self.changeTexture()
        elif(event.key == "f"):
            name = self.blocks[self.i].name
            print(f"{name} stoed!")
            self.unwantedBlocks.append(name)
        elif(event.key == "k"):
            print("List Undoed!")
            self.unwantedBlocks.pop()
        elif(event.key == "r"):
            print("=======================================")
            print("Here's the list of blocks to change:")
            for name in self.unwantedBlocks:
                print(name) 

    def redrawAll(self, canvas):
        canvas.create_image(50,50, image = ImageTk.PhotoImage(self.currentTexture), anchor = 'nw')

        if(not isinstance(self.colors[0][1], tuple)):
            print("Error: not a tuple")
            print(self.colors)
            return
        elif(len(self.colors[0][1]) < 2):
            print("Error: tuple too short")
            return

        x, y, s = 600, 0, 30
        for i in range(len(self.colors)):
            thisColor = self.colors[i][1] # (count, colors)
            # Blocks that breaks it: Melons and pumpkin stems (i = 14 and i = 439)
            # Redstone blocks? (i = 459)
            # Default shulker boxes (503)
            # Slime blocks (504)
            # These have a color in format of [(2, 4), (1, 3), etc.]

            if(not isinstance(thisColor, tuple) or len(thisColor) <= 2):
                print("Error: encountered not a tuple")
                continue
            
            thisColorStr = rgbString(thisColor[0], thisColor[1], thisColor[2])
            canvas.create_rectangle(x, y, x + s, y + s, fill = thisColorStr, width = 0)
            y += 30
            if(y > 350):
                y = 0
                x += 30

        modeColor = self.blocks[self.i].colors
        if(not isinstance(modeColor, tuple) or len(modeColor) <= 2):
            modeColorStr = "green2"
        else:
            modeColorStr = rgbString(modeColor[0], modeColor[1], modeColor[2])
        
        canvas.create_rectangle(600, 400, 660, 460,
                                fill = modeColorStr)
        block = self.blocks[self.i]
        canvas.create_text(600, 470, anchor = 'nw', 
                           text = f"Noise Factor = {block.noise}\n" +
                                  f"Colors = {block.colors}\n" +
                                  f"{block.name}\n" +
                                  f"i = {self.i}",
                           font = "Arial 14")

myApp = ColorDisplayApp(width = 1000, height = 600)