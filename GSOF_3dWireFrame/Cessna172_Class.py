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
            filename="%s/objects/Cessna 172/body.stl"%folder, color=Colors.BLUE)\
            .setCenter(scale=1.0, method="arithCenter")
        
        self.propeller = Object(
           filename="%s/objects/Cessna 172/propeller.stl"%folder, color=Colors.RED)\
            .setCenter(scale=1.0, method="arithCenter")\
            .translate(0, -20, 210)\
            .setOrigin()
        self.propeller.color = Colors.RED

        self.leftGear = Object(
           filename="%s/objects/Cessna 172/LeftWheel.stl"%folder, color=Colors.BLACK)\
              .setCenter(scale=1.0, method="arithCenter")\
              .translate(70, -80, 0)\
              .setOrigin()
        self.rightGear = Object(
           filename="%s/objects/Cessna 172/RightWheel.stl"%folder, color=Colors.BLACK)\
              .setCenter(scale=1.0, method="arithCenter")\
              .translate(-70, -80, 0)\
              .setOrigin()
        self.frontGear = Object(
           filename="%s/objects/Cessna 172/FrontWheel.stl"%folder, color=Colors.BLACK)\
              .setCenter(scale=1.0, method="arithCenter")\
              .translate(0, -80, 120)\
              .setOrigin()
        self.gears = Assembly((self.leftGear,
                           self.rightGear,
                           self.frontGear
                          ))

        self.rightFlap = Object(
           filename="%s/objects/Cessna 172/RightFlap.stl"%folder, color=Colors.RED)\
            .setCenter(scale=1.0, method="arithCenter")\
            .translate(-95, 25, 0)\
            .setOrigin()
        self.leftFlap = Object(
           filename="%s/objects/Cessna 172/LeftFlap.stl"%folder, color=Colors.RED)\
            .setCenter(scale=1.0, method="arithCenter")\
            .translate(95, 25, 0)\
            .setOrigin()
        flaps = Assembly((self.rightFlap, self.leftFlap))

        self.rightAileron = Object(
           filename="%s/objects/Cessna 172/RightAileron.stl"%folder, color=Colors.RED)\
            .setCenter(scale=1.0, method="arithCenter")\
            .translate(-275, 25, 10)\
            .setOrigin()
        self.leftAileron = Object(
           filename="%s/objects/Cessna 172/LeftAileron.stl"%folder, color=Colors.RED)\
            .setCenter(scale=1.0, method="arithCenter")\
            .translate(275, 25, 10)\
            .setOrigin()
        ailerons = Assembly((self.rightAileron, self.leftAileron))

        self.rightElevator = Object(
           filename="%s/objects/Cessna 172/RightElevator.stl"%folder, color=Colors.RED)\
            .setCenter(scale=1.0, method="arithCenter")\
            .translate(-60, -20, -270)\
            .setOrigin()
        self.leftElevator = Object(
           filename="%s/objects/Cessna 172/LeftElevator.stl"%folder, color=Colors.RED)\
            .setCenter(scale=1.0, method="arithCenter")\
            .translate(60, -20, -270)\
            .setOrigin()
        elevators = Assembly((self.rightElevator, self.leftElevator))

        self.rudder = Object(
           filename="%s/objects/Cessna 172/Rudder.stl"%folder, color=Colors.RED)\
            .setCenter(scale=1.0, method="arithCenter")\
            .transform(rotate=(-0.3,0,0), translate=(0, 25, -290))\
            .setOrigin()

        super().__init__(objects=(axis, self.plane, self.propeller, self.gears, flaps, ailerons, elevators, self.rudder))

    def tick(self, fps=60):
        """Update all elements"""
        self.time += 1/fps
        self.propeller.rotate(x=0, y=0, z=self.time*self.rps*2*pi)
    
    def setRightFlapAngle(self, angle):
        self.rightFlap.rotate(angle,0,0)
    def setLeftFlapAngle(self, angle):
        self.leftFlap.rotate(angle,0,0)

    def setRightAileronAngle(self, angle):
        self.rightAileron.rotate(angle,0,0)
    def setLeftAileronAngle(self, angle):
        self.leftAileron.rotate(angle,0,0)

    def setRightElevatorAngle(self, angle):
        self.rightElevator.rotate(angle,0,0)
    def setLeftElevatorAngle(self, angle):
        self.leftElevator.rotate(angle,0,0)

    def setRudderAngle(self, angle):
        self.rudder.rotate(0,angle,0)

    def setGears(self, down=True):
        if down:
            self.setGearsDown()
        else:
            self.setGearsUp()
    def setGearsDown(self) -> None:
        self.gears.scale(0.0)
    def setGearsUp(self) -> None:
        self.gears.scale(1.0)

