from GSOF_3dWireFrame.Lib3D import Lib3D as L
from GSOF_3dWireFrame.Lib3D.Object_base import *

class Object_wireFrame(Object_base):
    OBJ_NUM = 0
    def __init__(self, obj=None, filename=None, color=None, name=None):
        if name == None:
            name = "O" +str(Object_wireFrame.OBJ_NUM)
            Object_wireFrame.OBJ_NUM += 1
        self.name = name    
        super().__init__()
        if filename != None:
            ext = filename.split(".")[-1]
            if ext == "json":
                obj = L.loadJson(filename)
            elif ext == "stl":
                obj = L.loadStl(filename)

        if color == None:
            if "color" in obj:
                color = obj["color"]  #< Color from file
            else:
                color = (0,0,0)       #< Default color black
        self.color       = color               #< Color to draw all lines
        self.points      = obj["points_xyz"]   #< xyz-coordinates of all corner-points of object
        self.connections = obj["connections"]  #< Lines between corner points of object
    
    def update(self) -> None:
        self.newPoints = L.transform(points=self.points, M=self.state)
        self.stateTouched = True

    def getLines(self) -> list:
        if not self.isUpdated():
            self.update()
        return L.calcLines(self.newPoints, self.connections, self.color)

    def setCenter(self,
                  pos=(0,0,0),
                  rotate=(0,0,0),
                  scale=(1,1,1),
                  method=None
                  ):
        """Move all original points to the new location than rotate and scale"""
        ### Find new center and translate all points
        center = super()._findCenter(self.points, method)
        translate = (-(pos[0]+center[0]), -(pos[1]+center[1]), -(pos[2]+center[2]))
        if True:
            self.points = L.translate(self.points, *translate)
            self.points = L.rotate(self.points, *rotate)
            self.points = L.scale(self.points, scale)
        else:    
            transMatrix = L.getTransformMatrix(scale=(1,1,1),
                                               rotate=(0,0,0),
                                               translate=translate)
            self.points = L.transform(points=self.points, M=transMatrix)

            ### Rotate all points
            if not isinstance(scale, (list, tuple)):
                scale = (scale,)*3
            transMatrix = L.getTransformMatrix(scale,
                                               rotate,
                                               translate=(0,0,0))
            self.points = L.transform(points=self.points, M=transMatrix)

        self.stateTouched = True
        return self
