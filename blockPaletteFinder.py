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

def unusedFunction():
    # Data structure #1: Dictionary keyed by block names
    # Need to search color values
    # name              colors              noise index
    {'acacia-planks' : (Red1, Orange1, Red2, 1)}

    # Data structure #2: List of block objects
    # name                 colors                noise index
    Block('acacia-planks', (Red1, Orange1, Red2), 1)

    # Data structure #3: Dict of block objects indexed by names
    { 'acacia-planks' : Block(etc) }

class Block(object):
    # Represents a block
    def __init__(self, name, colors, noise, textures):
        self.name = name
        self.colors = colors # Color is a set of the most prominant colors
        self.noise = noise # Noise is a number 1-10 that classifies the level of noise
        self.textures = textures # Texture is a set of image objects relating to the faces

    def __repr__(self):
        return f"{self.name} block with noise factor of {self.noise} and colors {self.colors}"

    def __eq__(self, other): pass
    def __hash__(self): pass

class TextureReader(object):
    def __init__(self, epsilon, path):
        # Initializes the error epsilon, and texture pack's path
        self.epsilon = epsilon
        self.path = path

    def parseFiles(self, path):
        #blocks = dict()
        blocks = []
        #Follow the format in class, base case -> finds a png file
        #Files are stored as a dictionary indexed by name of the blocks, holding Block objects

        if(os.path.isfile(path)):
            (head, fileName) = os.path.split(path)
            splitFileName = fileName.split('.')
            name = splitFileName[0]
            extension = splitFileName[-1]
            # We dont want McMeta files (yet), those are for animated textures
            if(extension == 'png'):
                texture = Image.open(path)
                colors = self.getPrimaryColors(texture)
                noise = self.getNoise(texture, colors)
                #return {name : Block(name, colors, noise, texture)}
                return [Block(name, colors, noise, texture)]
            else:
                #return dict()
                return []
        else:
            for fileName in os.listdir(path):
                subBlocks = self.parseFiles(path + os.sep + fileName)
                #blocks.update(subBlocks)
                blocks += subBlocks
            return blocks

    def getPrimaryColors(self, texture):
        return texture.getcolors()
        #Given the path, open the image via PIL and derive the block's main colors
        #(colors too close together are ignored)

        # First find the colors w the highest counts
        # go down the ordered list and add to dict
        # If RGB are within 100, combine the counts
        # return the final colors that still are there

    def getNoise(self, texture, colors): return 4
        # Noise is defined by how many total colors there are in a texture
        # (For now)

class BlockGenerator(object):
    # This function is responsible for generating the blocks
    def __init__(self, blocks):
        self.blocks = blocks
        pass
        # ?

    def findComplementary(): pass
        # Given a color, find its complementary

    def findTriatics(): pass

    # Given a color, find the block that has the color as one of its primaries
    def findBlockFromColor(): pass

    # Order: 2 analogous, 1 complement and 1 analogous of complement?
    # TODO: Research color balance websites

class BlockPaletteGenerator(App):
    # Final frontend app
    def appStarted(self): pass
    def timerFired(self): pass
        # Used for animations
    def mousePressed(self, event): pass
    def redrawAll(self, canvas): pass
        # Background
        # Blocks
        # Buttons
        # Animations

# This app just displays all the textures loaded
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