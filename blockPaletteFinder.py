#################################################
# 15-112 Term Project: Minecraft Block Palette Generator by Jimmy Zeng

# Inspired by online color palette generators like Colormind.io, this project
# aims to generate a list of minecraft blocks that work well with each other in
# any build based on their textures and colors.
#
# Your name: Jimmy Zeng
# Your andrew id: jimmyzen
#################################################

from tkinter import *
from cmu_112_graphics import *
from PIL import *
import random, math, copy, string, time, os

# TODO 1: To be able to parse files, and print out the colors
# TODO 2: Given a console input, print a list of blocks w/ complimentary or similar colors


class Block(object):
    def __init__(self, name, color):
        self.name = name
        self.color = color # Color is an rgb string or # code



class TextureReader(object):
    def __init__():
        pass
        #Should contain a error epsilon, file paths, etc

    def parseFiles(path):
        blocks = []
        pass
        #Follow the format in class, base case -> finds a png file

    def analyzeBlock(path):
        pass
        #Given the path, open the image via PIL and derive the block's main colors
        #(colors too close together are ignored)

# Given a color, find its complementary
def findComplementary(): pass

def findTriatics(): pass

# Given a color, find the block that has the color as one of its primaries
def findBlockFromColor(): pass


def unusedFunction()
    # Data structure #1: Dictionary keyed by block names
    # Need to search color values
    # name              colors              noise index
    {'acacia-planks' : (Red1, Orange1, Red2, 1)}

    # Data structure #2: List of block objects
    # name                 colors                noise index
    Block('acacia-planks', (Red1, Orange1, Red2), 1)