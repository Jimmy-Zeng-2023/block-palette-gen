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
import random, math, copy, string, time, os

class Block(object):
    # Represents a block
    def __init__(self, name, colors, noise, textures):
        self.name = name
        self.colors = colors # Color is a set of the most prominant colors
        self.noise = noise # Noise is a number 1-10 that classifies the level of noise
        self.textures = textures # Texture is a set of image objects relating to the faces

    def __repr__(self):
        if(len(self.colors) > 3):
            return f"{self.name} block. Noise factor = {self.noise}.\n Colors = {self.colors[:3]} and {len(self.colors) - 3} more..."
        else:
            return f"{self.name} block. Noise factor = {self.noise}.\n Colors = {self.colors}."

    def __eq__(self, other): pass
    def __hash__(self): pass