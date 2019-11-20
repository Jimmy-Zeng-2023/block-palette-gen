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

#################################################
# The Block class represents a Minecraft block.
# Its purpose is mainly to serve as a data structure.
#################################################
class Block(object):
    def __init__(self, name, colors, noise, textures):
        self.name = name
        self.colors = colors # Color is a set of the most prominant colors
        self.noise = noise # Noise is a number 1-10 that classifies the level of noise
        self.textures = textures # Texture is a list of image objects relating to the faces

    def __repr__(self):
        if(len(self.colors) > 3):
            return f"{self.name} block. Noise factor = {self.noise}.\n Colors = {self.colors[:3]} and {len(self.colors) - 3} more..."
        else:
            return f"{self.name} block. Noise factor = {self.noise}.\n Colors = {self.colors}."

    def __eq__(self, other):
        return (isinstance(other, Block) and
                self.name == other.name)

    def __hash__(self):
        hashables = (self.name, self.colors, self.noise)
        return hash(hashables)

    def draw(self, app, canvas, x, y, scale):
        #Advanced: want to draw in 3D w/ 3 images

        texture = app.scaleImage(self.textures, scale)
        canvas.create_image(x, y, image = ImageTk.PhotoImage(texture))