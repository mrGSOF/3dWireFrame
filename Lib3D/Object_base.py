from MathLib import MathLib as ML

def scale(points, scale) -> list:
    newPoints = [None]*len(points)
    for i,point in enumerate(points):
        newPoints[i] = ML.scale_V3(point, scale)
    return newPoints

def rotate(points, x=0, y=0, z=0, dcm=None, state=False) -> list:
    newPoints = [None]*len(points)
    if dcm == None:
        dcm = ML.DCM_XYZ(x, y, z)

    for i, point in enumerate(points):
        newPoints[i] = ML.MxV(dcm, point)
    return newPoints

def translate(points, x=0, y=0, z=0, V=None, state=False) -> list:
    newPoints = [None]*len(points)
    if V == None:
        V = (x, y, z)

    for i, point in enumerate(points):
        newPoints[i] = ML.addV(point, V)
    return newPoints

def getLines(self) -> list:
    return []

class Object_base():
    def __init__(self, obj=None, filename=None):
        return

    def loadJson(self, filename):
        return self

    def scale(self, scale, state=False):
        return self

    def rotate(self, x, y, z, state=False):
        return self

    def translate(self, x, y, z, state=False):
        return self

    def getLines(self):
        return []
