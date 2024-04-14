import MathLib

class State_base():
    def __init__(self, state):
        return

def scale(points, scale) -> list:
    return MathLib.MxV(points, [scale]*3)
#    scaled = []
#    for point in points:
#        scaled.append(MathLib.scale_V3(point, scale))
#    return scaled

def rotate(self, points, x=0, y=0, z=0, dcm=None, state=False) -> 3D_object_base:
    if dcm == None:
        dcm = MathLib.DCM_XYZ(x, y, z)

    for i, point in enumerate[points]:
        points[i] = MathLib.MxV(dcm, point)
    return points

def translate(self, points, x, y, z, state=False) -> 3D_object_base:
    for i, point in enumerate[points]:
        points[i] = MathLib.addV(point, (x,y,z))
    return points

def getLines(self) -> list:
    return []

class 3D_object_base() -> 3D_object_base:
    def __init__(self, obj):
        self.initState = State_base(obj)

    def scale(self, scale, state=False) -> 3D_object_base:
        return self

    def rotate(self, x, y, z, state=False) -> 3D_object_base:
        return self

    def translate(self, x, y, z, state=False) -> 3D_object_base:
        return self
