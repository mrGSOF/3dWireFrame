import pygame, math
from Lib3D import Object_WireFrame as OWF
from Lib3D import Object_base as OB
from Lib3D import Objects
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
    house = OWF.Object_wireFrame(filename="./objects/house.json", color=(0,180,180)).scale(1.0, initShape=True)
    world = OB.Object_container(objList = (
        house,
        ))

    pygame.init()
    clock = pygame.time.Clock()
    screen = newScreen("3D Wire Frame Shapes", SCREEN_WIDTH, SCREEN_HEIGHT, WHITE)
    wireframe = DISP.WireFrame(screen, pygame.draw.line, f=50)

    fps = 30
    dt = 1/fps
    t = 0.0
    camAngX_r = 0.0
    camAngY_r = 0.0
    roofAng_r = 0.0
    houseAng_r = 0.0
    run = True
    location = [0,200,0]
    attitude = [0.0, 0.0, 0.0]

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

##            elif event.type == pygame.KEYDOWN:
##                speed = 1
##                if event.key == pygame.K_LEFT:
##                    location[0] += speed
##                if event.key == pygame.K_RIGHT:
##                    location[0] -= speed
##                if event.key == pygame.K_UP:
##                    location[2] += speed
##                if event.key == pygame.K_DOWN:
##                    location[2] -= speed
##
##                speed = 0.05
##                if event.key == pygame.K_q:
##                    attitude[0] += speed
##                if event.key == pygame.K_z:
##                    attitude[0] -= speed

        keys = pygame.key.get_pressed()
        speed = 1
        location[0] += -(keys[pygame.K_RIGHT] - keys[pygame.K_LEFT])*2.0*speed
        location[1] += -(keys[pygame.K_UP] - keys[pygame.K_DOWN])*2.0*speed
        location[2] += -(keys[pygame.K_q] - keys[pygame.K_z])*5*speed
        wireframe.f += -(keys[pygame.K_w] - keys[pygame.K_s])*10
        #attitude[0] += -(keys[pygame.K_q] - keys[pygame.K_z])*0.05*speed
        print(wireframe.f, location[0], location[1], location[2])
        clearScreen(screen, WHITE)
        world.reset()
        world.translate(V=location, initShape=False)
        world.rotate(*attitude, initShape=False)

        ### Draw 3D world
        clearScreen(screen, WHITE)
        wireframe.draw(world)

        ### Wait for next step time
        clock.tick(30)

        ### Display output
        pygame.display.flip()

    pygame.quit()
