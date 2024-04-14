import json
import numpy as np
import pygame

def rotationMatrix(angle_x_deg, angle_y_deg, angle_z_deg):
    angle_x_rad = np.radians(angle_x_deg)
    angle_y_rad = np.radians(angle_y_deg)
    angle_z_rad = np.radians(angle_z_deg)

    cos_x = np.cos(angle_x_rad)
    sin_x = np.sin(angle_x_rad)
    cos_y = np.cos(angle_y_rad)
    sin_y = np.sin(angle_y_rad)
    cos_z = np.cos(angle_z_rad)
    sin_z = np.sin(angle_z_rad)

    Rx = np.array([
        [1, 0, 0],
        [0, cos_x, -sin_x],
        [0, sin_x, cos_x]
    ])

    Ry = np.array([
        [cos_y, 0, sin_y],
        [0, 1, 0],
        [-sin_y, 0, cos_y]
    ])

    Rz = np.array([
        [cos_z, -sin_z, 0],
        [sin_z, cos_z, 0],
        [0, 0, 1]
    ])

    # Combine the rotation matrices
    combined_rotation_matrix = np.dot(Rz, np.dot(Ry, Rx))

    return combined_rotation_matrix

class Window():
    def __init__(self, screenWidth=400, screenHeight=300):
        pygame.init()
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.screen = pygame.display.set_mode((screenWidth, screenHeight))
        pygame.display.set_caption("Shape Drawer")
        self.clock = pygame.time.Clock()
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.lines = []
    
    def tick(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        self.screen.fill(self.WHITE)
        for line in self.lines:
            start_point = line[0]
            end_point = line[1]
            pygame.draw.line(self.screen, self.RED, start_point, end_point, 2)

        pygame.display.flip()
        self.clock.tick(60)
    
    def loadObject(self, lines):
        self.lines.extend(lines)
    
    def clear(self):
        self.lines = []

class Object():
    def __init__(self, parent):
        self.objectPoints = None
        self.objectLines = None
        self.win = parent
    
    def _findCenter(self):
        return(np.mean(self.objectPoints, axis=0))

    def loadObject(self, fileName=None, dict=None) -> object:
        if fileName == None and dict == None:
            raise Exception("Missing kwargs, fileName or dict")
        
        if fileName != None:
            with open(fileName, "r") as f:
                dict = json.load(f)

        self.objectPoints = np.array(dict["points_xyz"], dtype=np.float64)*dict["scale"]
        self.objectLines = np.array(dict["lines"], dtype=np.uint16)
        
        return(self)

    def rotateObject(self, angles, center=(0,0,0)) -> object:
        if type(self.objectLines) == type(None):
            raise Exception("Object not loaded")
        
        if type(center) == tuple:
            offset = center
        
        elif type(center) == str:
            if center == "object":
                offset = self._findCenter()
        
        objectCenter = self.objectPoints-offset
        
        self.objectPoints = np.dot(objectCenter, rotationMatrix(*angles))+offset
        
        return(self)

    def translate(self, biases) -> object:
        if type(self.objectLines) == type(None):
            raise Exception("Object not loaded")

        self.objectPoints = self.objectPoints + biases
        
        return(self)
    
    def draw(self) -> object:
        points = self.objectPoints.astype(np.int32)[:,:2]
        lines = points[self.objectLines]
        self.win.loadObject(lines)
        return(self)
    
    def clear(self) -> object:
        self.win.clear()
        return(self)

class Container(Object):
    def __init__(self):
        self.objects = []

    def addObjects(self, objects) -> object:
        self.objects.extend(objects)
        return(self)

    def apply(self, method_name, *args, **kwargs):
        for obj in self.objects:
            method = getattr(obj, method_name)
            method(*args, **kwargs)
        return self

if __name__ == "__main__":
    import time
    win = Window(400, 300)
    box = Container()
    cube = Object(win)
    cube.loadObject(fileName="objects/cube.json").translate((0, 50, 0))
    pyramid = Object(win)
    pyramid.loadObject(fileName="objects/pyramid.json").translate((0, 150, 0))
    box.addObjects([cube, pyramid])
    box.apply("translate", (200, 0, 0))
    rotation = 1
    while True:
        # pyramid.rotateObject((0, rotation, 0), center="object")
        box.apply("rotateObject", (0, 1, 0), center="object")

        box.apply("clear")
        box.apply("draw")
        time.sleep(0.01)
        win.tick()