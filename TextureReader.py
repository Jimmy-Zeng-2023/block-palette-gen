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
import random, math, copy, string, time, os

# TODO: Switch to dict based data structure
# TODO: Generate a blacklist for random blocks not needed

## From Class Notes: Strings, Basic File I/O
def readFile(path):
    with open(path, "rt") as f:
        return f.read()

class TextureReader(object):
    def __init__(self, epsilon, path):
        # Initializes the error epsilon, and texture pack's path
        self.epsilon = epsilon
        self.path = path
        #self.blacklistPath = ""
        #self.blackList = readFile(blackListPath)

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
                #print(f"loading {name}...")
                colors, noise = self.getColorsAndNoise(texture)

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

    def getColorsAndNoise(self, texture):
        #Given the path, open the image via PIL and derive the block's main colors
        #(colors too close together are ignored)

        # First find the colors w the highest counts
        # go down the ordered list and add to dict
        # If RGB are within 100, combine the counts
        # return the final colors that still are there

        colorLst = texture.getcolors() # Gets a list of all the colors
        noise = self.getNoise(colorLst)
        color = self.getPrimaryColor(colorLst)
        return color, noise
        
    '''## Following from Class Notes: Recursion Part 1
    def merge(A, B):
        # iterative (ugh) and destructive (double ugh), but practical...
        C = [ ]
        i = j = 0
        while ((i < len(A)) or (j < len(B))):
            # Need to compare only the count part of the element
            # (count (RGBA))
            if ((j == len(B)) or ((i < len(A)) and (A[i][0] <= B[j][0]))):
                C.append(A[i])
                i += 1
            else:
                C.append(B[j])
                j += 1
        return C

    def mergeSortByCount(colors):
        if (len(colors) < 2):
            return L
        else:
            # No need for complicated loops- just merge sort each half, then merge!
            mid = len(colors)//2
            left = mergeSort(colors[:mid])
            right = mergeSort(colors[mid:])
            return merge(left, right)'''

    def getPrimaryColor(self, colorLst):
        return self.getMode(colorLst)
    
    def getMode(self, colorLst):
        if(colorLst == None):
            return None
        
        highestCount = 0
        mostFreqColor = None
        for (count, color) in colorLst:
            if(not isinstance(color, tuple)):
                pass
            elif((len(color) == 4) and (color[3] == 0)): # Alpha value of 0 means transparent, so ignore
                pass
            elif(count > highestCount):
                highestCount = count
                mostFreqColor = color
        return mostFreqColor

    def getNoise(self, colorLst):
        # Noise is defined by how many total colors there are in a texture
        # (For now)
        if(colorLst == None):
            return 0
        else:
            return len(colorLst)