import pygame, math
from Lib3D import Object_WireFrame as OWF
from Lib3D import Object_base as OB

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255,255,255)
BLACK = (0,0,0)
PI = math.pi

def drawWireFrame(screen, obj, color) -> None:
    for line in obj.getLines():
        x0, y0, z0 = line.p0
        x1, y1, z1 = line.p1
        pygame.draw.line( screen, color, (x0, y0), (x1, y1) ) #< Line from P0 to P1

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
    #objName = "./objects/cube.json"
    #objName = "./objects/pyramid.json"
    #objName = "./objects/house.json"
    obj1 = OWF.Object_wireFrame(filename="./objects/house.json").scale(0.5, initShape=True)
    obj2 = OB.Object_container(objList = (
        OWF.Object_wireFrame(filename="./objects/cube.json").translate(V=(0,0,0), initShape=True),       #< Body
        OWF.Object_wireFrame(filename="./objects/pyramid.json").translate(V=(0,-250,0), initShape=True), #< Roof
        OWF.Object_wireFrame(filename="./objects/frame.json").translate(V=(0,0,-100), initShape=True),   #< Window
        ),
                               connections=[[[0,4],[1,0]],[[0,5],[1,1]],[[0,6],[1,2]],[[0,7],[1,3]]])

    obj3 = OWF.Object_wireFrame(filename="./objects/frame.json").translate(V=(0,0,0), initShape=True)

    world = OB.Object_container(objList = (
        obj1.translate(V=(0,0,0), initShape=True),
        obj2.translate(V=(0,-200,0), initShape=True),
        #obj3.translate(V=(0,0,0), initShape=True),
        ))
    
    pygame.init()
    clock = pygame.time.Clock()
    screen = newScreen("3D Wire Frame Shapes", SCREEN_WIDTH, SCREEN_HEIGHT, WHITE)

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

        clearScreen(screen, WHITE)
        world.reset()
        obj1.rotate(x=0,y=roofAng_r,z=houseAng_r, initShape=False)
        roof = obj2.shapes[1]
        roof.rotate(x=0,y=roofAng_r,z=0, initShape=False)
        window = obj2.shapes[2]
        window.translate(V=(0,200,0)).rotate(x=0,y=0,z=10*t).translate(V=(0,-200,0))
        world.rotate(x=camAngX_r,y=camAngY_r,z=0, initShape=False)
        world.translate(x=400,y=400,z=400, initShape=False)
        drawWireFrame(screen, world, BLACK)
        pygame.display.flip()
        camAngX_r += 0.5*dt
        camAngY_r += 1*dt
        roofAng_r = (PI/4/2)*math.sin(2*PI*1*t)
        houseAng_r = (PI/4)*math.sin(2*PI*1.5*t)
        t += dt
        clock.tick(30)

    pygame.quit()
