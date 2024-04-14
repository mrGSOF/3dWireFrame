import 3D_object_base as *

class 3D_object_wireFrame(3D_object_base):
    def __init__(self, obj) -> 3D_object_wireFrame:
        #self.obj = obj
        self.Color =  obj["color"]
        self.lines =  obj["lines"]
        self.points = obj["points_xyz"]
        self.scale(obj["scale"])
        self.nPoints = self.point

    def scale(self, scale, state=False) -> 3D_object_wireFrame:
        self.points = self.obj["points_xyz"] #scale
        return self

    def rotate(self, x, y, z, state=False) -> 3D_object_wireFrame:
        return self

    def translate(self, x, y, z, state=False) -> 3D_object_wireFrame:
        return self

    def getLines(self) -> list:
        lines = [0]*len(self.lines)
        for i,line in enumerate(lines):
            fromPnt, toPnt = line
            p0 = points[fromPnt]
            p1 = points[toPnt]
            lines[i]=(p0,p1)
        return lines
