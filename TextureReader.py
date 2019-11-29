#################################################
# 15-112 Term Project: Minecraft Block Palette Generator by Jimmy Zeng

# Inspired by online color palette generators like Colormind.io, this project
# aims to generate a list of minecraft blocks that work well with each other in
# any build based on their textures and colors.
#
# Your name: Jimmy Zeng
# Your andrew id: jimmyzen
#################################################

from PIL import Image
from Block import *
from operator import itemgetter # Itemgetter class
import random, math, copy, string, time, os

# TODO: Switch to dict based data structure

## From Class Notes: Strings, Basic File I/O
def readFile(path):
    with open(path, "rt") as f:
        return f.read()

#################################################
# The TextureReader takes in the raw textures, derive their colors and noise
# factors, and organizes them for the rest of the classes.

# Citation: PIL.Images for image manipulation options. From the Python Imaging Library
#################################################
class TextureReader(object):
    def __init__(self, colorEpsilon, path):
        # Initializes the error epsilon, and texture pack's path
        self.colorEpsilon = colorEpsilon
        self.path = path
        self.blacklistPath = "blacklist.txt"
        self.getBlackList()

    def getBlackList(self):
        self.blacklist = set()
        blacklistStr = readFile(self.blacklistPath)
        for name in blacklistStr.splitlines():
            self.blacklist.add(name)

    def parseFiles(self, path):
        blocks = dict()
        # Follow the format in class, base case -> finds a png file
        # Files are currently stored as a list of Block objects,
        # in the future I will emigrate to a dictionary structure

        if(os.path.isfile(path)):
            (head, fileName) = os.path.split(path)
            splitFileName = fileName.split('.')
            name = splitFileName[0]
            extension = splitFileName[-1]
            # We dont want .mcMeta files (yet), those are for animated textures
            if(extension == 'png' and name not in self.blacklist):
                texture = Image.open(path).convert("RGBA")
                sideLength = texture.width
                texture = texture.crop((0, 0, sideLength, sideLength))
                colors, noise = self.getColorsAndNoise(texture)

                return {name : Block(name, colors, noise, texture)}
                #return [Block(name, colors, noise, texture)]
            else:
                return dict()
                #return []
        else:
            for fileName in os.listdir(path):
                subBlocks = self.parseFiles(path + os.sep + fileName)
                blocks.update(subBlocks)
                #blocks += subBlocks
            return blocks

    def getColorsAndNoise(self, texture):
        #Given the path, open the image via PIL and derive the block's main colors
        #(colors too close together are ignored)

        colorLst = texture.getcolors() # Gets a list of all the colors
        noise = self.getNoise(colorLst)
        color = self.getPrimaryColor(colorLst)
        return color, noise
        

    def getPrimaryColor(self, colorLst):
        # Sorts the list of tuples by only the count element
        sortedColorLst = sorted(colorLst, key = itemgetter(0))
        mergedColors = dict()
        # Reverse loops through the list (greatest to least) and combine colors too close (based on the epsilon)
        for i in range(len(sortedColorLst)-1, 0, -1):
            count = sortedColorLst[i][0]
            color = sortedColorLst[i][1]
            for key in mergedColors:
                dR = abs(key[0] - color[0])
                dG = abs(key[1] - color[1])
                dB = abs(key[2] - color[2])
                dColor = dR + dG + dB
                if(dColor < self.colorEpsilon):
                    mergedColors[key] += count
            mergedColors[color] = count
        
        # Then, check the color with the greatest number of combined counts
        return self.getMode(mergedColors)
    
    def getMode(self, mergedColors):
        highest = 0
        highestColor = None 
        for key in mergedColors:
            if(key[0] == 0 or key[3] == 0): # Either RGB with completely black (from being converted from RBGA)
                                            # Or RGBA with 0 alpha (transparent)
               pass
            elif(mergedColors[key] > highest):
                highest = mergedColors[key]
                highestColor = key
        return highestColor

    def getNoise(self, colorLst):
        # Noise is defined by how many total colors there are in a texture
        # (For now)
        if(colorLst == None):
            return 0
        else:
            return len(colorLst)

    @staticmethod
    def convertBlockNames(name):
        newStr = ""
        charcount = 0
        maxChars = 18 # Maximum characters before line break
        for s in name.split('_'):
            charcount += len(s)
            if(charcount > maxChars):
                newStr += '\n'
                charcount = 0
            newStr += s.capitalize()
            newStr += ' '
            charcount += 1
        return newStr
        