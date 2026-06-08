#!/usr/bin/python
"""
 * Example_F16.py
 * Created on: 31 May 2026
 * Improved for: 31 May 2026
 * Author: Guy Soffer
 * Copyright (C) 2026 Guy Soffer
"""
import pygame, math
from Lib3D.Object_WireFrame import Object_wireFrame
from Lib3D.Assembly import Assembly
#from Lib3D.Object_base import Object_base
from Lib3D import Objects
from Lib3D import WireFrame_display as DISP
from F16_Class import F16_View

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255,255,255)
BLUE = (220,220,255)
BLACK = (0,0,0)
PI = math.pi

class Engine():
    def __init__(self, thrust_lbf):
        self.thrust_lbf = thrust_lbf

class InertialNavigationSystem():
    def __init__(self, azimuth_d, pitch_d, roll_d):
        self.azimuth_d = azimuth_d
        self.pitch_d   = pitch_d
        self.roll_d    = roll_d

class FlightSurfaces():
    def __init__(self,
                 leftAliron_d=0, rightAliron_d=0,
                 leftElevator_d=0, rightElevator_d=0,
                 rudder_d=0, speedbrake_d=0,
                 gearDown_b=True):
        self.lAliron_d   = leftAliron_d
        self.rAliron_d   = rightAliron_d
        self.lElevator_d = leftElevator_d
        self.rElevator_d = rightElevator_d
        self.rudder_d    = rudder_d
        self.sb_d        = speedbrake_d
        self.gearsDown   = gearDown_b

class WeightOnWheels():
    def __init__(self, left, right, nose):
        self.left  = left
        self.right = right
        self.nose  = nose

def drawWireFrame(screen, obj, color=None) -> None:
    for line in obj.getLines():
        x0, y0, z0 = line.p0
        x1, y1, z1 = line.p1
        lcolor = color
        if lcolor == None:
            lcolor = line.color
        pygame.draw.line( screen, lcolor, (x0, y0), (x1, y1) ) #< Line from P0 to P1

def clearScreen(screen, color=(255,255,255)) -> None:
  screen.fill(color)
    
def newScreen(title="New", resX=SCREEN_WIDTH, resY=SCREEN_HEIGHT, color=WHITE):
    screenSize = (resX, resY)
    screen = pygame.display.set_mode( screenSize )
    clearScreen(screen, color)
    pygame.display.set_caption(title)
    return screen

if __name__ == "__main__":
    ground = Object_wireFrame(
       obj=Objects.net(25,25), color=(0,100,0))\
       .scale(0.2)\
       .rotate(x=math.pi/2, y=0, z=0)\
       .translate(-250, -200, -250)\
       .setOrigin()

    f16 = F16_View()\
          .scale(1.0)\
          .translate(0, 0, 0)\
          .rotate(0*3.14/2, 0*3.14/2, 0)\
          .setOrigin()

    world = Assembly(objects=(ground, f16))

    pygame.init()
    clock = pygame.time.Clock()
    screen = newScreen("3D Wire Frame Shapes", SCREEN_WIDTH, SCREEN_HEIGHT, WHITE)
    wireframe = DISP.WireFrame(screen, pygame.draw.line, f=50, scale=20.0)

    fps = 30
    dt = 1/fps
    t = 0.0
    camAngX_r = 0.0
    camAngY_r = 0.0
    eng  = Engine(thrust_lbf=6000)
    wow = WeightOnWheels(left=True, right=True, nose=True)
    useMouse = True

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
              run = False
        world.reset()
        f16.setControls(t, fcs=None, eng=eng, ins=None, wow=wow)
        world.transform(rotate=(camAngX_r,camAngY_r,0), translate=(0,0,-1000))
#        world.transform(rotate=(0.0*3.14, 0.0*3.14, 0), translate=(0,0,-80))

        ### Draw 3D world
        clearScreen(screen, BLUE)
        wireframe.draw(world)
        
        ### Wait for next step time
        keys = pygame.key.get_pressed()
        eng.thrust_lbf += -(keys[pygame.K_1] - keys[pygame.K_2])*200
        
        if useMouse:
            (mPosX, mPosY) = pygame.mouse.get_pos()
            camAngY_r = 0.01*(mPosX -SCREEN_WIDTH/2)
            camAngX_r = 0.01*(mPosY -SCREEN_HEIGHT/2)
        else:
            camAngX_r += 0.5*dt
            camAngY_r += 1*dt
        t += dt
        clock.tick(30)
        
        ### Display output
        pygame.display.flip()

    pygame.quit()
    
