import pygame, math
from Lib3D.Object_WireFrame import Object_wireFrame
from Lib3D.Object_base import Object_base
from Lib3D.Assembly import Assembly
from Lib3D import WireFrame_display as DISP
from Lib3D import Objects

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255,255,255)
BLACK = (0,0,0)
PI = math.pi

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
    net    = Object_wireFrame(obj=Objects.net(25,20), color=(0,100,0)).scale(0.2).translate(0, 0, 0).setOrigin()
    sphere = Object_wireFrame(obj=Objects.sphere(500, 25, color=(255,0,0))).scale(0.1).translate(125, 150, 500).setOrigin() #< More up and right to the center of the net 
    plane  = Object_wireFrame(filename="./objects/F16.stl", color=(0,0,255)).scale(1.0).translate(160, 90, 250).rotate(-PI/2,0,0).setOrigin()
    world  = Assembly(objects = (
        net,
        plane,
        sphere,
        ))

    pygame.init()
    clock = pygame.time.Clock()
    screen = newScreen("3D Wire Frame Shapes", SCREEN_WIDTH, SCREEN_HEIGHT, WHITE)
    wireframe = DISP.WireFrame(screen, pygame.draw.line, f=50, scale=10.0)

    fps = 30
    dt = 1/fps
    t = 0.0
    camAngX_r = 0.0
    camAngY_r = 0.0
    roofAng_r = 0.0
    houseAng_r = 0.0
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
              run = False

        world.reset()
        #world.rotate(x=1.8,y=3.14,z=0.3)
        world.rotate(x=camAngX_r,y=camAngY_r,z=0)
        #world.rotate(x=camAngX_r,y=camAngY_r,z=0, origin="arithCenter")
        #world.rotate(x=camAngX_r,y=camAngY_r,z=0, origin="minMaxCenter")
        world.translate(x=0,y=0,z=-1500)

        ### Draw 3D world
        clearScreen(screen, WHITE)
        wireframe.draw(world)
        
        ### Wait for next step time
        camAngX_r += 0.5*dt
        camAngY_r += 1*dt
        t += dt
        clock.tick(30)
        
        ### Display output
        pygame.display.flip()

    pygame.quit()
