import copy
from GSOF_3dWireFrame.MathLib import MathLib as ML
from GSOF_3dWireFrame.Lib3D import Lib3D as L

class Object_base():
    def __init__(self):
        self.stateOrigin = ML.I(4) #< 4x4 matrix to store the original state of scale, rotation and translations
        self.reset()               #< 4x4 matrix to store the currect state

    def reset(self, all=True):
        """Reset current state to original"""
        self.state = self.getOrigin() #< 4x4 matrix to store the currect state
        self.updated = False
        return self

    def setOrigin(self, newState=None):
        """Set current state as the new original state"""
        
        if newState == None:
            newState = self.stateOrigin
        self.stateOrigin = copy.deepcopy(newState)
        self.update = False
        return self

    def getOrigin(self) -> list:
        """Get the original state"""
        return copy.deepcopy(self.stateOrigin)

    def _findCenter(self,
                    points: list|tuple,
                    method: str="arithCenter"
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

    def scale(self, scale: list|float):
        """Apply scaling to curent state"""
        if not isinstance(scale, (list, tuple)):
            scale = (scale,)*3
        self.state[0][0] *= scale[0]
        self.state[1][1] *= scale[1]
        self.state[2][2] *= scale[2]
        self.update = False
        return self
    
    def copyDcmIntoState(self, dcm: list) -> None:
        #self.state = ML.copyIntoMatrix(self.state, dcm, rs=0, cs=0)
        print(dcm)
        for ri, row in enumerate(dcm):
            print(row)
            for ci, val in enumerate(row):
                self.state[ri][ci] = val

    def rotate(self, x: float, y: float, z: float, dcm: list=None):
        """Apply rotation to curent state"""
        print(dcm)
        if dcm == None:
            dcm = L.getRotationMatrix(x, y, z)
        print(dcm)
        self.copyDcmIntoState(ML.MxM(self.state[0:3], dcm))
        self.stateTouched = False
        return self

    def translate(self, x, y, z):
        """Apply translation to curent state"""
        self.state[0][3] += x
        self.state[1][3] += y
        self.state[2][3] += z
        self.update = False
        return self

    def transform(self,
                  scale: list=(1,1,1),
                  rotate: list=(0,0,0),
                  translate: list=(0,0,0),
                  transMatrix: list=None
                  ):
        """Apply transformation to curent state"""
        if transMatrix == None:
            self\
            .scale(scale)\
            .rotate(rotate)\
            .translate(translate)
        else:
            self.state = L.updateTransformationMatrix(self.state, transMatrix)
        self.update = False
        return self

    def isUpdated(self) -> bool:
        return bool(self._updated)

    def update(self) -> None:
        self.update = True

    def getLines(self) -> list:
        """Return all lines of object"""
        return []

    def getObjects(self) -> list: #< For compatibility with Assembly class
        """Return a list of all objects"""
        return []
