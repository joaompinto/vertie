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
  
  Basic geometric elements:
    Point, Vector, Line
"""
from math import sqrt, hypot, pi, sin, cos, atan2

class Point:

    def __init__(self, x, y):
        self.x, self.y = x, y
            
    def distance_to(self, other):
        return hypot(self.x-other.x, self.y-other.y)
        
    def pos(self):
        """ return position as tuple, useful for some gfx libs """
        return (int(self.x), int(self.y))
        
    def nearest(self, *args):
        """ """
        nearest_point = args[0]
        min_length = hypot(args[0].x - self.x, args[0].y - self.y)
        for arg in args[1:]:
            length = hypot(arg.x - self.x, arg.y - self.y)
            if length < min_length:
                nearest_point = arg
        return nearest_point

class Vector(Point):
    """ For simplicy we assume vectors have origin (0,0) to (PointX, PointY)"""
    pass

class Line:
    """ Line between point A and B """
    def __init__(self, A, B):
        self.A, self.B = A, B
            
    def __repr__(self):
        return "<Line> "+str(self.A.pos())+","+str(self.B.pos())
    
    

