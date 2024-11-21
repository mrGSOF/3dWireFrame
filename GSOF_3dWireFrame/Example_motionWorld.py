import pygame
from Lib3D import Object_WireFrame as OWF
from Lib3D import Object_base as OB
from Lib3D import Objects
from Lib3D import WireFrame_display as DISP
from modules import Controls

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255,255,255)
BLACK = (0,0,0)

def clearScreen(screen, color=(255,255,255)) -> None:
  screen.fill(color)

def newScreen(title="New", resX=SCREEN_WIDTH, resY=SCREEN_HEIGHT, color=WHITE):
    screenSize = (resX, resY)
    screen = pygame.display.set_mode( screenSize )
    clearScreen(screen, color)
    pygame.display.set_caption(title)
    return screen
  
if __name__ == "__main__":
    house = OWF.Object_wireFrame(filename="./objects/house.json", color=(0,180,180)).scale(1.0, initShape=True)
    world = OB.Object_container(objList = (
        house,
        ))

    pygame.init()
    clock = pygame.time.Clock()
    screen = newScreen("3D Wire Frame Shapes", SCREEN_WIDTH, SCREEN_HEIGHT, WHITE)
    wireframe = DISP.WireFrame(screen, pygame.draw.line, f=50, scale=10)
    viewer = Controls.Viewer( pos=(0,0,-400),
                              center=(int(screen.get_width()/2), int(screen.get_height()/2)),
                              moveLeftKey  = pygame.K_a,
                              moveRightKey = pygame.K_d,
                              moveUpKey    = pygame.K_UP,
                              moveDownKey  = pygame.K_DOWN,
                              moveFwdKey   = pygame.K_w,
                              moveBackKey  = pygame.K_x,
                              tiltLeft     = pygame.K_COMMA,
                              tiltRight    = pygame.K_PERIOD
                             )

    fps = 30
    dt = 1/fps
    t = 0.0
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        (mPosX, mPosY) = pygame.mouse.get_pos()
        wireframe.f += -(keys[pygame.K_1] - keys[pygame.K_2])*10
        viewer.update(keys, mPosX, mPosY, speed=2)
        
        clearScreen(screen, WHITE)
        world.reset()
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
