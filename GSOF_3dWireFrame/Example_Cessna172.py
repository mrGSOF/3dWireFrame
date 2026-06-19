#!/usr/bin/python
"""
 * Example_cessna.py
 * Created on: 31 May 2026
 * Improved for: 31 May 2026
 * Author: Guy Soffer
 * Copyright (C) 2026 Guy Soffer
"""
import math
import pygame
import Cessna172_Class
from Lib3D.Object_WireFrame import Object_wireFrame
from Lib3D.Assembly import Assembly
#from Lib3D.Object_base import Object_base
from GSOF_3dWireFrame.utils import Colors
from Lib3D import Objects
from Lib3D import WireFrame_display as DISP

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
pygame.init()

def clearScreen(screen, color=Colors.WHITE) -> None:
  screen.fill(color)

def newScreen(title="New", resX=SCREEN_WIDTH, resY=SCREEN_HEIGHT, color=Colors.WHITE):
    screenSize = (resX, resY)
    screen = pygame.display.set_mode( screenSize )
    clearScreen(screen, color)
    pygame.display.set_caption(title)
    return screen

def rotateFromMouse(obj):
    (mPosX, mPosY) = pygame.mouse.get_pos()
    camAngY_r = 0.01*(mPosX -SCREEN_WIDTH/2)
    camAngX_r = 0.01*(mPosY -SCREEN_HEIGHT/2)
    obj.transform(rotate=(camAngX_r,camAngY_r,0), translate=(0,0,-1000))

if __name__ == "__main__":
    ground = Object_wireFrame(
       obj=Objects.net(25,25), color=Colors.GRAY)\
       .rotate(x=math.pi/2, y=0, z=0)\
       .scale(0.2)\
       .setOrigin()

    cessna = Cessna172_Class.View()

    world = Assembly(objects=(ground, cessna))

    clock = pygame.time.Clock()
    screen = newScreen("3D Wire Frame Shapes", SCREEN_WIDTH, SCREEN_HEIGHT, Colors.WHITE)
    wireframe = DISP.WireFrame(screen, pygame.draw.line, f=50, scale=20.0)

    fps = 30
    run = True
    gearDown = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
              run = False

        clearScreen(screen, Colors.DARK_BLUE)
        world.reset()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_b]:
            gearDown = True
        elif keys[pygame.K_g]:
            gearDown = False
        cessna.setGearsDown(gearDown)

        rotateFromMouse(world)

        cessna.tick(fps=fps)
        wireframe.draw(world)

        clock.tick(fps)
        pygame.display.flip()

    pygame.quit()
