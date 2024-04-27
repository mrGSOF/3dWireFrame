from MathLib import MathLib as ML
from Lib3D import Object_base as O
from Lib3D import Lib3D as L
import json
try:
    from stl import mesh
except:
    print("could not find numpy-stl. DO NOT USE STL FILES!!\nTo install, run ```pip install numpy-stl```")

class Object_wireFrame(O.Object_base):
    def __init__(self, obj=None, filename=None, color=(0,0,0)):
        if filename != None:
            ext = filename.split(".")[-1]
            if ext == "json":
                obj = self._loadJson(filename)
            elif ext == "stl":
                obj = self._loadStl(filename)

        self.color  = color
        self.initShape   = obj["points_xyz"]
        self.connections = obj["connections"]
        self.reset().scale(obj["scale"], initShape=True)

    def _updateShape(self, initShape=False):
        if initShape == True:
            self.initShape = self.shape

    def _loadJson(self, filename):
        obj = None
        with open(filename) as f:
            obj = json.load(f)
        return obj
    
    def _loadStl(self, filename):
        objMesh = mesh.Mesh.from_file(filename) #< Load the STL file

        # Initialize lists for points and lines
        points = []
        lines = []

        for i in range(len(objMesh.vectors)):
            vertexes = objMesh.vectors[i].tolist() #< triangle
            # Add the vertices (points) to the list
            for vertex in vertexes:
                points.append(vertex)
            
            # Add the edges (lines) to the list
            lines.append((i*3, i*3+1))
            lines.append((i*3+1, i*3+2))
            lines.append((i*3+2, i*3+0))

        # Now you have a list of points and lines
        obj = {"scale": 100.0,
                "points_xyz": points,
                "connections": lines}

        return(obj)

    def reset(self):
        self.shape = self.initShape
        return self

    def scale(self, scale, initShape=False, elements=[]):
        self.shape = L._scale(self.shape, scale)
        self._updateShape( initShape )
        return self
        
    def rotate(self, x=0, y=0, z=0, dcm=None, initShape=False, elements=[]):
        self.shape = L._rotate( self.shape, x,y,z, dcm )
        self._updateShape( initShape )
        return self

    def translate(self, x=0, y=0, z=0, V=None, initShape=False, elements=[]):
        self.shape = L._translate( self.shape, x,y,z, V )
        self._updateShape( initShape )
        return self

    def getShape(self) -> list:
        return self.shape

    def getLines(self) -> list:
        return L._calcLines(self.shape, self.connections)
