from MathLib import MathLib as ML

def _scale(points, scale) -> list:
    newPoints = [None]*len(points)
    for i,point in enumerate(points):
        newPoints[i] = ML.scale_V3(point, scale)
    return newPoints

def _rotate(points, x=0, y=0, z=0, dcm=None) -> list:
    newPoints = [None]*len(points)
    if dcm == None:
        dcm = ML.DCM_XYZ(x, y, z)
        #dcm = ML.DCM_ZYX(z, y, x)

    for i, point in enumerate(points):
        newPoints[i] = ML.MxV(dcm, point)
        #np = ML.MxV(dcm, [point[0], point[2], point[1]])
        #newPoints[i] = [np[0],np[2],np[1]] 
    return newPoints

def _translate(points, x=0, y=0, z=0, V=None) -> list:
    newPoints = [None]*len(points)
    if V == None:
        V = (x, y, z)

    for i, point in enumerate(points):
        newPoints[i] = ML.addV(point, V)
    return newPoints

def _calcLines(points, connections) -> list:
    lines = [0]*len(connections)
    for i, connect in enumerate(connections):
        fromPnt, toPnt = connect
        p0 = points[fromPnt]
        p1 = points[toPnt]
        lines[i] = Line(p0,p1)
    return lines


class Line():
    def __init__(self, p0=None, p1=None, color=(0,0,0)):
        self.p0 = p0
        self.p1 = p1
        self.color = color

    def scale(self, scale):
        self.p1, self.p2 = _scale([self.p1, self.p2], scale)

    def translate(self, x=0, y=0, z=0, V=None):
        self.p1, self.p2 = _translate([self.p1, self.p2], x,y,z,V)
    
    def rotate(self, x=0, y=0, z=0, dcm=None):
        self.p1, self.p2 = _rotate([self.p1, self.p2], x,y,z,dcm)
