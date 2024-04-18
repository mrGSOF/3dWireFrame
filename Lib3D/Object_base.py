from MathLib import MathLib as ML

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
        for shape in self.shapes:
            shape.scale(scale, initShape)
        return self

    def rotate(self, x=0, y=0, z=0, dcm=None, initShape=False):
        for shape in self.shapes:
            shape.rotate(x, y, z, dcm, initShape)
        return self

    def translate(self, x=0, y=0, z=0, V=None, initShape=False):
        for shape in self.shapes:
            shape.translate(x, y, z, V, initShape)
        return self

    def getShape(self):
        shapes = []
        for shape in self.shapes:
            shapes += shape.getShape()
        return shapes

    def getLines(self):
        lines = []
        for shape in self.shapes:
            lines += shape.getLines()
        return lines

    
