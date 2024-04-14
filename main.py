import pygame
from Lib3D import Object_WireFrame

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
COLOR = (255,255,255)

def drawWireFrame(screen, lines, color) -> None:
    for line in lines:
        p0 = line[0]
        p1 = line[1]
        pygame.draw.line( screen, color, p0, p1 )

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
    objName = "./objects/cube.json"
    obj = None
    with open(objName) as f:
        obj = json.load(f)

    pygame.init()
    screen = newScreen("3D Wire Frame Shapes", SCREEN_WIDTH, SCREEN_HEIGHT, COLOR)

    run = True
    while run:

      #pygame.draw.rect(screen, (255, 0, 0), (200, 100, 150, 150))
      drawWireFrame(screen, [[(50,50),(100,100)],[(50,50),(50,200)]], (0,0,0))
      #drawObject(screen, obj)
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          run = False

      pygame.display.flip()

    pygame.quit()
