from GSOF_3dWireFrame.MathLib import MathLib as ML
from GSOF_3dWireFrame.Lib3D import Lib3D as L
from GSOF_3dWireFrame.Lib3D.Object_base import *

class Object_wireFrame(Object_base):
    def __init__(self, obj=None, filename=None, color=None):
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
