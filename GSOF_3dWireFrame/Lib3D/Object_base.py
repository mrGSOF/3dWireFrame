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
        self.stateTouched = True
        return self

    def setOrigin(self, newState=None):
        """Set current state as the new original state"""
        if newState == None:
            newState = self.state
        self.stateOrigin = copy.deepcopy(newState)
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
            return (0,0,0)
        
        else:
            return None

    def scale(self, scale: list|tuple|float):
        """Apply scaling to current state"""
        """Apply scaling to current state"""
        if not isinstance(scale, (list, tuple)):
            scale = (scale,)*3
        scaleM = ML.I(4)
        scaleM[0][0] = scale[0]
        scaleM[1][1] = scale[1]
        scaleM[2][2] = scale[2]
        self.state = ML.MxM(self.state, scaleM)
        self.stateTouched = True
        return self
    
    def copyDcmIntoState(self, dcm: list) -> None:
        #self.state = ML.copyIntoMatrix(self.state, dcm, rs=0, cs=0)
        for ri, row in enumerate(dcm):
            for ci, val in enumerate(row):
                self.state[ri][ci] = val

    def rotate(self, x: float, y: float, z: float, dcm: list=None):
        """Apply rotation to current state"""
        if dcm == None:
            dcm = L.getRotationMatrix(x, y, z)
        if centerAt == None:
            #self.copyDcmIntoState(ML.MxM(self.state[0:3], dcm))
            dcm[0] += [0]
            dcm[1] += [0]
            dcm[2] += [0]
        else:
            tx, tz, tz = -centerAt[0],-centerAt[1],-centerAt[2]
            r = dcm
            dcm[0] += [tx*(1-r[0][0]) -r[0][1]*ty -r[0][2]*tz]
            dcm[1] += [ty*(1-r[1][1]) -r[1][0]*tx -r[1][2]*tz]
            dcm[2] += [tz*(1-r[2][2]) -r[2][0]*tx -r[2][1]*ty]
        dcm += [[0,0,0,1]]
        self.state = ML.MxM(dcm, self.state)
        self.stateTouched = True
        return self

    def translate(self, x, y, z):
        """Apply translation to current state"""
        transM = ML.I(4)
        transM[0][3] += x
        transM[1][3] += y
        transM[2][3] += z
        self.state = ML.MxM(transM, self.state)
        self.stateTouched = True
        return self

    def transform(self,
                  scale: list=(1,1,1),
                  rotate: list=(0,0,0),
                  translate: list=(0,0,0),
                  transMatrix: list=None
                  ):
        """Apply transformation to current state"""
        if transMatrix == None:
            self\
            .scale(scale)\
            .rotate(*rotate)\
            .translate(*translate)
        else:
            self.state = L.updateTransformationMatrix(self.state, transMatrix)
        self.stateTouched = True
        return self

    def isUpdated(self) -> bool:
        return not bool(self.stateTouched)

    def update(self) -> None:
        self.stateTouched = False

    def getLines(self) -> list:
        """Return all lines of object"""
        return []

    def getObjects(self) -> list: #< For compatibility with Assembly class
        """Return a list of all objects"""
        return []
