import pygame, math
from Lib3D import Object_WireFrame as OWF
from Lib3D import Object_base as OB
from Lib3D import WireFrame_display as DISP

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255,255,255)
BLACK = (0,0,0)
PI = math.pi
        
def clearScreen(screen, color=(255,255,255)) -> None:
  screen.fill(color)
    
def newScreen(title="New", resX=SCREEN_WIDTH, resY=SCREEN_HEIGHT, color=WHITE):
    screenSize = (resX, resY)
    screen = pygame.display.set_mode( screenSize )
    clearScreen(screen, color)
    pygame.display.set_caption(title)
    return screen
    
if __name__ == "__main__":
    import json
    d = 50
    obj1 = OWF.Object_wireFrame(filename="./objects/house.json", color=(0,180,180)).scale(0.5, initShape=True)
    obj2 = OB.Object_container(objList = (
        OWF.Object_wireFrame(filename="./objects/cube.json", color=(190,190,190)).translate(V=(0,0,0 +d), initShape=True),       #< Body
        OWF.Object_wireFrame(filename="./objects/pyramid.json", color=(90,90,90)).translate(V=(0,-250,0 +d), initShape=True), #< Roof
        OWF.Object_wireFrame(filename="./objects/frame.json", color=(200,0,0)).translate(V=(0,0,-100 +d), initShape=True),   #< Window
        ),
                               connections=[[[0,4],[1,0]],[[0,5],[1,1]],[[0,6],[1,2]],[[0,7],[1,3]]])

    world = OB.Object_container(objList = (
        obj1.translate(V=(0,0,0), initShape=True),
        obj2.translate(V=(0,-100,0), initShape=True),
        ))
    print(obj2.origin)
    pygame.init()
    clock = pygame.time.Clock()
    screen = newScreen("3D Wire Frame Shapes", SCREEN_WIDTH, SCREEN_HEIGHT, WHITE)
    wireframe = DISP.WireFrame(screen, pygame.draw.line, f=50, scale=10)
    fps = 30
    dt = 1/fps
    t = 0.0
    camAngX_r = 0.0
    camAngY_r = 0.0
    roofAng_r = 0.0
    houseAng_r = 0.0
    run = True
    while run:
        ### Get inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
              run = False

        ### Calculate next step state
        camAngX_r += 0.5*dt
        camAngY_r += 1*dt
        roofAng_r = (PI/4/2)*math.sin(2*PI*1*t)
        houseAng_r = (PI/4)*math.sin(2*PI*1.5*t)
        t += dt

        ### Update 3D world
        world.reset()
        obj1.rotate(x=0,y=roofAng_r,z=houseAng_r, initShape=False)
        roof = obj2.shapes[1]
        roof.rotate(x=0,y=roofAng_r,z=0, initShape=False)
        window = obj2.shapes[2]
        window.translate(V=(0,0,0)).rotate(x=0,y=0,z=10*t).translate(V=(0,0,0))
        world.rotate(x=camAngX_r,y=camAngY_r,z=0, initShape=False)
        world.translate(x=0,y=0,z=-600, initShape=False)

        ### Draw 3D world
        clearScreen(screen, WHITE)
        wireframe.draw(world)
        
        ### Wait for next step time
        clock.tick(30)
        
        ### Display output
        pygame.display.flip()
        
    pygame.quit()
