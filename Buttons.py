#################################################
# 15-112 Term Project: Minecraft Block Palette Generator by Jimmy Zeng

# Inspired by online color palette generators like Colormind.io, this project
# aims to generate a list of minecraft blocks that work well with each other in
# any build based on their textures and colors.
#
# Your name: Jimmy Zeng
# Your andrew id: jimmyzen
#################################################

from cmu_112_graphics import * # From Class Notes: Animation Part 1
from tkinter import *
from PIL import Image
import random, math, copy, string, time, os
from tkinter.font import *

# My other classes
from Block import *

#################################################
# The variety of Buttons found here are implemented in __init__.py and helps
# with drawing and checking mouse detection.
#################################################

# Base for all buttons the player can click on
# Tab and gen buttons won't have an active mode. The search + lock buttons will.
class Button(object):
    def __init__(self, x, y, width, height, sprite, activeSprite = None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        WHRatio = sprite.width // sprite.height
        if(width > height):
            width = height * WHRatio
        else:
            height = width // WHRatio
        ratio = (width, height)

        self.sprite = sprite.resize(ratio)
        
        if(activeSprite != None):
            self.activeSprite = activeSprite.resize(ratio)
        else:
            self.activeSprite = self.sprite

    def draw(self, canvas):
        canvas.create_image(self.x, self.y,
                            image = ImageTk.PhotoImage(self.sprite),
                            activeimage = ImageTk.PhotoImage(self.activeSprite),
                            anchor = "nw")
        
    def checkInBounds(self, mouseX, mouseY):
        return (mouseX > self.x and mouseX < self.x + self.width and
                mouseY > self.y and mouseY < self.y + self.height)

    def setSprites(self, inactive, active):
        self.sprite = inactive
        self.activeSprite = active
        

class LockableButton(Button):
    def __init__(self, x, y, width, height,
                 lockInactive, lockActive,
                 unlockInactive, unlockActive):
                 
        self.lockInactive   = lockInactive
        self.lockActive     = lockActive
        self.unlockInactive = unlockInactive
        self.unlockActive   = unlockActive

        self.isLocked = False # If locked, the lock button should appear.
                              # Else, the unlock button should appear

        super().__init__(x, y, width, height, self.unlockInactive, self.unlockActive):
    
    def lock(self):
        self.isLocked = not self.isLocked
        if(self.isLocked):
            (self.image, self.active) = self.unlockSprite
        else:
            (self.image, self.active) = self.lockSprites 


# Buttons that has both images and text -> the generate! button
class GenerateButton(Button):
    def __init__(self, x, y, width, height,
             font, text, textColor, activeColor, margins, action, image = None, color = None):
        super().__init__(x, y, width, height, action, color)
        self.text = text
        self.font = font
        self.textColor = textColor
        self.activeColor = activeColor
        size = min(width, height)
        self.image = image.resize((size, size))
        self.xMargin, self.yMargin = margins

    def draw(self, canvas):
        super().draw(canvas)
        canvas.create_image(self.x + self.xMargin,
                            self.y + self.height / 2,
                            image = ImageTk.PhotoImage(self.image),
                            anchor = "w")
        canvas.create_text(self.x + self.image.width + self.xMargin * 2,
                           self.y + self.height / 2 ,
                           text = self.text,
                           font = self.font,
                           fill = self.textColor,
                           activefill = self.activeColor,
                           anchor = "w")