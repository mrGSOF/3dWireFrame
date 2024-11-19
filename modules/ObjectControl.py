import pygame, math
from MathLib import MathLib as ML
from modules.ViewerControl import ViewerControl

class ObjectControl(ViewerControl):
  def updateAtt(self) -> list:
    (mPosX, mPosY) = pygame.mouse.get_pos()
    self.attY = 0.5*ML.pi*(mPosX/self.centerX -1)
    self.attX = 0.5*ML.pi*(mPosY/self.centerY -1)
    keys = pygame.key.get_pressed()
    speed = 3*ML.pi/180 #< 3 deg
    self.attZ += (keys[pygame.K_PERIOD] -keys[pygame.K_COMMA])*speed
    return self.getAttitude()

  def updatePos(self) -> list:
    keys = pygame.key.get_pressed()
    speed = 2.0
    self.posX += (keys[pygame.K_RIGHT] -keys[pygame.K_LEFT])*speed
    self.posX += (keys[pygame.K_d]     -keys[pygame.K_a])*speed
    self.posY += (keys[pygame.K_w]     -keys[pygame.K_x])*5*speed
    self.posZ += (keys[pygame.K_UP]    -keys[pygame.K_DOWN])*speed
    return self.getPosition()
