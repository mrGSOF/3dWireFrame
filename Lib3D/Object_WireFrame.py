from Lib3D import Object_base as O

class Object_wireFrame(O.Object_base):
    def __init__(self, obj):
        self.Color  = obj["color"]
        self.lines  = obj["lines"]
        self.points = obj["points_xyz"]
        self.scale(obj["scale"], state=True)
        self.nPoints = self.point

    def scale(self, scale, state=False):
        points = scale( self.obj["points_xyz"], scale )
        if state == True:
            self.points = points
        else:
            self.nPoints = points
        return self

    def rotate(self, x, y, z, state=False):
        return self

    def translate(self, x, y, z, state=False):
        return self

    def getLines(self) -> list:
        lines = [0]*len(self.lines)
        for i,line in enumerate(lines):
            fromPnt, toPnt = line
            p0 = points[fromPnt]
            p1 = points[toPnt]
            lines[i]=(p0,p1)
        return lines
