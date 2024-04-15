from Lib3D import Object_base as O
import json

class Object_wireFrame(O.Object_base):
    def __init__(self, obj=None, filename=None, color=(0,0,0)):
        if filename != None:
            obj = self._loadJson(filename)

        self.color  = color
        self.initShape = self._calcShape(obj["points_xyz"], obj["connections"])
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

    def _calcShape(self, points, connections) -> list:
        shape = [0]*len(connections)
        for i, connect in enumerate(connections):
            fromPnt, toPnt = connect
            p0 = points[fromPnt]
            p1 = points[toPnt]
            shape[i] = (p0,p1)
        return shape

    def scale(self, scale, initShape=False):
        shape = O.scale(self.initShape, scale)
        self._updateShape( shape, initShape )
        return self
        
    def rotate(self, x=0, y=0, z=0, dcm=None, initShape=False):
        shape = O.rotate( self.initShape, x,y,z, dcm )
        self._updateShape( shape, initShape )
        return self

    def translate(self, x=0, y=0, z=0, V=None, initShape=False):
        shape = O.translate( self.initShape, x,y,z, V )
        self._updateShape( shape, initShape )
        return self

    def getShape(self) -> list:
        return self.shape

    def getLines(self) -> list:
        return self.shape

##    def setLines(self, points, connections) -> list:
##        lines = [0]*len(connections)
##        for i,line in enumerate(connections):
##            fromPnt, toPnt = line
##            p0 = self.points[fromPnt]
##            p1 = self.points[toPnt]
##            lines[i]=(p0,p1)
##        return lines

##    def getLines(self) -> list:
##        lines = [0]*len(self.lines)
##        for i,line in enumerate(self.shapes):
##            fromPnt, toPnt = line
##            p0 = self.newPoints[fromPnt]
##            p1 = self.newPoints[toPnt]
##            lines[i]=(p0,p1)
##        return lines
