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

## From Class Notes: Graphics Part 2
def rgbString(red, green, blue):
    # Don't worry about how this code works yet.
    return "#%02x%02x%02x" % (red, green, blue)

# The State holds a list of 5 blocks last generated and displayed.
class State(object):
    def __init__(self, blocks, locked):
        self.blocks = blocks # List of blocks
        self.locked = locked # List of indices locked currently

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
# The BlockGenerator generateS matching blocks when provided with
# a base block. This is the key to the palette generator.
#################################################
class BlockGenerator(object):
    # This function is responsible for generating the blocks
    def __init__(self, blocks, noiseEpsilon = 10):
        self.blocks = blocks
        self.noiseEpsilon = noiseEpsilon

    # Generates a new State 
    def generate(self, state):
        toGen = []
        locked = state.locked
        for i in range(5):
            if(i in locked):
                toGen.append(state[i])

        if(len(toGen) == 0):
            toGen.append(self.generateRandomBlock(state, toGen))
        while(len(toGen) < 5):
            toGen.append(self.generateBlock(state, toGen))
        return State(toGen, locked)
        print(state)

    def generateRandomBlock(self, state, toGen):
        randColor = [random.randint(1,255) for _ in range(3)]
        randNoise = random.randint(1,40)
        return self.findBlockFromColor(state, toGen, randColor, randNoise)

    def generateBlock(self, state, toGen):
        color = toGen[-1].colors
        noise = toGen[-1].noise
        analogous = self.findAnalogous(color)
        block = self.findBlockFromColor(state, toGen, analogous, noise)
        return block

    # Find the complement
    def findComplementary(self, color):
        red = color[0]
        green = color[1]
        blue = color[2]
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
    def findBlockFromColor(self, state, toGen, color, noise):
        lowest = 255*3
        lowestBlock = self.blocks[0]
        for block in self.blocks:
            dR = abs(color[0] - block.colors[0])  
            dG = abs(color[1] - block.colors[1])
            dB = abs(color[2] - block.colors[2])
            dColor = dR + dG + dB
            dNoise = abs(block.noise - noise)
            if(block not in toGen and
               block not in state.blocks and
               dColor < lowest and
               dNoise < self.noiseEpsilon):
                lowest = dColor
                lowestBlock = block
        return lowestBlock