from MathLib import MathLib as ML
from Lib3D import Object_base as O
import json

def _scale(points, scale) -> list:
    newPoints = [None]*len(points)
    for i,point in enumerate(points):
        newPoints[i] = ML.scale_V3(point, scale)
    return newPoints

def _rotate(points, x=0, y=0, z=0, dcm=None, state=False) -> list:
    newPoints = [None]*len(points)
    if dcm == None:
        dcm = ML.DCM_XYZ(x, y, z)

    for i, point in enumerate(points):
        newPoints[i] = ML.MxV(dcm, point)
    return newPoints

def _translate(points, x=0, y=0, z=0, V=None, state=False) -> list:
    newPoints = [None]*len(points)
    if V == None:
        V = (x, y, z)

    for i, point in enumerate(points):
        newPoints[i] = ML.addV(point, V)
    return newPoints

def _calcLines(points, connections) -> list:
    shape = [0]*len(connections)
    for i, connect in enumerate(connections):
        fromPnt, toPnt = connect
        p0 = points[fromPnt]
        p1 = points[toPnt]
        shape[i] = (p0,p1)
    return shape

class Object_wireFrame(O.Object_base):
    def __init__(self, obj=None, filename=None, color=(0,0,0)):
        if filename != None:
            obj = self._loadJson(filename)

        self.color  = color
        self.initShape   = obj["points_xyz"]
        self.connections = obj["connections"]
        self.scale(obj["scale"], initShape=True)

    def _updateShape(self, shape, initShape=False):
        if initShape == True:
            self.initShape = shape
        self.shape = shape

    def _loadJson(self, filename):
        obj = None
        with open(filename) as f:
            obj = json.load(f)
        return obj

    def scale(self, scale, initShape=False):
        shape = _scale(self.initShape, scale)
        self._updateShape( shape, initShape )
        return self
        
    def rotate(self, x=0, y=0, z=0, dcm=None, initShape=False):
        shape = _rotate( self.initShape, x,y,z, dcm )
        self._updateShape( shape, initShape )
        return self

    def translate(self, x=0, y=0, z=0, V=None, initShape=False):
        shape = _translate( self.initShape, x,y,z, V )
        self._updateShape( shape, initShape )
        return self

    def getShape(self) -> list:
        return self.getShape()

    def getLines(self) -> list:
        return _calcLines(self.shape, self.connections)
