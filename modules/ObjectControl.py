import pygame, math
from MathLib import MathLib as ML
from modules.ViewerControl import ViewerControl

class ObjectControl(ViewerControl):
  def updateAtt(self) -> list:
    (mPosX, mPosY) = pygame.mouse.get_pos()
    self.attY = 0.5*ML.pi*(mPosX/self.centerX -1)
    self.attX = 0.5*ML.pi*(mPosY/self.centerY -1)
    return self.getAttitude()

  def updatePos(self) -> list:
    keys = pygame.key.get_pressed()
    speed = 1
    self.posX += (keys[pygame.K_RIGHT] -keys[pygame.K_LEFT])*2.0*speed
    self.posX += (keys[pygame.K_d]     -keys[pygame.K_a])*2.0*speed
    self.posY += (keys[pygame.K_w]     -keys[pygame.K_x])*5*speed
    self.posZ += (keys[pygame.K_UP]    -keys[pygame.K_DOWN])*2.0*speed
    return self.getPosition()
