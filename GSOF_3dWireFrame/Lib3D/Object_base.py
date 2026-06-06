from GSOF_3dWireFrame.MathLib import MathLib as ML
from GSOF_3dWireFrame.Lib3D import Lib3D as L

class Object_base():
    def __init__(self):
        self.stateOrigin = ML.I(4) #< 4x4 matrix to store the original state of scale, rotation and translations
        self.reset()               #< 4x4 matrix to store the currect state

    def reset(self, all=True):
        """Reset current state to original"""
        self.state = copy.copydeep(self.stateOrigin) #< 4x4 matrix to store the currect state
        return self

    def setOrigin(self, newState=None):
        """Set current state as the new original state"""
        
        if newState == None:
            newState = self.stateOrigin
        self.stateOrigin = copy.copydeep(newState)
        return self

    def getOrigin(self) -> list:
        """Get the original state"""
        return copy.copydeep(self.stateOrigin)

    def _findCenter(self,
                    method: str="arithCenter",
                    points: list|tuple
                    ) -> list:
        """Return the center point of all points"""
        if method == "arithCenter":
            return L.findArithmeticCenter(points)
            
        elif method == "minMaxCenter":
            return L.findMinMaxCenter(points)

        elif method == None:
            return self.getOrigin()

        else:
            return None

    def scale(self, scale):
        """Apply scaling to curent state"""
        self.state[0][0] *= scale[0]
        self.state[1][1] *= scale[1]
        self.state[2][2] *= scale[2]
        return self
    
    def copyDcmIntoState(self, dcm: list) -> None:
        #self.state = ML.copyIntoMatrix(self.state, dcm, rs=0, cs=0)
        for ri, row in enumerate(dcm):
            for ci, val in enumerate(row):
                self.state[ri][ci] = val

    def rotate(self, x: float, y: float, z: float, dcm: list):
        """Apply rotation to curent state"""
        if dcm == None:
            dcm = L.getRotationMatrix(x, y, z)
        self.copyDcmIntoState(ML.MxM(self.state, dcm)
        return self

    def translate(self, x, y, z):
        """Apply translation to curent state"""
        self.state[0][3] += x
        self.state[1][3] += y
        self.state[2][3] += z
        return self

    def transform(self, scale: list, rotate: list, translate: list):
        """Apply transformation to curent state"""
        self\
        .scale(scale)\
        .rotate(rotate)\
        .translate(translate)
        return self

    def update(self, state) -> None:
        """Apply transformation matrix to state"""
        self.state = L.updateTransformationMatrix(self.state, state)

    def getLines(self) -> list:
        """Return all lines of object"""
        return []

    def getObjects(self) -> list: #< For compatibility with Assembly class
        """Return a list of all objects"""
        return []
