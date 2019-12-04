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
    def __init__(self, name, colors, noise, textures, weight = 4):
        self.name = name
        self.colors = colors # Color is a set of the most prominant colors
                             # Each color is a tuple of (R, G, B) or (R, G, B, A)
        self.noise = noise # Noise is a number that classifies the level of noise
        
        # Textures is an list of images corresponding to the top, left, and right faces
        # self.texture stores the transformed cube image
        self.texture = self.transformTo3D(textures)

        self.weight = weight # Lower weight means the block shows up with elss frequency


    def transformTo3D(self, textures):
        scale = 2
        
        textures = textures.resize((16*scale, 16*scale))
        side1 = textures
        side2 = textures
        side3 = textures

        bgSize = (32*scale, 36*scale)
        bg = Image.new('RGBA', bgSize, (0, 0, 0, 0))
        
        # Top Rect:
        # Size = (x=32, y=16)
        #
        # To perform an Affine transformation, we need a 6-tuple
        # Where every (x, y) in the result maps to the point in the original defined by:
        # x = ax + by + c, y = dx + ey + f
        #
        # a = 1/2, b = 1, c = -8, e = 1, d = -1/2, f = 8
        size = (32, 16)
        size = (size[0] * scale, size[1] * scale)

        data = (1/2, 1, -8*scale, -1/2, 1, 8*scale)
        side1 = side1.transform(size, Image.AFFINE, data)

        # Bottom-left Rect:
        # Size = (x=16, y=32)
        #
        # a = 1, b = 0, c = 0, d = -1/2, e = 1, f = 0
        size = (16, 28)
        size = (size[0] * scale, size[1] * scale)

        data = (1, 0, 0, -2/5, 4/5, 0)
        side2 = side2.transform(size, Image.AFFINE, data)

        # Bottom-right Rect:
        # Size = (x=16, y=32)
        #
        # a = 1, b = 0, c = 0, d = 1/2, e = 1, f = 8  # Try adjusting e and f for ratio change
        size = (16, 28)
        size = (size[0] * scale, size[1] * scale)

        data = (1, 0, 0, 2/5, 4/5, -(32/5)*scale)
        side3 = side3.transform(size, Image.AFFINE, data)

        '''# Makes all three sides transparent
        self.clearBackground(side1)
        self.clearBackground(side2)
        self.clearBackground(side3)'''

        # Applies a shade to side 2 and side 3 to better distinguish them
        shade2 = Image.new('RGBA', side2.size, (0, 0, 0, 255))
        alpha2 = side2.getchannel('A')
        side2 = Image.blend(side2, shade2, 0.2)
        side2.putalpha(alpha2)
        
        shade3 = Image.new('RGBA', side3.size, (0, 0, 0, 255))
        alpha3 = side3.getchannel('A')
        side3 = Image.blend(side3, shade3, 0.4)
        side3.putalpha(alpha3)
        
        # Pastes the sides into the background
        bg.paste(side2, (0, 8*scale), mask = side2)
        bg.paste(side3, (16*scale, 8*scale), mask = side3)
        
        # TODO: This will be just grass path
        if(self.name == "grass_path_side"):
            bg.paste(side1, (0, 1*scale - 1), mask = side1)
        else:
            bg.paste(side1, mask = side1)

        return bg


    # Code from: 
    # https://stackoverflow.com/questions/765736/using-pil-to-make-all-white-pixels-transparent
    # with modifications.
    def clearBackground(self, img, shadeAmt = 0):
        # Takes an image and destructively changes all white pixels to transparent

        data = img.getdata()

        newData = []
        for item in data:
            if item[0] == 255 and item[1] == 255 and item[2] == 255 and item[3] == 255:
                newData.append((255, 255, 255, 0))
            #elif item[0] == 0 and item[1] == 0 and item[2] == 0:
            #    newData.append((255, 255, 255, 0))
            else:
                newData.append(item)
        img.putdata(newData)

    def __repr__(self):
        if(len(self.colors) > 3):
            return f"{self.name} block. Noise factor = {self.noise}.\n Colors = {self.colors[:3]} and {len(self.colors) - 3} more..."
        else:
            return f"\n{self.name} block. Noise = {self.noise}.\n Colors = {self.colors}."

    def __str__(self):
        return f"{self.name} block. Noise = {self.noise}.\n\tColors = {self.colors}."

    def __eq__(self, other):
        return (isinstance(other, Block) and
                self.name == other.name)

    def __hash__(self):
        hashables = (self.name, self.colors, self.noise)
        return hash(hashables)

    @staticmethod
    def getWidth(): # Function used by: PresetPanel.py
        return 16

    # From Class Notes: Animations Part 2, with modifications
    def getCachedPhotoImage(self, app, image, scale):
        if("cached" not in image.__dict__):
            # Case 1: no cached images at all
            # Solution - Make the dictionary
            image.cached = dict()

        if(scale not in image.cached):
            # Case 2: there are cached images, but not of the correct size
            # Solution, actually caches the image
            resizedImage = app.scaleImage(image, scale)
            photoImage = ImageTk.PhotoImage(resizedImage) # Actually makes it
            image.cached[scale] = photoImage

        return image.cached[scale]


    def draw(self, app, canvas, x, y, scale, anchor = 'center'):
        #Advanced: want to draw in 3D w/ 3 images
        photoImage = self.getCachedPhotoImage(app, self.texture, scale)
        texture = app.scaleImage(self.texture, scale)
        canvas.create_image(x, y, image = photoImage,
                            anchor = anchor)