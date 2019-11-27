# block-palette-gen
15-112 Term Project: Minecraft Block Palette Generator by Jimmy Zeng

Inspired by online color palette generators like Colormind.io, this project aims
to generate a list of minecraft blocks that work well with each other in any
build based on their textures and colors.

## Running the App

Run __init__.py for the final app.
Change blacklist.txt to change which textures are loaded and which are discarded.

## Explaination of the Classes:

The Block class represents a Minecraft block.
Its purpose is mainly to serve as a data structure.

The TextureReader takes in the raw textures, derive their colors and noise
factors, and organizes them for the rest of the classes.

The BlockGenerator will generate matching blocks when provided with
a base block. This is the key to the palette generator.

The TextureDisplayApp shows an overview of all the textures loaded.
Press left and right to navigate.

The ColorDisplayApp allows one to go through each block in the loaded
Texturepack and view their colors and noise. Press left and right to navigate.

There are some other classes around, such as Panel.py and Buttons.py, which are
relatively simple and instantiated for the frontend display. More info can be found
in each of their respective files.