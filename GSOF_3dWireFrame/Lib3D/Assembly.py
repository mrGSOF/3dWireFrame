from GSOF_3dWireFrame.MathLib import MathLib as ML
from GSOF_3dWireFrame.Lib3D import Lib3D as L
from GSOF_3dWireFrame.Lib3D.Object_base import Object_base

class Assembly(Object_base):
    """A new frame of reference with collection of other assemblies or objects"""
    def __init__(self,
                 objects=[],    #< Objects in assembly  
                 connections=[] #< Connections between objects (for flexable objects)
                 ):
        self.objects = objects
        self.connections = connections
        super().__init__()

    def reset(self, all=True):
        """Reset current state and all objects (optional)"""
        super().reset()
        if all:
            for obj in self.objects:
                obj.reset(all)
        return self

    def findCenter(self, method) -> list:
        """Return the center point of the assembly"""
        points = self.getLines()
        return super()._findCenter(method, points)

    def getobjects(self) -> list:
        """Return a list of all objects"""
        objects = []
        for obj in self.objects:
            objects += obj.getobjects()
        return objects

    def getLines(self):
        """Return lines of all objects. Will update transformations if needed"""
        lines = []
        if not self.isUpdated():
            self.update()

        ### Lines from all objects 
        for obj in self.objects:
            lines += obj.getLines()

        ### Lines between objects 
        for between in self.connections:
            [obj0, p0], [obj1, p1] = between
            fromPnt = self.objects[obj0][p0]
            toPnt   = self.objects[obj1][p1]
            lines += [L.Line(fromPnt, toPnt)]
        return lines

    def update(self):
        """Update the coordinates of all assembly and object"""
        for obj in self.objects:
            if not self.isUpdated():
                obj.transform(transMatrix=self.state, reverse=True)
            obj.update()
        self.stateTouched = True
