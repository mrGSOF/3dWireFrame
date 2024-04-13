import json
import numpy as np
import pygame
import threading

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
        self.points = []
        self.lines = []
        
        self.run = False
    
    def start(self):
        self.run = True
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False

            self.screen.fill(self.WHITE)
            for line in self.lines:
                start_point = self.points[line[0]][:2]
                end_point = self.points[line[1]][:2]
                pygame.draw.line(self.screen, self.RED, start_point, end_point, 2)

            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
    
    def loadObject(self, points, lines, bias=0):
        self.points = points+bias
        self.lines = lines

class WireFrame():
    def __init__(self):
        self.objectPoints = None
        self.objectLines = None
        self.win = Window(400, 300)
        threading.Thread(target=self.win.start).start()

    def loadObject(self, fileName=None, dict=None) -> None:
        if fileName == None and dict == None:
            raise Exception("Missing kwargs, fileName or dict")
        
        if fileName != None:
            with open(fileName, "r") as f:
                dict = json.load(f)

        self.objectPoints = np.array(dict["points_xyz"], dtype=np.float64)*dict["scale"]
        self.objectLines = np.array(dict["lines"], dtype=np.uint16)

    def rotateObject(self, angles) -> None:
        if type(self.objectLines) == type(None):
            raise Exception("Object not loaded")

        self.objectPoints = np.dot(self.objectPoints, rotationMatrix(*angles))
    
    def draw(self, biases=0) -> None:
        self.win.loadObject(self.objectPoints.astype(np.int32), self.objectLines, biases)

if __name__ == "__main__":
    import time
    wireFrame = WireFrame()
    # wireFrame.loadObject(fileName="objects/cube.json")
    wireFrame.loadObject(fileName="objects/pyramid.json")
    wireFrame.rotateObject((45, 45, 45))
    wireFrame.draw(biases=[200, 0, 0])
    rotation = 1
    while True:
        wireFrame.rotateObject((0, rotation, 0))
        wireFrame.draw(biases=[200, 0, 0])
        time.sleep(0.01)