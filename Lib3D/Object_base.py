from MathLib import MathLib as ML

def scale(points, scale) -> list:
    newPoints = [None]*len(points)
    for i,point in enumerate(points):
        #newPoints[i] = ML.scale_V3(point, scale)
        p0 = ML.scale_V3(point[0], scale)
        p1 = ML.scale_V3(point[1], scale)
        newPoints[i] = (p0, p1)
    return newPoints

def rotate(points, x=0, y=0, z=0, dcm=None, state=False) -> list:
    newPoints = [None]*len(points)
    if dcm == None:
        dcm = ML.DCM_XYZ(x, y, z)

    for i, point in enumerate(points):
        #newPoints[i] = ML.MxV(dcm, point)
        p0 = ML.MxV(dcm, point[0])
        p1 = ML.MxV(dcm, point[1])
        newPoints[i] = (p0, p1)
    return newPoints

def translate(points, x=0, y=0, z=0, V=None, state=False) -> list:
    newPoints = [None]*len(points)
    if V == None:
        V = (x, y, z)

    for i, point in enumerate(points):
        #newPoints[i] = ML.addV(point, V)
        p0 = ML.addV(point[0], V)
        p1 = ML.addV(point[1], V)
        newPoints[i] = (p0, p1)
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

    def rotate(self, x, y, z, dcm, state=False):
        return self

    def translate(self, x, y, z, V, state=False):
        return self

    def getShape(self):
        return []

    def getLines(self):
        return []

class Object_container(Object_base):
    def __init__(self, objList=[]):
        self.shapes = objList

    def scale(self, scale, initShape=False):
        for shape in shapes:
            shape.scale(scale, initShape)
        return self

    def rotate(self, x=0, y=0, z=0, dcm=None, initShape=False):
        for shape in shapes:
            shape.rotate(x, y, z, dcm, initShape)
        return self

    def translate(self, x=0, y=0, z=0, V=None, initShape=False):
        for shape in shapes:
            shape.translate(x, y, z, dcm, initShape)
        return self

    def getShape(self):
        return []

    def getLines(self):
        return []

    
