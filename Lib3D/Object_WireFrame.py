from MathLib import MathLib as ML
from Lib3D import Object_base as O
from Lib3D import Lib3D as L
from Lib3D import stlToObj
import json

class Object_wireFrame(O.Object_base):
    def __init__(self, obj=None, filename=None, color=(0,0,0)):
        if filename != None:
            ext = filename.split(".")[-1]
            if ext == "json":
                obj = self._loadJson(filename)
            elif ext == "stl":
                obj = self.loadStl(filename)

        self.color  = color
        self.initShape   = obj["points_xyz"]
        self.connections = obj["connections"]
        self.reset().scale(obj["scale"], initShape=True)

    def _updateShape(self, initShape=False):
        if initShape == True:
            self.initShape = self.shape

    def _loadJson(self, filename):
        obj = None
        with open(filename) as f:
            obj = json.load(f)
        return obj

    def loadStl(self, filename, faceCount=500):
        return stlToObj.stlToObj(filename, faceCount=faceCount)

    def reset(self):
        self.shape = self.initShape
        return self

    def scale(self, scale, initShape=False, elements=[]):
        self.shape = L.scale(self.shape, scale)
        self._updateShape( initShape )
        return self
        
    def rotate(self, x=0, y=0, z=0, dcm=None, initShape=False, elements=[], origin=(0,0,0)):
        shape = self.shape
        if origin == "arithCenter":
            origin = L.findArithmeticCenter(shape)

        if origin == "minMaxCenter":
            origin = L.findMinMaxCenter(shape)

        if origin != (0,0,0):
            for axis in range(len(shape)):
                for i in range(len(shape[axis])):
                    shape[axis][i]-=origin[i]

        shape = L.rotate( shape, x,y,z, dcm )

        if origin != (0,0,0):
            for axis in range(len(shape)):
                for i in range(len(shape[axis])):
                    shape[axis][i]+=origin[i]

        self.shape = shape
        self._updateShape( initShape )
        return self

    def translate(self, x=0, y=0, z=0, V=None, initShape=False, elements=[], origin=(0,0,0)):
        self.shape = L.translate( self.shape, x,y,z, V )
        self._updateShape( initShape )
        return self

    def getShape(self) -> list:
        return self.shape

    def getLines(self) -> list:
        return L.calcLines(self.shape, self.connections)
