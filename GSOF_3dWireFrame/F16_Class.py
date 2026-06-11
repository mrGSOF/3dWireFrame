#!/usr/bin/python
"""
 * F16_Class.py
 * Created on: 6 Jan 2025
 * Improved for: 25 May 2026
 * Author: Guy Soffer
 * Copyright (C) 2026 Guy Soffer
"""

from math import pi
try:
   from GSOF_3dWireFrame.Lib3D.Object_WireFrame import Object_wireFrame as Object
   from GSOF_3dWireFrame.Lib3D.Object_base import Object_base
   from GSOF_3dWireFrame.Lib3D.Assembly import Assembly
   from GSOF_3dWireFrame.Lib3D import Objects
   _3D_active = True
except:
   _3D_active = False
   print("GSOF_Wireframe3D module isn't installed")

degToRad = pi/180
#YELLOW = (255,255,140)
YELLOW = (125,125,0)
BLACK  = (0,0,0)
RED    = (255,0,0)
GREEN  = (0,170,0)
BLUE   = (0,0,255)
GRAY   = (50,50,50)
class F16_View(Assembly):
    """Constructs the gauges screen"""
    def __init__(self, folder='./'):
        self.time = 0.0
        axis  = Object(
           filename="%s/objects/axis.json"%folder, color=GREEN)\
           .scale(50.0)\
           .translate(0, 0, 150)\
           .setOrigin()

        self.plane = Object(
            filename="%s/objects/f16.stl"%folder, color=BLUE, name="F16")\
            .setCenter(scale=1.0, method="arithCenter")
        
        self.plume = objects=Object(
           filename="%s/objects/Plume.json"%folder, color=RED)\
           .setCenter(scale=30, rotate=(180*degToRad, 0, 0))
        plume = Assembly(objects=(self.plume,))   
        plume.translate(0, 0, -90).setOrigin()
        
        self.nw = Object(
           filename="%s/objects/LandingGear.json"%folder, color=BLACK, name="NW")
        self.nwow = Object(
           filename="%s/objects/Spark.json"%folder, color=YELLOW, name="NWOW")
        nw = Assembly(objects=(self.nw, self.nwow), name="NW-Assy")\
           .translate(0, -2, 0).scale(8).translate(0, -30, 80).setOrigin()           

        self.rw = Object(
           filename="%s/objects/LandingGear.json"%folder, color=BLACK, name="RW")
        self.rwow = Object(
           filename="%s/objects/Spark.json"%folder, color=YELLOW)
        rw = Assembly(objects=(self.rw, self.rwow), name="RW-Assy")\
           .translate(0, -2, 0).rotate(x=0, y=0, z=-degToRad*15)\
           .scale(8).translate(-18, -30, 0).setOrigin()           

        self.lw = Object(
           filename="%s/objects/LandingGear.json"%folder, color=BLACK, name="LW")
        self.lwow = Object(
           filename="%s/objects/Spark.json"%folder, color=YELLOW)
        lw = Assembly(objects=(self.lw, self.lwow), name="LW-Assy")\
           .translate(0, -2, 0).rotate(x=0, y=0, z=degToRad*15)\
           .scale(8).translate(18, -30, 0).setOrigin()           

        self.gears = Assembly(objects=(nw,
                                       rw,
                                       lw
                                       ))
        super().__init__(objects=(axis, self.plane, plume, self.gears))

    def setControls(self, time, fcs=None, eng=None, ins=None, wow=None):
        """Update all elements"""
        self.time += 0.1
        if eng != None:
            self.setExahustPlume(eng.thrust_lbf)

        if wow != None:
           leftWow, rightWow, noseWow = wow.left, wow.right, wow.nose
           self.setWOW(leftWow, rightWow, noseWow)

        if fcs != None:
            lElev_deg  = fcs.lElevator_d
            rElev_deg  = fcs.rElevator_d
            rudder_deg = fcs.rudder_d
            sb_deg     = fcs.speedbrake_d
            self.setFCS(lElev_deg, rElev_deg, rudder_deg, sb_deg)
            self.setGearsDown(fcs.gearDown_b)

        if ins != None:
            heading =  ins.heading_d*degToRad
            pitch   = -ins.pitch_d*degToRad
            roll    =  ins.roll_d*degToRad
            self.setAttitude(heading, pitch, roll)

            mToFt = 3.28
            self.setAltitude(mToFt*ins.height.value)

    def setAltitude(self, alt_ft) -> None:
        self.translate(V=(0, alt_ft, 0))
       
    def setAttitude(self, heading, pitch, roll) -> None:
        self.rotate( y=-heading-0*degToRad, x=-pitch, z=-roll )

    def setExahustPlume(self, thrust_lbf) -> None:
        thrustMAX = 6360
        plume = thrust_lbf/thrustMAX
        if plume > 1:
            plume = 1
        elif plume < 0:
            plume = 0
        plumeColor = (255, 255*(1-plume), 255*(1-plume))
        self.plume.rotate(x=0, y=0, z=self.time*plume)
        self.plume.scale(plume).color = plumeColor
       
    def setFCS(self, lElev_deg, rElev_deg, rudder_deg, sb_deg) -> None:
        return
      
    def setGearsDown(self, downCmd) -> None:
        if downCmd == False:
           self.gears.scale(0.0)
        else:
           self.gears.scale(1.0)

    def setWOW(self, leftWow, rightWow, noseWow) -> None:
        time = int(self.time*10)
        blink = bool(time&0b010)
        self.nwow.rotate(x=0, y=0, z=4*self.time)\
                 .scale(int(noseWow and blink))
                 #.translate(0, -48, 120)\
        self.lwow.rotate(x=0, y=0, z=4*self.time)\
                 .scale(int(leftWow and blink))
                 #.translate(-15, -48, 15)\
        self.rwow.rotate(x=0, y=0, z=4*self.time)\
                 .scale(int(rightWow and blink))
                 #.translate(15, -48, 15)\

