from GSOF_3dWireFrame.MathLib import MathLib as ML
import json
from GSOF_3dWireFrame.Lib3D import stlToObj

def loadStl(filename, faceCount=500):
    return stlToObj.stlToObj(filename, faceCount=faceCount)

def loadJson(filename):
    obj = None
    with open(filename) as f:
        obj = json.load(f)
    return obj

def dataToDict(points, lines, scale=1.0, color=(0,0,0)):
    return({"scale":scale,
            "color":color,
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

def scalePoint(point, scale, dim) -> list:
    new = [0]*dim
    for i in range(0, dim):
        new[i] = point[i]*scale[i]
    return new
        
def scale(points, _scale) -> list:
    """Scale coordinates"""
    dim = len(points[0])
    if not isinstance(_scale, (tuple,list)):
        _scale = (_scale,)*dim
    newPoints = [None]*len(points)
    for i, point in enumerate(points):
        newPoints[i] = scalePoint(point, _scale, dim)
    return newPoints

def getRotationMatrix(x=0, y=0, z=0) -> list:
    """Return the proper rotation matrix for our coordinate system"""
    return ML.DCM_YXZ(y, x, z) #< the proper rotation order for our coordinate system

def getTransformMatrix(scale=(1,1,1), rotate=(0,0,0), translate=(0,0,0)) -> list:
    """Return the transformation matrix"""
    M = getRotationMatrix(*rotate)
    scaleM = ML.I(3)
    scaleM[0][0] = scale[0]
    scaleM[1][1] = scale[1]
    scaleM[2][2] = scale[2]
    M = ML.MxM(M, scaleM)
    M[0] += [translate[0]] #< Add translation
    M[1] += [translate[1]]
    M[2] += [translate[2]]
    return M +[[0,0,0,1]]    #< Add last row and return

def updateTransformationMatrix(oldT, newT) -> list:
    return ML.MxM(newT, oldT)
    
def rotate(points, x=0, y=0, z=0, dcm=None) -> list:
    newPoints = [None]*len(points)
    if dcm == None:
        dcm = getRotationMatrix(x, y, z)

    for i, point in enumerate(points):
        newPoints[i] = ML.MxV(dcm, point)
    return newPoints

def translate(points, x=0, y=0, z=0) -> list:
    newPoints = [None]*len(points)
    T = [x, y, z]
    for i, point in enumerate(points):
        newPoints[i] = ML.addV(point, T)
    return newPoints

def transform(points, _scale=(1,1,1), _rotate=(0,0,0), _translate=(0,0,0), M=None) -> list:
    if M == None:
        M = getTransformMatrix(_scale, _rotate, _translate)
    return _update(points, M)
##    points = scale(points, _scale) #< Inefficient method
##    points = rotate(points, *_rotate)
##    return translate(points, *_translate)

def _update(points, transformation) -> list:
    newPoints = [None]*len(points)
    for i, point in enumerate(points):
        point += [1] #< Add translation dimension
        newPoints[i] = (ML.MxV(transformation, point))[0:3]
    return newPoints

def calcLines(points, connections, color=(0,0,0)) -> list:
    lines = [0]*len(connections)
    for i, connect in enumerate(connections):
        fromPnt, toPnt = connect
        p0 = points[fromPnt]
        p1 = points[toPnt]
        lines[i] = Line(p0, p1, color)
    return lines

class Line():
    def __init__(self, p0=None, p1=None, color=(0,0,0)):
        self.points = [p0, p1]
        self.color = color
### THE METHODS BELOW ARE NOT USED
##    def scale(self, scale):
##        self.points = scale(self.points, scale)
##
##    def translate(self, x=0, y=0, z=0):
##        self.points = translate(self.points, x,y,z)
##    
##    def rotate(self, x=0, y=0, z=0, dcm=None):
##        self.points = rotate(self.points, x,y,z,dcm)

class Triangle(Line):
    def __init__(self, p0=None, p1=None, p2=None, color=(0,0,0)):
        super().__init__(p0, p1, color)
        self.points += [p2]
