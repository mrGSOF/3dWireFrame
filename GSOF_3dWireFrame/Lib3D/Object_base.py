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

    def getOrigin(self) -> list:
        """Get the original state"""
        return self.stateOrigin

    def reset(self, all=True):
        """Reset current state to original"""
        self.state = copy.copydeep(stateOrigin) #< 4x4 matrix to store the currect state
        return self

    def _findCenter(self,
                    method: str="arithCenter",
                    points: list|tuple
                    ) -> list:
        """Return the center point of all points"""
        if origin == "arithCenter":
            return L.findArithmeticCenter(points)
            
        elif origin == "minMaxCenter":
            return L.findMinMaxCenter(points)

        elif origin == None:
            return self.getOrigin()

    def copyDcmIntoState(self, dcm) -> None:
        for ri, row in enumerate(dcm):
            for ci, val in enumerate(row):
                self.state[ri][ci] = val

    def scale(self, scale, setInitState=False):
        """Apply scaling to curent state"""
        self.state[0][0] *= scale[0]
        self.state[1][1] *= scale[1]
        self.state[2][2] *= scale[2]
        self.setOrigin(setInitState)
        return self
    
    def rotate(self, x, y, z, dcm, setInitState=False):
        """Apply rotation to curent state"""
        if dcm == None:
            dcm = ML.DCM_YXZ(y, x, z) #< This is the proper rotation order for our coordinate system
        self.copyDcmIntoState(ML.MxM(self.state, dcm)
        self.setOrigin(setInitState)
        return self

    def translate(self, x, y, z, setInitState=False):
        """Apply translation to curent state"""
        self.state[0][3] += x
        self.state[1][3] += y
        self.state[2][3] += z
        self.setOrigin(setInitState)
        return self

    def transform(self, scale, rotate, translate, setInitState=False):
        """Apply transformation to curent state"""
        self.state\
        .scale(scale, si)\
        .rotate(rotate, si)\
        .translate(translate, si)
        self.setOrigin(setInitState)
        return self

    def getLines(self) -> list:
        """Return all lines of object"""
        return []

    def update(self, state) -> None:
        """Update the coordinates of all points of the object"""
        self.state = L.updateTransformationMatrix(self.state, state)

    def getObjects(self) -> list: #< For compatibility with Assembly class
        """Return a list of all objects"""
        return []
