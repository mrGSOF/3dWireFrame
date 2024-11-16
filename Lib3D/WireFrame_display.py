class WireFrame():
    def __init__(self, screen, line, f=50, scale=1.0):
        self.screen = screen
        self.line = line
        self.f = f
        self.scale = scale
        self.centerX, self.centerY = (int(screen.get_width()/2), int(screen.get_height()/2))
        
    def draw(self, obj, color=None) -> None:
        ###  ###
        for line in obj.getLines():
            p0 = self.camera(line.p0)
            p1 = self.camera(line.p1)
            if (p0[2] > self.f) or (p1[2] > self.f): #Skip lines in the back of the viewer
                lcolor = color
                if lcolor == None:
                    lcolor = line.color
                self.drawLine( lcolor, p0, p1 ) #< Line from P0 to P1

    def camera(self, point) -> list:
        ### Perspective projection <https://en.wikipedia.org/wiki/3D_projection> ###
        x, y, z = point
        z = -z
        if (self.f != None):
            if (z > self.f):
                s = (self.f/z)*self.scale
            else:
                s = 100000
            x *= s
            y *= s
        return (x,y,z)

    def drawLine(self, color, p0, p1):
        ###  ###
        p0 = (self.centerX +p0[0], self.centerY -p0[1])
        p1 = (self.centerX +p1[0], self.centerY -p1[1])
        self.line( self.screen, color, p0, p1 ) #< Line from P0 to P1
