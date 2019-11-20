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
