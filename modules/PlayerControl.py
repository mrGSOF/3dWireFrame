import pygame, math
from MathLib import MathLib as ML

class PlayerControl():
  def __init__(self, pos=(0,0,0), att=(0,0,0), center=(0,0)):
    self.posX = pos[0]
    self.posY = pos[1]
    self.posZ = pos[2]
    self.attX = att[0]
    self.attY = att[1]
    self.centerX = center[0]
    self.centerY = center[1]

  def update(self) -> list:
    pos = self.updatePos()
    att = self.updateAtt()
    return (pos, att)

  def updateAtt(self) -> list:
    (mPosX, mPosY) = pygame.mouse.get_pos()
    self.attY = 0.5*ML.pi*(mPosX/self.centerX -1)
    self.attX = 0.5*ML.pi*(mPosY/self.centerY -1)
    return (self.attX, self.attY)

  def updatePos(self) -> list:
    keys = pygame.key.get_pressed()
    speed = 1
    self.posX += -(keys[pygame.K_RIGHT] -keys[pygame.K_LEFT])*2.0*speed
    self.posX += -(keys[pygame.K_d]     -keys[pygame.K_a])*2.0*speed
    self.posY += -(keys[pygame.K_UP]    -keys[pygame.K_DOWN])*2.0*speed
    self.posZ += -(keys[pygame.K_x]     -keys[pygame.K_w])*5*speed
    return (self.posX, self.posY, self.posZ)
