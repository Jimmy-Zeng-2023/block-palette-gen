from cmu_112_graphics import *
from tkinter import *
from PIL import Image
import random, math, copy, string, time, os


def rgbString(red, green, blue):
    # Don't worry about how this code works yet.
    return "#%02x%02x%02x" % (red, green, blue)

def appStarted(app):
    
    grass = "grass_block_side.png"
    glass = "blue_stained_glass.png"
    app.block = Image.open(grass)

    app.colors = app.block.getcolors(maxcolors = 10**6)
    print(app.colors)
    app.block = app.scaleImage(app.block, 20)
   
def redrawAll(app, canvas):
    canvas.create_image(0,0, image =  ImageTk.PhotoImage(app.block), anchor = 'nw')

    x, y, s = 600, 0, 30
    for i in range(len(app.colors)):
        thisColor = app.colors[i][1]
        thisColorStr = rgbString(thisColor[0], thisColor[1], thisColor[2])
        canvas.create_rectangle(x, y, x + s, y + s, fill = thisColorStr, width = 0)
        y += 30
        if(y > 350):
            y = 0
            x += 30

runApp(width = 800, height = 400)