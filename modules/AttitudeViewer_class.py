import pygame, math, json
from Lib3D import Object_WireFrame as OWF
from Lib3D import Object_base as OB
from Lib3D import WireFrame_display as DISP
from Lib3D import Objects
from modules import Controls

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255,255,255)
BLACK = (0,0,0)
PI = math.pi

def newScreen(title="New", resX=SCREEN_WIDTH, resY=SCREEN_HEIGHT, color=WHITE):
    screen = pygame.display.set_mode( (resX, resY) )
    screen.fill(color)
    pygame.display.set_caption(title)
    return screen
 
class AttitudeViewer():
  def __init__(self):
      net  = OWF.Object_wireFrame(obj=Objects.net(25,25), color=(0,100,0)).rotate(x=PI/2, y=0, z=0).translate(V=(0, 0, 0), initShape=True).scale(0.2, initShape=True)
      axis = OWF.Object_wireFrame(filename="./objects/axis.json", color=(10,10,10)).translate(V=(0, 0, 0), initShape=True).scale(5.0, initShape=True)
      self.f16  = OWF.Object_wireFrame(filename="./objects/F16.stl", color=(0,0,255)).translate(V=(0, 0, 0), initShape=True)
      self.f16.setOrigin( origin=self.f16.getOrigin(origin="arithCenter"), initShape=True ).scale(0.02, initShape=True)
  #    f16.translate(V=(0, 0, 200), initShape=True)
  #    f16.rotate(x=0, y=PI/2, z=PI, origin="arithCenter", initShape=True)
  #    f16.translate(V=(-50, -50, 0), initShape=True)

      self.world = OB.Object_container(objList = (
          axis,
          net,
          self.f16,
          ))

      pygame.init()
      self.clock     = pygame.time.Clock()
      self.screen    = newScreen("3D Wire Frame - Attitude Viewer", SCREEN_WIDTH, SCREEN_HEIGHT, WHITE)
      self.wireframe = DISP.WireFrame(self.screen, pygame.draw.line, f=50, scale=10)
      self.viewer    = Controls.Viewer( pos=(0,0,-1200),
                                        center=(int(self.screen.get_width()/2),int(self.screen.get_height()/2)),
                                        moveLeftKey  = pygame.K_a,
                                        moveRightKey = pygame.K_d,
                                        moveUpKey    = pygame.K_UP,
                                        moveDownKey  = pygame.K_DOWN,
                                        moveFwdKey   = pygame.K_w,
                                        moveBackKey  = pygame.K_x,
                                        tiltLeft     = pygame.K_COMMA,
                                        tiltRight    = pygame.K_PERIOD
                                       )
      self.uut       = Controls.Object( pos=(200,200,200),
                                        center=(int(self.screen.get_width()/2), int(self.screen.get_height()/2)),
                                        moveLeftKey  = pygame.K_a,
                                        moveRightKey = pygame.K_d,
                                        moveUpKey    = pygame.K_UP,
                                        moveDownKey  = pygame.K_DOWN,
                                        moveFwdKey   = pygame.K_w,
                                        moveBackKey  = pygame.K_x,
                                        tiltLeft     = pygame.K_COMMA,
                                        tiltRight    = pygame.K_PERIOD
                                       )

      self.fps = 30
      self.dt = 1/self.fps
      self.t = 0.0
      self.objects = [self.viewer, self.uut]
      self.objSel  = 0
      self.run = False

  def _clearScreen(self, color=(255,255,255)) -> None:
      self.screen.fill(color)

  def start(self):    
      self.run = True
      while self.run:
          ### Get inputs
          for event in pygame.event.get():
              if event.type == pygame.QUIT:
                self.run = False

          keys = pygame.key.get_pressed()
          (mPosX, mPosY) = pygame.mouse.get_pos()
          if keys[pygame.K_v]:
            self.objSel = 0
          elif keys[pygame.K_u]:
            self.objSel = 1

          self.objects[self.objSel].update(keys, mPosX, mPosY, speed=2)

          self.wireframe.f += -(keys[pygame.K_1] - keys[pygame.K_2])*10

          ### Calculate next step state
  #        t += dt

          ### Update 3D world
          self.world.reset()
          self.f16.rotate( *self.uut.getAttitude() ).translate( V=self.uut.getPosition() )
          self.world.translate( V=self.viewer.getPosition() ).rotate( *self.viewer.getAttitude() )

          ### Draw 3D world
          self._clearScreen(WHITE)
          self.wireframe.draw(self.world)

          ### Wait for next step time
          self.clock.tick(30)

          ### Display output
          pygame.display.flip()
          
      pygame.quit()

if __name__ == "__main__":
    attitude = AttitudeViewer()
    attitude.start()

