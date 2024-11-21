import math

class Viewer():
    def __init__(self, pos=(0,0,0), att=(0,0,0), center=(0,0),
                 moveLeftKey=0, moveRightKey=0,
                 moveUpKey=0,   moveDownKey=0,
                 moveFwdKey=0,  moveBackKey=0,
                 tiltLeft=0,    tiltRight=0):
        self.posX = pos[0]
        self.posY = pos[1]
        self.posZ = pos[2]
        self.attX = att[0]
        self.attY = att[1]
        self.attZ = att[2]
        self.centerX = center[0]
        self.centerY = center[1]
        self.moveLeftKey  = moveLeftKey
        self.moveRightKey = moveRightKey
        self.moveUpKey    = moveUpKey
        self.moveDownKey  = moveDownKey
        self.moveFwdKey   = moveFwdKey
        self.moveBackKey  = moveBackKey
        self.tiltLeft     = tiltLeft
        self.tiltRight    = tiltRight

    def update(self, keys, mPosX, mPosY, speed=2) -> list:
        pos = self.updatePos(keys, mPosX, mPosY, speed)
        att = self.updateAtt(keys, mPosX, mPosY, speed)
        return (pos, att)

    def getPosition(self):
        return (self.posX, self.posY, self.posZ)
      
    def getAttitude(self):
        return (self.attX, self.attY, self.attZ)

    def updateAtt(self, keys, mPosX, mPosY, speed) -> list:
        self.attY = 0.5*math.pi*(mPosX/self.centerX -1)
        self.attX = 0.5*math.pi*(mPosY/self.centerY -1)
        return self.getAttitude()

    def updatePos(self, keys, mPosX, mPosY, speed) -> list:
        self.posX += -(keys[self.moveRightKey] -keys[self.moveLeftKey])*2.0*speed
        self.posY += -(keys[self.moveUpKey]    -keys[self.moveDownKey])*2.0*speed
        self.posZ += -(keys[self.moveBackKey]  -keys[self.moveFwdKey])*5.0*speed
        return self.getPosition()

class Object(Viewer):
    def updateAtt(self, keys, mPosX, mPosY, speed) -> list:
        self.attY = 0.5*math.pi*(mPosX/self.centerX -1)
        self.attX = 0.5*math.pi*(mPosY/self.centerY -1)
        speed = 3*math.pi/180 #< 3 deg
        self.attZ += (keys[self.tiltRight] -keys[self.tiltLeft])*speed
        return self.getAttitude()

    def updatePos(self, keys, mPosX, mPosY, speed) -> list:
        self.posX += -(keys[self.moveRightKey] -keys[self.moveLeftKey])*2.0*speed
        self.posY += -(keys[self.moveUpKey]    -keys[self.moveDownKey])*2.0*speed
        self.posZ += -(keys[self.moveFwdKey]   -keys[self.moveBackKey])*5.0*speed
        return self.getPosition()
