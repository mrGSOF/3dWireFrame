import pygame, math
from Lib3D import Object_WireFrame as OWF
from Lib3D import Object_base as OB
from Lib3D import Objects

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
    net = OWF.Object_wireFrame(obj=Objects.net(25,20)).translate(V=(-1000, 0, 500), initShape=True).scale(0.2, initShape=True)
    sphere = OWF.Object_wireFrame(obj=Objects.sphere(500, 25)).translate(V=(-1000, 0, 500), initShape=True).scale(0.2, initShape=True)
    plane = OWF.Object_wireFrame(filename="./objects/F16.stl").rotate(-PI/2,0,0).scale(0.02, initShape=True)
    world = OB.Object_container(objList = (
        net,
        plane,
        sphere,
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
        world.rotate(x=camAngX_r,y=camAngY_r,z=0, initShape=False)
        #world.rotate(x=camAngX_r,y=camAngY_r,z=0, initShape=False, origin="arithCenter")
        #world.rotate(x=camAngX_r,y=camAngY_r,z=0, initShape=False, origin="minMaxCenter")
        world.translate(x=400,y=200,z=400, initShape=False)
        drawWireFrame(screen, world, BLACK)
        pygame.display.flip()
        camAngX_r += 0.5*dt
        camAngY_r += 1*dt
        t += dt
        clock.tick(30)

    pygame.quit()
