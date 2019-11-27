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

# My other classes
from Block import *
from TextureReader import *

## From Class Notes: Graphics Part 2
def rgbString(red, green, blue):
    # Don't worry about how this code works yet.
    return "#%02x%02x%02x" % (red, green, blue)

#################################################
# The State is another storage object, holding a list of 5 blocks last generated
# to be displayed.
#################################################

class State(object):
    def __init__(self, blocks, locked = set()):
        self.blocks = blocks # List of blocks
        self.locked = locked # set of indices locked currently

    def __iter__(self):
        return tuple(self.blocks)

    def __str__(self):
        toPrint = ""
        toPrint += "\n==== Current State ====\n"
        for block in self.blocks:
            toPrint = toPrint + str(block) + "\n"
        toPrint += f"Indices {self.locked} Locked, [{len(self.locked)}/5]"
        return toPrint

#################################################
# The BlockGenerator generates matching blocks when provided with
# a base block. This is the key to the palette generator.
#################################################
class BlockGenerator(object):
    # This function is responsible for generating the blocks
    def __init__(self, blocks, noiseEpsilon = 10):
        self.blocks = blocks
        self.noiseEpsilon = noiseEpsilon
        self.placeholder = Block("placeholder",
                                  (0, 0, 0),
                                  0,
                                  Image.new("RGBA", (1, 1)))

    # Generates a new State 
    def generate(self, state):
        newBlocks = []
        nToGen = 0
        locked = state.locked
        for i in range(5):
            if(i in locked):
                newBlocks.append(state.blocks[i])
            else:
                newBlocks.append(self.placeholder)
                nToGen += 1

        # If there were no locked values, add a random one to start
        if(len(locked) == 0):
            newBlocks[0] = self.generateRandomBlock(state, newBlocks)
            nToGen -= 1

        if(nToGen != 0):
            generatedBlocks = self.generateFromBlocks(newBlocks, nToGen, state)

        for i in range(len(newBlocks)):
            if(newBlocks[i] == self.placeholder):
                block = generatedBlocks[0]
                newBlocks[i] = block
                generatedBlocks.pop(0)
        
        
        result = State(newBlocks, locked)
        print(result)
        return result

    def generateRandomBlock(self, state, newBlocks):
        randColor = [random.randint(1,255) for _ in range(3)]
        randNoise = random.randint(1,40)
        return self.findBlockFromColor(state, newBlocks, randColor, randNoise)

    def generateFromBlocks(self, newBlocks, nToGen, state):
        # Average the colors from newBlocks in a 3-tuple
        average = self.averageColors(newBlocks)
        complement = self.findComplementary(average)
        noise = self.averageNoise(newBlocks)

        dR = complement[0] - average[0] + random.randint(-40, 40)
        dG = complement[1] - average[1] + random.randint(-40, 40)
        dB = complement[2] - average[2] + random.randint(-40, 40)

        '''print(f"Average Col was {average}\n",
              f"Complement was {complement}\n",
              f"dR = {dR}, dG = {dG}, dB = {dB}\n")'''
               
        stepR = dR // nToGen
        stepG = dG // nToGen
        stepB = dB // nToGen

        generatedBlocks = []
        blocksToCheck = copy.copy(newBlocks)
        for i in range(nToGen):
            color = (stepR * i + average[0] + random.randint(-20, 20),
                     stepG * i + average[1] + random.randint(-20, 20),
                     stepB * i + average[2] + random.randint(-20, 20))
            block = self.findBlockFromColor(state, blocksToCheck, color, noise)
            generatedBlocks.append(block)
            blocksToCheck.append(block)
        return generatedBlocks

    # Returns the averages of the colors
    def averageColors(self, blocks):
        (totalR, totalG, totalB) = (0, 0, 0)
        n = 0
        for block in blocks:
            if(block == self.placeholder): continue

            (R, G, B) = block.colors[0:3]
            totalR += R
            totalG += G
            totalB += B
            n += 1
        totalR //= n
        totalG //= n
        totalB //= n
        return (totalR, totalG, totalB)

    # Returns the average noise
    def averageNoise(self, blocks):
        totalNoise = 0
        n = 0
        for block in blocks:
            if(block == self.placeholder): continue
            totalNoise += block.noise
            n += 1
        return totalNoise // n
        
    # Find the complement
    def findComplementary(self, color):
        (red, green, blue) = color
        return (255 - red, 255 - green, 255 - blue)
       
    # Finds 2 analogous colors (maybe)
    def findAnalogous(self, color):
        highest = max(color[:3])
        higherColor = []
        for i in range(3):
            variation = 20
            if(color[i] == highest):
                newElement = color[i] - variation
            else:
                newElement = color[i] + variation

            if(newElement > 255):
                newElement = 255
            higherColor.append(newElement)

        '''lowerColor = []
        for i in range(3):
            newElement = color[i] - 50 - random.randint(1,50)
            if(newElement < 0):
                newElement = 0
            lowerColor.append(newElement)'''
        return tuple(higherColor)
        
    def findTriadics(self): pass

    # Given a color and a noise, finds the block closest to that color within acceptable noise
    def findBlockFromColor(self, state, newBlocks, color, noise):
        lowest = 255*3
        lowestBlock = self.blocks[0]
        for block in self.blocks:
            dR = abs(color[0] - block.colors[0])  
            dG = abs(color[1] - block.colors[1])
            dB = abs(color[2] - block.colors[2])
            dColor = dR + dG + dB
            dNoise = abs(block.noise - noise)
            if(block not in newBlocks and
               block not in state.blocks and
               dColor < lowest and
               dNoise < self.noiseEpsilon):
                lowest = dColor
                lowestBlock = block
        return lowestBlock