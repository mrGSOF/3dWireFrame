from MathLib import MathLib as ML
from Lib3D import Object_base as O
from Lib3D import Lib3D as L
from Lib3D import stlToObj
import json

class Object_wireFrame(O.Object_base):
    def __init__(self, obj=None, filename=None, color=None):
        if filename != None:
            ext = filename.split(".")[-1]
            if ext == "json":
                obj = self._loadJson(filename)
            elif ext == "stl":
                obj = self.loadStl(filename)

        if color == None:
            if "color" in obj:
                color = obj["color"]  #< Color from file
            else:
                color = (0,0,0)       #< Default color
        self.color       = color               #< The color to draw all lines (from file, overriden, or default)
        self.initShape   = obj["points_xyz"]   #< List of original xyz-coordinates of all corner-points in the shape
        self.shape       = obj["points_xyz"]   #< List of manipulated xyz-coordinates of all corner-points in the shape
        self.connections = obj["connections"]  #< List of interconnected points that form a line
        self.reset().scale(obj["scale"], initShape=True) #< Scale the coordinates of all points and store

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

    def getOrigin(self, origin=None, elements=[] ):
        if origin == "arithCenter":
            points = self.getShape()
            return L.findArithmeticCenter(points)
            
        elif origin == "minMaxCenter":
            points = self.getShape()
            return L.findMinMaxCenter(points)

        else:
            return self.origin

    def setOrigin(self, origin, initShape=False, elements=[]):
        if initShape == True:
            shape = self.initShape #< Modify the original points
        else:
            shape = self.shape     #< Modify the temporary points

        if origin != (0,0,0):
            ### If new origin is different offset all points
            for axis in range(len(shape)):
                for i in range(len(shape[axis])):
                    shape[axis][i] -= origin[i]
        return self
        
    def scale(self, scale, initShape=False, elements=[]):
        self.shape = L.scale(self.shape, scale)
        self._updateShape( initShape )
        return self
        
    def rotate(self, x=0, y=0, z=0, dcm=None, initShape=False, elements=[], origin=(0,0,0)):
        self.shape = L.rotate( self.shape, x,y,z, dcm )
        self._updateShape( initShape )
        return self

    def translate(self, x=0, y=0, z=0, V=None, initShape=False, elements=[], origin=(0,0,0)):
        self.shape = L.translate( self.shape, x,y,z, V )
        self._updateShape( initShape )
        return self

    def getShape(self) -> list:
        return self.shape

    def getLines(self) -> list:
        return L.calcLines(self.shape, self.connections, self.color)
