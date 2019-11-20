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
import random, math, copy, string, time, os
from Block import *
from TextureReader import *
from BlockGenerator import *

#################################################
# The TextureDisplayApp shows an overview of all the textures loaded.
# Press left and right to navigate.
#################################################
class TextureDisplayApp(App):
    def appStarted(self):
        path = "Block-textures-vanilla-1.14.4"
        self.myTextureReader = TextureReader(1, path)
        self.myBlocks = self.myTextureReader.parseFiles(path)
        self.displayStartIndex = 0
        self.texPerPage = 128

    def keyPressed(self, event):
        if(event.key == 'Right'):
            if(self.displayStartIndex < len(self.myBlocks) - self.texPerPage):
                self.displayStartIndex += self.texPerPage
        elif(event.key == 'Left'):
            if(self.displayStartIndex >= self.texPerPage):
                self.displayStartIndex -= self.texPerPage

    def redrawAll(self, canvas):
        for i in range(self.displayStartIndex, self.displayStartIndex + self.texPerPage):
            row = (i - self.displayStartIndex) // 16
            col = (i - self.displayStartIndex) % 16
            if (i < len(self.myBlocks)):
                block = self.myBlocks[i]
                self.drawBlock(canvas, block, row, col)
            
    def drawBlock(self, canvas, block, row, col):
        resizedTexture = block.textures.resize((50,50))
        canvas.create_image(col*50, row*50, image = ImageTk.PhotoImage(resizedTexture),
                            anchor = 'nw')

def main():
    myApp = TextureDisplayApp(width = 800, height = 400, title = 'Loaded Textures')    

if __name__ == "__main__":
    main()