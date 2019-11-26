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

# Base for all buttons the player can click on
class Button(object):
    def __init__(self, x, y, width, height, action = "", color = None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.action = action
        self.color = color

    def draw(self, canvas):
        # Draws the rectangle of the button
        if(self.color != None):
            canvas.create_rectangle(self.x, self.y,
                                    self.x + self.width, self.y + self.height,
                                    width = 0,
                                    fill = self.color)

    def checkInBounds(self, mouseX, mouseY):
        return (mouseX > self.x and mouseX < self.x + self.width and
                mouseY > self.y and mouseY < self.y + self.height)
        
# Button that also displays text
class TextButton(Button):
    def __init__(self, x, y, width, height,
                 font, text, textColor, activeColor, action, offset = 0, color = None):
        super().__init__(x, y, width, height, action, color)
        self.text = text
        self.font = font
        self.textColor = textColor
        self.activeColor = activeColor
        self.offset = offset

    def draw(self, canvas):
        super().draw(canvas)
        canvas.create_text(self.x + self.width/2, self.y + self.height/2 + self.offset,
                           text = self.text,
                           font = self.font,
                           fill = self.textColor,
                           activefill = self.activeColor)

# Buttons that display an image
class ImageButton(Button):
    def __init__(self, x, y, width, height, action, sprites):
        super().__init__(x, y, width, height, action, None)
        # Active is image displayed when moused over
        # sprites holds both the regular and the active image
        self.image, self.active = sprites

    def draw(self, canvas):
        canvas.create_image(self.x, self.y,
                            image = ImageTk.PhotoImage(self.image),
                            activeimage = ImageTk.PhotoImage(self.active),
                            anchor = "nw")

class LockableButton(ImageButton):
    def __init__(self, x, y, width, height, action, lockSprites, unlockSprite):
        self.lockSprites = lockSprites
        self.unlockSprite = unlockSprite
        self.isLocked = False # If locked, the unlock button should appear.
                              # Else, the lock button should appear

        super().__init__(x, y, width, height, action, self.lockSprites)
    
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