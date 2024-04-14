import pygame

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
COLOR = (255,255,255)

class 3D_object_base() -> 3D_object_base:
    def __init__(self, obj):
        return

    def rotate(self, x,y,z) -> 3D_object_base:
        return self

    def translate(self,x,y,z) -> 3D_object:
        return self

    def getLines(self) -> list:
        return (0,0)

class 3D_object_wireFrame(3D_object_base):
    def __init__(self, obj):
        self.obj = obj
        self.color = self.obj["color"]
        self.lines = self.obj["lines"]
        self.scale(obj["scale"])
        self.obj["points_xyz"] = self.points

    def scale(self, scale) -> 3D_object:
        self.points = self.obj["points_xyz"] #scale
        return self

    def rotate(self, x, y, z) -> 3D_object:
        return self

    def translate(self, x, y, z) -> 3D_object:
        return self

    def getLines(self) -> list:
        for line in lines:
            fromPnt, toPnt = line
            p0 = points[fromPnt]
            p1 = points[toPnt]
            pygame.draw.line( screen, color, (p0[0], p0[1], p1[0], p1[1]) )

def drawObject(screen, obj) -> None:
    drawWireFrame( screen, obj["points_xyz"], obj["lines"], obj["color"] )

def drawWireFrame(screen, points, lines, color) -> None:
    for line in lines:
        fromPnt, toPnt = line
        p0 = points[fromPnt]
        p1 = points[toPnt]
        pygame.draw.line( screen, color, (p0[0], p0[1], p1[0], p1[1]) )

def translateObj(obj, ) -> dict:
    
    
#def drawWorld(world) -> None:
#    for obj in world["objects"]:
#    return

def clearScreen(screen, color=(255,255,255)) -> None:
  screen.fill((255, 255, 255))
    
def newScreen(title="New", resX=SCREEN_WIDTH, resY=SCREEN_HEIGHT, color=COLOR):
    screenSize = (resX, resY)
    screen = pygame.display.set_mode( screenSize )
    clearScreen(screen, color)
    pygame.display.set_caption(title)
    return screen
    
if __name__ == "__main__":
    import json
    objName = "../objects/cube.json"
    pygame.init()
    screen = newScreen("3D Wire Frame Shapes", SCREEN_WIDTH, SCREEN_HEIGHT, COLOR)

    run = True
    while run:

      pygame.draw.rect(screen, (255, 0, 0), (200, 100, 150, 150))
      #drawObject(screen, obj)
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          run = False

      pygame.display.flip()

    pygame.quit()
