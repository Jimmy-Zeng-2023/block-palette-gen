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
from TextureDisplayApp import *
import random, math, copy, string, time, os

## From Class Notes: Graphics Part 2
def rgbString(red, green, blue):
    # Don't worry about how this code works yet.
    return "#%02x%02x%02x" % (red, green, blue)

#################################################
# The ColorDisplayApp allows one to go through each block in the loaded
# Texturepack and view their colors and noise. Press left and right to navigate.
#################################################
class ColorDisplayApp(App):
    def appStarted(self):
        path = "Block-textures-vanilla-1.14.4"
        self.reader = TextureReader(3, path)
        self.blocks = self.reader.parseFiles(path)
        print("Loading Complete!")
        self.i = 16
        self.printBlockNames = True
        self.printColorDetails = False
        self.unwantedBlocks = []
        self.changeTexture()
    
    def changeTexture(self):
        self.currentTexture = self.blocks[self.i].textures
        self.colors = self.currentTexture.getcolors(maxcolors = 10**6)
        
        if(self.printBlockNames):
            print()
            print(self.blocks[self.i].name, ", i =", self.i)
        if(self.printColorDetails):
            for (count, color) in self.colors:
                print(f"{color} with count {count}")
        self.currentTexture = self.scaleImage(self.currentTexture, 20)

    def keyPressed(self, event):
        if(event.key == 'Right' and self.i < 607):
            self.i += 1
            self.changeTexture()
        elif(event.key == "Left" and self.i > 0):
            self.i -= 1
            self.changeTexture()
        elif(event.key == "f"):
            name = self.blocks[self.i].name
            print(f"{name} blacklisted!")
            self.unwantedBlocks.append(name)
        elif(event.key == "k"):
            print("Blacklist Undoed!")
            self.unwantedBlocks.pop()
        elif(event.key == "r"):
            print("=======================================")
            print("Here's the list of blacklisted blocks:")
            for name in self.unwantedBlocks:
                print(name) 

    def redrawAll(self, canvas):
        canvas.create_image(0,0, image =  ImageTk.PhotoImage(self.currentTexture), anchor = 'nw')

        x, y, s = 600, 0, 30
        for i in range(len(self.colors)):
            thisColor = self.colors[i][1]
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
        canvas.create_text(600, 460, anchor = 'nw', 
                           text = f"Noise Factor = {self.blocks[self.i].noise}",
                           font = "Helvetica 20 bold")

myApp = ColorDisplayApp(width = 1000, height = 600)