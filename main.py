import pygame
from Lib3D import Object_WireFrame as OWF
from Lib3D import Object_base as OB

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
COLOR = (255,255,255)

def drawWireFrame(screen, lines, color) -> None:
    for line in lines:
        x0, y0, z0 = line[0] #< P0
        x1, y1, z1 = line[1] #< P1
        pygame.draw.line( screen, color, (x0, y0), (x1, y1) ) #< Line from P0 to P1

def clearScreen(screen, color=(255,255,255)) -> None:
  screen.fill(color)
    
def newScreen(title="New", resX=SCREEN_WIDTH, resY=SCREEN_HEIGHT, color=COLOR):
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
                               connections=[[[0,0],[1,0]],[[0,1],[1,1]],[[0,2],[1,2]],[[0,3],[1,3]]])

    world = OB.Object_container(objList = (
        obj1.translate(V=(0,0,0), initShape=True),
        obj2.translate(V=(0,-200,0), initShape=True),
        ))
    
    pygame.init()
    clock = pygame.time.Clock()
    screen = newScreen("3D Wire Frame Shapes", SCREEN_WIDTH, SCREEN_HEIGHT, COLOR)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
              run = False

        clearScreen(screen, COLOR)
        world.rotate(x=0.02,y=0.01,z=0, initShape=True)
        world.translate(x=400,y=400,z=400, initShape=False)
        drawWireFrame(screen, world.getLines(), (0,0,0))
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
