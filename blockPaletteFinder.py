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

# TODO 1: To be able to parse files, and print out the colors
# TODO 2: Given a console input, print a list of blocks w/ complimentary or similar colors


class Block(object):
    def __init__(self, name, color, image):
        self.name = name
        self.color = color # Color is an rgb string or # code
        self.texture = image

    def __repr__(self):
        return f"{self.name} block"

class TextureReader(object):
    def __init__(self):
        pass
        #Should contain a error epsilon, file paths, etc

    def parseFiles(self, path):
        blocks = []
        #Follow the format in class, base case -> finds a png file

        if(os.path.isfile(path)):
            (head, fileName) = os.path.split(path)
            splitFileName = fileName.split('.')
            name = splitFileName[0]
            extension = splitFileName[-1]
            # We dont want McMeta files (yet), those are for animated textures
            if(extension == 'png'):
                #print(path)

                texture = Image.open(path)
                color = 'green' # Temp color
                return [Block(name, color, texture)]
            else:
                return []
        else:
            for fileName in os.listdir(path):
                subBlocks = self.parseFiles(path + os.sep + fileName)
                blocks += subBlocks
            return blocks

    def analyzeBlock(path):
        pass
        #Given the path, open the image via PIL and derive the block's main colors
        #(colors too close together are ignored)

# Given a color, find its complementary
def findComplementary(): pass

def findTriatics(): pass

# Given a color, find the block that has the color as one of its primaries
def findBlockFromColor(): pass


    # Data structure #1: Dictionary keyed by block names
    # Need to search color values
    # name              colors              noise index
#    {'acacia-planks' : (Red1, Orange1, Red2, 1)}

    # Data structure #2: List of block objects
    # name                 colors                noise index
#    Block('acacia-planks', (Red1, Orange1, Red2), 1)


# This app just displays all the textures loaded
class TextureDisplayApp(App):
    def appStarted(self):
        self.myTextureReader = TextureReader()
        path = "Block-textures-vanilla-1.14.4"
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
        resizedTexture = block.texture.resize((50,50))
        canvas.create_image(col*50, row*50, image = ImageTk.PhotoImage(resizedTexture),
                            anchor = 'nw')

def main():
    myApp = TextureDisplayApp(width = 800, height = 400, title = 'Loaded Textures')    


if __name__ == "__main__":
    main()