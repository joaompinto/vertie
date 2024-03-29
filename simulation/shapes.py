#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@copyright:
  (C) Copyright 2012, Open Source Game Seed <devs at osgameseed dot org>

@license:
  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.
    
  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.
    
  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.    

@doc:
  This module provides classes for:
  
  Shapes:
    Circle, Triangle, Rectangle
"""
from math import sqrt, hypot, pi, sin, cos, atan2
from simulation.geometry import Point

class CircleShape:
    """ Circle shape centered at point P """
    def __init__(self, P, radius):
        self.x, self.y, self.radius = P.x, P.y, radius
        self.px, self.py = P.x, P.y
        self.ax = self.ay = 0
    
    def center(self):
        return Point(self.x, self.y)
        
    def hit(self, P):
        length = self.center().distance_to(P)
        return length < self.radius
                    
    def accelerate(self, delta):
        self.x += self.ax * delta * delta
        self.y += self.ay * delta * delta
        self.y += self.ay * delta * delta
        self.ax = self.ay = 0
        
    def inertia(self):
        x, y = self.x*2 - self.px, self.y*2 - self.py
        self.px, self.py = self.x, self.y;
        self.x, self.y = x, y
    
    def apply_friction(self, friction):
        x = (self.px - self.x)
        y = (self.py - self.y)
        length = hypot(x, y)
        if x <> 0:          
            self.ax += (x/length)*friction
            if abs(x) < 0.04: # stop on residual acceleration
                self.ax = 0
                self.px = self.x            
        if y <> 0:
            self.ay += (y/length)*friction
            if abs(y) < 0.04:  # stop on residual acceleration
                self.ay = 0
                self.py = self.y
                
    def line_contact(self, line):
        """ Returns the contact point with a Line """
        p = self.line_intersection(line)
        distance = p.distance_to(self.center())
        if distance > self.radius:
            return None
        else:
            return p
                        
    def line_intersection(self, line):
        """ 
        Returns the point of intersection with a line
        (point which is closer to the center of the circle)
        Math from http://paulbourke.net/geometry/pointline/ 
        """            
        A, B, C = line.A, line.B, self
        line_length = hypot(A.x - B.x, A.y - B.y)
        u = (((C.x - A.x ) * ( B.x - A.x )) +
            ((C.y - A.y) * (B.y - A.y))) / ( line_length ** 2 )
        
        in_segment = not (u < 0 or u > 1)
        if in_segment:
            point = Point(A.x + u * ( B.x - A.x),  A.y + u * ( B.y - A.y))
        else:
            point = self.center().nearest(A, B)
            
        return point               
