from GSOF_3dWireFrame.MathLib import MathLib as ML
from GSOF_3dWireFrame.Lib3D import Lib3D as L
from GSOF_3dWireFrame.Lib3D.Pbject_base import Object_base

class Assembly(Object_base):
    """A new frame of reference with collection of other assemblies or objects"""
    def __init__(self,
                 objects=[],    #< Objects in assembly  
                 connections=[] #< Connections between objects (for flexable objects)
                 ):
        super().__init__()
        self.objects = objects
        self.connections = connections

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

    def _getobj(self) -> list:
        """Return a list of all objects"""
        objects = []
        for obj in self.objects:
            objects += obj.getobj()
        return objects

    def getLines(self):
        """Return lines of all objects. Will automatically start to update transformations if needed"""
        lines = []
        if not self.isUpdated():
            self.update()

        ### Collect lines from all objects 
        for obj in self.objects:
            lines += obj.getLines()

        for line in self.connections:
            p0, p1 = line
            objects0 = self.objects[p0[0]].getobj()
            objects1 = self.objects[p1[0]].getobj()
            lines += [L.Line(objects0[p0[1]], objects1[p1[1]])]
        return lines

    def update(self):
        """Update the coordinates of all assembly and object"""
        for obj in self.objects:
            if not self.isUpdated():
                obj.transform(transMatrix=self.state)
            obj.update()
        self.updated = True
