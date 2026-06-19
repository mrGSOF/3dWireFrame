#!/usr/bin/python
"""
 * Cessna172_Class.py
 * Created on: 18 June 2026
 * Improved for: 18 june 2026
 * Author: Tzur Soffer
 * Copyright (C) 2026 Guy Soffer
"""

from math import pi
try:
   from GSOF_3dWireFrame.Lib3D.Object_WireFrame import Object_wireFrame as Object
   from GSOF_3dWireFrame.Lib3D.Assembly import Assembly
   from GSOF_3dWireFrame.utils import Colors
except:
   raise "GSOF_Wireframe3D module isn't installed"

class View(Assembly):
    """Constructs the gauges screen"""
    def __init__(self, folder='./', rps=40):
        self.time = 0.0
        self.rps = rps
        axis  = Object(
           filename="%s/objects/axis.json"%folder, color=Colors.GREEN)\
           .scale(50.0)\
           .translate(0, 0, 150)\
           .setOrigin()

        self.plane = Object(
            filename="%s/objects/Cessna 172/body.stl"%folder, color=Colors.BLUE, name="Cessna172")\
            .setCenter(scale=1.0, method="arithCenter")
        
        self.propeller = Object(
           filename="%s/objects/Cessna 172/propeller.stl"%folder, color=Colors.RED, name="Propeller")\
            .setCenter(scale=1.0, method="arithCenter")\
            .translate(0, -20, 225)\
            .setOrigin()
        self.propeller.color = Colors.RED

        self.gears = Object(
           filename="%s/objects/Cessna 172/wheels.stl"%folder, color=Colors.BLACK, name="GEARS")\
            .setCenter(scale=1.0, method="arithCenter")\
            .translate(0, -80, 80)\
            .setOrigin()

        super().__init__(objects=(axis, self.plane, self.propeller, self.gears))

    def tick(self, fps=60):
        """Update all elements"""
        self.time += 1/fps
        self.propeller.rotate(x=0, y=0, z=self.time*self.rps*2*pi)

    def setGearsDown(self, downCmd) -> None:
        if downCmd == False:
           self.gears.scale(0.0)
        else:
           self.gears.scale(1.0)

