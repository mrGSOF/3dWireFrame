from Lib3D import Object_base as O
import json

class Object_wireFrame(O.Object_base):
    def __init__(self, obj=None, filename=None, color=(0,0,0)):
        if filename != None:
            obj = self.loadJson(filename)

        self.color  = color
        self.lines  = obj["lines"]
        self.initPoints = obj["points_xyz"]
        self.scale(obj["scale"], state=True)

    def _updateState(self, points, updateInit):
        if updateInit == True:
            self.initPoints = points
        self.newPoints = points

    def loadJson(self, filename):
        obj = None
        with open(filename) as f:
            obj = json.load(f)
        return obj

    def scale(self, scale, state=False):
        points = O.scale(self.initPoints, scale)
        self._updateState( points, state )
        return self
        
    def rotate(self, x=0, y=0, z=0, dcm=None, state=False):
        points = O.rotate( self.initPoints, x,y,z, dcm )
        self._updateState( points, state )
        return self

    def translate(self, x=0, y=0, z=0, V=None, state=False):
        points = O.translate( self.initPoints, x,y,z, V )
        self._updateState( points, state )
        return self

    def setLines(self, points, connections) -> list:
        lines = [0]*len(connections)
        for i,line in enumerate(connections):
            fromPnt, toPnt = line
            p0 = self.points[fromPnt]
            p1 = self.points[toPnt]
            lines[i]=(p0,p1)
        return lines

    def setLines(self, points, connections) -> list:
        lines = [0]*len(connections)
        for i,line in enumerate(connections):
            fromPnt, toPnt = line
            p0 = self.points[fromPnt]
            p1 = self.points[toPnt]
            lines[i]=(p0,p1)
        return lines

    def getLines(self) -> list:
        lines = [0]*len(self.lines)
        for i,line in enumerate(self.lines):
            fromPnt, toPnt = line
            p0 = self.newPoints[fromPnt]
            p1 = self.newPoints[toPnt]
            lines[i]=(p0,p1)
        return lines
