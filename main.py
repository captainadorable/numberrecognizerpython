#---------------------------------------------------------------------
""" Imports """
import pygame, sys
from pygame.locals import K_ESCAPE
from pygame.locals import K_r

import numpy as np
from PIL import Image
from recognizer import Recognizer
import tkinter as tk
from tkinter import messagebox

#Initialize pygame and Recognizer
recognizer = Recognizer()
pygame.init()
#----------------------------------------------------------------- 


#------------------------------------------------------------------
""" WINDOW """
screen = pygame.display.set_mode((1000, 1000), pygame.VIDEORESIZE)
drawSurface = pygame.Surface((896, 896))

pygame.display.set_caption('Number Recognizer!')
#------------------------------------------------------------------


#------------------------------------------------------------------
""" VARIABLES """
font = pygame.font.Font('freesansbold.ttf', 14)
#----------------------------  


#------------------------------------------------------------------
"""Input Class For Inputs"""
class Inputs():
    def __init__(self, events, keyPressed, mousePos, mousePressed):
        self.events = events
        self.keyPressed = keyPressed
        self.mousePos = mousePos
        self.mousePressed = mousePressed

    """KEYBOARD"""

    def GetKeyDown(self, key):
        for event in self.events:
            if event.type == pygame.KEYDOWN:
                if event.key == key:
                    return True
                else:
                    return False

    def GetKeyUp(self, key):
        for event in self.events:
            if event.type == pygame.KEYUP:
                if event.key == key:
                    return True
                else:
                    return False

    def GetKey(self, key):
        if self.keyPressed[key]:
            return True
        else:
            return False

    """MOUSE"""

    def GetMouseButton(self, mouseButton):
        if self.mousePressed[mouseButton]:
            return True
        else:
            return False

    def GetMouseButtonDown(self, mouseButton):
        for event in self.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.mousePressed[mouseButton]:
                    return True
                else:
                    return False

    def GetMouseButtonUp(self, mouseButton):
        for event in self.events:
            if event.type == pygame.MOUSEBUTTONUP:
                if self.mousePressed[mouseButton]:
                    return True
                else:
                    return False
#------------------------------------------------------------------


#-------------------------------------------------------------------
""" Generating drawing table """
class Block():

    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.mainColor = color
        self.color = self.mainColor
        self.rect = pygame.Rect(x, y, width, height)
        self.isDrawed = False
    def DrawBlock(self, surface):
        pygame.draw.rect(surface,  self.color, self.rect)
def CreateBlocks():

    blocks = []

    for x in range(0, 896, 32):
        for y in range(0, 896, 32):
            block = Block(x,  y, 32, 32, (40, 40, 40))
            blocks.append(block)
    return blocks
blocks = CreateBlocks()
#---------------------------------------------------------


#---------------------------------------------------------
"""Save Image"""
def SaveImage(blocks):
    w, h = 28, 28
    data = np.zeros((h, w, 3), dtype=np.uint8)
    
    # Changing Data
    for i in blocks:
        y = i.y // 32
        x = i.x // 32
        if i.isDrawed:    
            data[y, x] = [0, 0, 0]
        else:
            data[y, x] = [255, 255, 255]
        
    #Save image
    img = Image.fromarray(data, 'RGB')
    img.save('image.png')

    #Recognize it
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo(title="Guess",message=f"It's look like {recognizer.Guess()}")
#----------------------------------------------------------


#---------------------------------------------------------------------------
""" Main Loop """
while True:
    #Input
    Input = Inputs(pygame.event.get(), pygame.key.get_pressed(), pygame.mouse.get_pos(), pygame.mouse.get_pressed())

    screen.fill((50, 50, 50))
    drawSurface.fill((30, 30, 30))

    mousePressed = pygame.mouse.get_pressed()
    mousePos = pygame.mouse.get_pos()
    
    #----------------------------------------------------------------------
    """EXIT"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        """EXIT WITH ESC"""
        if Input.GetKeyDown(K_ESCAPE):
            pygame.quit()
            sys.exit()

    """Clear Drawing Table"""
    if Input.GetKeyDown(K_r):
        blocks = CreateBlocks()

    #-----------------------------------------------------------------------
    """Draw Blocks"""

    for block in blocks:
        block.DrawBlock(drawSurface)

    if Input.GetMouseButton(0):
        for block in blocks:
            if block.rect.collidepoint((mousePos[0] - 52, mousePos[1] - 40)):
                block.isDrawed = True
                block.color = (255, 255, 255)
    if Input.GetMouseButton(2):
        for block in blocks:
            if block.rect.collidepoint((mousePos[0] - 52, mousePos[1] - 40)):
                block.isDrawed = False
                block.color = block.mainColor
    #----------------------------------------------------------------------
    
    
    #----------------------------------------------------------------------
    """Save Button"""
    savebtnrect = pygame.Rect(450, 965, 100, 30)    

    text = font.render("Guess", True, (10, 10, 10))
    textrect = pygame.Rect(475, 970, 0, 0)

    pygame.draw.rect(screen, (250, 250, 250), savebtnrect)
    screen.blit(text, textrect)

    if Input.GetMouseButtonDown(0):
        if savebtnrect.collidepoint(mousePos):
            SaveImage(blocks)
    #-------------------------------------------------------------------------

    screen.blit(drawSurface, (52, 40))
    pygame.display.update()