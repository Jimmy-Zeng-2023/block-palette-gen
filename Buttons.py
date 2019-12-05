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

class ImageButton(object):
    def __init__(self, x, y, width, height, sprite = None, activeSprite = None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.sprite = sprite
        
        # A button can have 0 sprites, only active, or both active and inactive (regular) sprites
        if(activeSprite != None):
            #self.activeSprite = activeSprite.resize(ratio)
            self.activeSprite = activeSprite
        else:
            self.activeSprite = self.sprite

    def draw(self, canvas, dragDelta = 0):
        # Draws the sprite(s) (if possible)
        if(self.sprite == None):
            return
        else:
            if(dragDelta != 0):
                x = self.x + dragDelta
            else:
                x = self.x

            canvas.create_image(x + self.width//2,
                            self.y + self.height//2,
                            image = ImageTk.PhotoImage(self.sprite),
                            activeimage = ImageTk.PhotoImage(self.activeSprite))
        
    def checkInBounds(self, mouseX, mouseY):
        # Main function of the button: checking if it has been clicked on
        return (mouseX > self.x and mouseX < self.x + self.width and
                mouseY > self.y and mouseY < self.y + self.height)

    def setSprites(self, inactive, active):
        # Allows other functions to override the initial sprites
        self.sprite = inactive
        self.activeSprite = active
        

class LockButton(ImageButton):
    # The lock button can be toggled on and off (locked and unlocked)
    def __init__(self, x, y, width, height,
                 lockedActive,
                 unlockedInactive, unlockedActive):
                 
        self.lockedActive     = lockedActive # Locked -> Shackle down. Displayed when block is locked.
                                             # When locked, always white.
        self.unlockedInactive = unlockedInactive # Unlocked -> Shackle lifed. Displayed when block is not locked.
        self.unlockedActive   = unlockedActive

        self.isLocked = False # If locked, the lock button should appear.
                              # Else, the unlock button should appear

        super().__init__(x, y, width, height, self.unlockedInactive, self.unlockedActive)
    
    def lock(self, forceLock = False):
        # Swaps between the two states
        self.isLocked = not self.isLocked

        if(forceLock): 
            # Normal lock toggles the lock, forcelock locks the button down.
            self.setSprites(self.lockedActive, self.lockedActive)
            return
        # Had a strange but that the forcelock would activate but the the unlocked sprite
        # still loads. Workaround was to make forcelock shut down the function completely.

        if(self.isLocked):
            self.setSprites(self.lockedActive, self.lockedActive)
        else:
            self.setSprites(self.unlockedInactive, self.unlockedActive)
