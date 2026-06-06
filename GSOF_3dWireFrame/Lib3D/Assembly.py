from GSOF_3dWireFrame.MathLib import MathLib as ML
from GSOF_3dWireFrame.Lib3D import Lib3D as L
from GSOF_3dWireFrame.Lib3D.Pbject_base import Pbject_base

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
            for obj in objects:
                obj.reset(all)
        return self

    def findCenter(self, method) -> list:
        """Returns the center point of the assembly"""
        points = self.getobj()
        return super()._findCenter(self, method, points)

    def getobj(self) -> list:
        """Return a list of all objects"""
        objects = []
        for obj in self.objects:
            objects += obj.getobj()
        return objects

    def getLines(self):
        """Return lines of all objects"""
        lines = []
        ### Colect lines from all objects 
        for obj in self.objects:
            obj.update(self.stateOrigin)
            lines += obj.getLines()

        for line in self.connections:
            p0, p1 = line
            objects0 = self.objects[p0[0]].getobj()
            objects1 = self.objects[p1[0]].getobj()
            lines += [L.Line(objects0[p0[1]], objects1[p1[1]])]
        return lines

    def update(self, state):
        """Update the coordinates of all assembly and object"""
        super().update(state)
        for obj in objects:
            obj.update(self.state)
