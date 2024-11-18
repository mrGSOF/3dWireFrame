import pygame, math
from Lib3D import Object_WireFrame as OWF
from Lib3D import Object_base as OB
from Lib3D import WireFrame_display as DISP
from Lib3D import Objects
from modules import PlayerControl

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

    net = OWF.Object_wireFrame(obj=Objects.net(25,20), color=(0,100,0)).translate(V=(-1000, 0, 500), initShape=True).scale(0.2, initShape=True)
    f16 = OWF.Object_wireFrame(filename="./objects/F16.stl", color=(0,0,255))
    f16.translate(V=(0, 0, 0), initShape=True)
    f16.scale(0.02, initShape=True)
    f16.translate(V=(0, 0, 0), initShape=True)
    f16.rotate(x=0, y=PI/2, z=PI, origin="arithCenter", initShape=True)
    f16.translate(V=(-50, -50, 0), initShape=True)
    world = OB.Object_container(objList = (
        net,
        f16,
        ))

    pygame.init()
    clock = pygame.time.Clock()
    screen = newScreen("3D Wire Frame Shapes", SCREEN_WIDTH, SCREEN_HEIGHT, WHITE)
    wireframe = DISP.WireFrame(screen, pygame.draw.line, f=50, scale=10)
    viewer = PlayerControl.PlayerControl( pos=(0,0,-1000), center=(int(screen.get_width()/2), int(screen.get_height()/2)) )
    uut    = PlayerControl.PlayerControl( pos=(0,0,0), center=(int(screen.get_width()/2), int(screen.get_height()/2)) )

    fps = 30
    dt = 1/fps
    t = 0.0
    yaw_r = 0.0
    pitch_r = 0.0
    roll_r = 0.0
    objects = [viewer, uut]
    objSel  = 0
    
    run = True
    while run:
        ### Get inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
              run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_v]:
          objSel = 0
        elif keys[pygame.K_u]:
          objSel = 1

        objects[objSel].update()

        wireframe.f += -(keys[pygame.K_1] - keys[pygame.K_2])*10

        ### Calculate next step state
#        t += dt

        ### Update 3D world
        world.reset()
        #f16.rotate(x=roll_r, y=pitch_r, z=yaw_r, initShape=False)
        f16.translate(V=uut.getPosition(), initShape=False)
        f16.rotate(*uut.getAttitude(), initShape=False)
        world.translate(V=viewer.getPosition(), initShape=False)
        world.rotate(*viewer.getAttitude(), initShape=False)

        ### Draw 3D world
        clearScreen(screen, WHITE)
        wireframe.draw(world)

        ### Wait for next step time
        clock.tick(30)

        ### Display output
        pygame.display.flip()
        
    pygame.quit()
