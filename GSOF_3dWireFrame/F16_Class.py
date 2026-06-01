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
   from GSOF_3dWireFrame.Lib3D import Object_WireFrame as OWF
   from GSOF_3dWireFrame.Lib3D import Object_base as OB
   from GSOF_3dWireFrame.Lib3D import Objects
   _3D_active = True
except:
   _3D_active = False
   print("GSOF_Wireframe3D module isn't installed")

degToRad = pi/180
class F16_View(OB.Object_container):
    """Constructs the gauges screen"""
    def __init__(self, folder='./'):
        self.time = 0.0
        axis  = OWF.Object_wireFrame(
           filename="%s/objects/axis.json"%folder, color=(10,10,10 ))\
           .translate(V=(0, 0, 0))\
           .scale(1.5, initShape=True)

        self.plane = OWF.Object_wireFrame(
            filename="%s/objects/f16.stl"%folder, color=( 0, 0,255))\
            .rotate(x=0, y=0, z=0)
        self.plane.setOrigin(
            origin=self.plane.getOrigin(origin="arithCenter") )\
            .scale(0.015)\
            .rotate(x=0, y=0, z=0)\
            .translate(V=(0, 0, 0), initShape=True)
        
        plume = OWF.Object_wireFrame(
           filename="%s/objects/Plume.json"%folder, color=( 255, 0,0))\
           .scale(0.5)\
           .rotate(x=0, y=180*degToRad, z=0)\
           .translate(V=(0, 0, -130), initShape=True)
                       
        self.plume = OB.Object_container(objList=(plume,))
        
        nw = OWF.Object_wireFrame(
           filename="%s/objects/LandingGear.json"%folder, color=( 0,0,0))\
           .scale(0.1)\
           .translate(V=(0, -45, 120), initShape=True)
        self.nwow = OWF.Object_wireFrame(
           filename="%s/objects/Spark.json"%folder, color=( 255,0,255))\
           .scale(0.1, initShape=True)#\
           #.translate(V=(0, -48, 120), initShape=True) #< Translation is done in manipulation function
        rw = OWF.Object_wireFrame(
           filename="%s/objects/LandingGear.json"%folder, color=( 0,0,0))\
           .scale(0.1)\
           .rotate(x=0, y=0, z=-degToRad*10)\
           .translate(V=(-15, -45, 15), initShape=True)
        self.rwow = OWF.Object_wireFrame(
           filename="%s/objects/Spark.json"%folder, color=( 255,255,0))\
           .scale(0.1, initShape=True)#\
           #.translate(V=(-15, -48, 15), initShape=True) #< Translation is done in manipulation function
        lw = OWF.Object_wireFrame(
           filename="%s/objects/LandingGear.json"%folder, color=( 0,0,0))\
           .scale(0.1)\
           .rotate(x=0, y=0, z=degToRad*10)\
           .translate(V=(15, -45, 15), initShape=True)
        self.lwow = OWF.Object_wireFrame(
           filename="%s/objects/Spark.json"%folder, color=( 255,255,0))\
           .scale(0.1, initShape=True)#\
           #.translate(V=(15, -48, 15), initShape=True) #< Translation is done in manipulation function

        self.gears = OB.Object_container(objList=(nw, self.nwow,
                                                  rw, self.rwow,
                                                  lw, self.lwow
                                                  ))
        
        super().__init__(objList=(self.plane, self.plume, self.gears))

    def update(self, time, fcs=None, eng=None, ins=None, wow=None):
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
        self.nwow.rotate(x=0, y=0, z=4*self.time).translate(V=(0, -48, 120)).scale(int(noseWow and blink))
        self.lwow.rotate(x=0, y=0, z=4*self.time).translate(V=(-15, -48, 15)).scale(int(leftWow and blink))
        self.rwow.rotate(x=0, y=0, z=4*self.time).translate(V=(15, -48, 15)).scale(int(rightWow and blink))

