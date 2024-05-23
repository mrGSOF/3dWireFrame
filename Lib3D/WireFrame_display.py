class WireFrame():
    def __init__(self, screen, line, f=200):
        self.screen = screen
        self.line = line
        self.f = f
        
    def draw(self, obj, color=None) -> None:
        for line in obj.getLines():
            p0 = self.camera(line.p0)
            p1 = self.camera(line.p1)
            lcolor = color
            if lcolor == None:
                lcolor = line.color
            self.drawLine( lcolor, p0, p1 ) #< Line from P0 to P1

    def camera(self, point) -> list:
        ### Perspective transformation ###
        x, y, z = point
        if self.f != None:
            s = self.f/z
            x *= s
            y *= s
        return (x,y)

    def drawLine(self, color, p0, p1):
        self.line( self.screen, color, p0, p1 ) #< Line from P0 to P1
