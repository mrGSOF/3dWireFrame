from GSOF_3dWireFrame.MathLib import MathLib as ML
from GSOF_3dWireFrame.Lib3D import Lib3D as L

class Object_base():
    def __init__(self):
        self.stateOrigin = ML.I(4) #< 4x4 matrix to store the original state of scale, rotation and translations
        self.reset()               #< 4x4 matrix to store the currect state

    def setOrigin(self, setInitState=True):
        """Set current state as the new original state"""
        if setInitState != False:
            self.stateOrigin = copy.copydeep(self.state)
        return self

    def getOrigin(self ):
        """Get the original state"""
        return self.stateOrigin

    def reset(self, newState=None):
        """Reset current state to original or new state"""
        state = self.stateOrigin if newState == None else newState
        self.state = copy.copydeep(state) #< 4x4 matrix to store the currect state
        return self
    
    def scale(self, scale, setInitState=False):
        """Apply scaling to curent state"""
        self.state[0][0] *= scale[0]
        self.state[1][1] *= scale[1]
        self.state[2][2] *= scale[2]
        self.setOrigin(setInitState)
        return self

    def rotate(self, x, y, z, dcm, setInitState=False):
        """Apply rotation to curent state"""
        self.setOrigin(setInitState)
        return self

    def translate(self, x, y, z, setInitState=False):
        """Apply translation to curent state"""
        self.state[0][3] += x
        self.state[1][3] += y
        self.state[2][3] += z
        self.setOrigin(setInitState)
        return self

    def transform(self, scle, rotate, translate, setInitState=False):
        """Apply transformation to curent state"""
        self.setOrigin(setInitState)
        return self
