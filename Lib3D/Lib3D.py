from MathLib import MathLib as ML

def dataToDict(points, lines):
    return({"scale":1.0,
                  "points_xyz": points,
                  "connections": lines})

def findArithmeticCenter(points):
    """ Return the arithmetic center from the list of points """
    mean = [0]*(len(points[0]))

    for axis in points:
        for i in range(len(axis)):
            mean[i]+=axis[i]
    for i in range(len(mean)):
        mean[i] = mean[i]/len(points)
    return mean

def findMinMaxCenter(points):
    """ Return the center point between the minimum and maximum
        values in the list of points """
    Max = 999999
    Min = -Max
    N = len(points[0])
    minPoint = [Max]*N
    maxPoint = [Min]*N
    for point in points:
        for i, v in enumerate(point):
            if v < minPoint[i]:
                minPoint[i] = v
            if v > maxPoint[i]:
                maxPoint[i] = v

    meanPoint = [0,0,0]
    for i in range(N):
        meanPoint[i] = (minPoint[i]+maxPoint[i])/2
    return meanPoint

def scale(points, scale) -> list:
    newPoints = [None]*len(points)
    for i,point in enumerate(points):
        newPoints[i] = ML.scale_V3(point, scale)
    return newPoints

def rotate(points, x=0, y=0, z=0, dcm=None) -> list:
    newPoints = [None]*len(points)
    if dcm == None:
        dcm = ML.DCM_XYZ(x, y, z)
        #dcm = ML.DCM_ZYX(z, y, x)

    for i, point in enumerate(points):
        newPoints[i] = ML.MxV(dcm, point)
        #np = ML.MxV(dcm, [point[0], point[2], point[1]])
        #newPoints[i] = [np[0],np[2],np[1]] 
    return newPoints

def translate(points, x=0, y=0, z=0, V=None) -> list:
    newPoints = [None]*len(points)
    if V == None:
        V = (x, y, z)

    for i, point in enumerate(points):
        newPoints[i] = ML.addV(point, V)
    return newPoints

def calcLines(points, connections) -> list:
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
        self.p0, self.p1 = scale([self.p0, self.p1], scale)

    def translate(self, x=0, y=0, z=0, V=None):
        self.p0, self.p1 = translate([self.p0, self.p1], x,y,z,V)
    
    def rotate(self, x=0, y=0, z=0, dcm=None):
        self.p0, self.p1 = rotate([self.p0, self.p1], x,y,z,dcm)
