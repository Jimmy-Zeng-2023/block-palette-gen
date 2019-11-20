from cmu_112_graphics import *
from tkinter import *
from PIL import Image
import random, math, copy, string, time, os
from Block import *
from TextureDisplayApp import *

def rgbString(red, green, blue):
    # Don't worry about how this code works yet.
    return "#%02x%02x%02x" % (red, green, blue)

class ColorDisplayApp(App):
    def appStarted(self):
        path = "Block-textures-vanilla-1.14.4"
        self.reader = TextureReader(3, path)
        self.blocks = self.reader.parseFiles(path)
        print("Loading Complete!")
        self.i = 500
        self.changeTexture()
        self.timerDelay = 2
    
    def changeTexture(self):
        self.currentTexture = self.blocks[self.i].textures
        self.colors = self.currentTexture.getcolors(maxcolors = 10**6)
        #print(self.colors)
        print()
        print(self.blocks[self.i].name, ", i =", self.i)
        for (count, color) in self.colors:
            print(f"{color} with count {count}")
        self.currentTexture = self.scaleImage(self.currentTexture, 20)

    def keyPressed(self, event):
        if(event.key == 'Right'):
            self.i += 1
            self.changeTexture()
        elif(event.key == "Left" and self.i > 0):
            self.i -= 1
            self.changeTexture()

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

            if(not isinstance(thisColor, tuple)):
                print("Error: encountered not a tuple")
                continue
            
            thisColorStr = rgbString(thisColor[0], thisColor[1], thisColor[2])
            canvas.create_rectangle(x, y, x + s, y + s, fill = thisColorStr, width = 0)
            y += 30
            if(y > 350):
                y = 0
                x += 30

        modeColor = self.blocks[self.i].colors
        if(not isinstance(modeColor, tuple)):
            print("Error: encountered not a tuple")
            modeColorStr = "White"
        else:
            modeColorStr = rgbString(modeColor[0], modeColor[1], modeColor[2])
        
        canvas.create_rectangle(600, 400, 660, 460,
                                fill = modeColorStr)

myApp = ColorDisplayApp(width = 800, height = 500)