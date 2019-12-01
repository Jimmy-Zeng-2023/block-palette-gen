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

        # For greenery and foilage. See addGreenLayer()
        
        self.foilage = {"oak_leaves", "birch_leaves", "spruce_leaves",
                        "jungle_leaves", "dark_oak_leaves", "acacia_leaves"}
        self.foilageColors = {
            "grass" : (1,1,1),
            "oak_leaves" : (70/186, 103/186, 28/186),
            "birch_leaves" : (75/184, 99/184, 50/184),
            "spruce_leaves" : (47/154, 74/154, 47/154),
            "jungle_leaves" : (36/218, 132/218, 6/218),
            "dark_oak_leaves" : (52/184, 103/184, 28/184),
            "acacia_leaves" : (101/181, 95/181, 25/181)
        }

    def getBlackList(self):
        self.blacklist = set()
        blacklistStr = readFile(self.blacklistPath)
        for name in blacklistStr.splitlines():
            self.blacklist.add(name)

    def parseFiles(self, path):
        # Similar to the listFiles() function from Class Notes: Recursion Part 2
        # Recursively searches target path and load the blocks into a dictionary
        blocks = dict()
        
        if(os.path.isfile(path)):
            (head, fileName) = os.path.split(path)
            splitFileName = fileName.split('.')
            name = splitFileName[0]
            extension = splitFileName[-1]
            # We dont want .mcMeta files (yet), those are for animated textures
            if(extension == 'png' and name not in self.blacklist):
                
                if(name in self.foilage):
                    # Vegetation blocks (leaves and grass) are stored as grayscale files
                    # by Minecraft. We need to add the green color manually.
                    texture = Image.open(path).convert("L")
                    texture = self.addGreenLayer(name, texture)
                else:
                    texture = Image.open(path).convert("RGBA")

                sideLength = texture.width
                texture = texture.crop((0, 0, sideLength, sideLength))
                colors, noise = self.getColorsAndNoise(texture)

                return {name : Block(name, colors, noise, texture)}
            else:
                return dict()
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

    def addGreenLayer(self, name, texture):
        # Vegetation blocks (leaves and grass) are stored as grayscale files
        # by Minecraft. We need to add the green color manually.
        
        color = self.foilageColors[name]

        texture = texture.convert('L')
        texture2 = Image.new('RGBA', texture.size, (0,0,0,0))

        pixdata = texture.load()
        pixdata2 = texture2.load()

        width, height = texture.size

        # Code Idea borrowed from: 
        # https://stackoverflow.com/questions/765736/using-pil-to-make-all-white-pixels-transparent
        # 
        # This loops through all the pixels and transforms the Luminosity values
        # to RGBA values according to the colors defined in self.foilageColors.
        for y in range(height):
            for x in range(width):
                if pixdata[x, y] == 0:
                    # 0 = Completely black
                    pixdata2[x, y] = (0,0,0,0)
                else:
                    factor = pixdata[x, y]
                    R = int(color[0] * factor)
                    G = int(color[1] * factor)
                    B = int(color[2] * factor)
                    pixdata2[x, y] = (R, G, B, 255)

        texture.close()

        return texture2


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
        