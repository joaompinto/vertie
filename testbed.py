import os
from os.path import exists
from copy import copy
from math import copysign
from interface.graphical import GraphichalEngine
from simulation.geometry import *
from simulation.shapes import *
from simulation.world import *

import pygame
from pygame.color import THECOLORS

try:
    import android  
    ANDROID = True
except ImportError:
    ANDROID = False
    
# Graphical Engine
class JumperBall(GraphichalEngine): 
    lines_xml = 'lines.xml'
    velocity_start = velocity_end = None
    def init(self):
        if not ANDROID:
            self.world.gravity = Vector(0, 0.2)
        self.drawing_line = Line(None, None)
        self.load_lines_from_xml()
        
    def load_lines_from_xml(self):
        try:
            with open(self.lines_xml) as xml_file:
                lines = xml_file.read().splitlines()
        except IOError:
            return
        for line in lines:
            x1, y1, x2, y2 = line.split()
            l = Line(Point(int(x1), int(y1)), Point(int(x2), int(y2)))
            self.world.lines.append(l)
        
    def update(self):
        self.world.step()
            
    def draw(self):
        self.display.fill(THECOLORS['black'])
        for shape in self.world.circle_shapes:
            pygame.draw.circle(self.display, THECOLORS['blue'], shape.center().pos(), shape.radius)
        for line in self.world.lines:       
            pygame.draw.line(self.display, THECOLORS['yellow'], line.A.pos(), line.B.pos())
        if self.drawing_line.A and self.drawing_line.B:
            line = self.drawing_line
            pygame.draw.line(self.display, THECOLORS['green'], line.A.pos(), line.B.pos())
        if self.velocity_start and self.velocity_end:
            pygame.draw.circle(self.display, THECOLORS['blue'], self.velocity_start.pos(), 20)
            pygame.draw.circle(self.display, THECOLORS['red'], self.velocity_end.pos(), 10)
            pygame.draw.line(self.display, THECOLORS['green'], 
                            self.velocity_end.pos(), self.velocity_start.pos())

    def on_MOUSEBUTTONDOWN(self, mouse):
        to_delete = [shape for shape in self.world.circle_shapes if shape.hit(mouse.point)]
        if not to_delete and mouse.pressed[-1]:
            self.velocity_start = copy(mouse.point)
            self.velocity_end = copy(mouse.point)
        elif mouse.pressed[0]:
            self.drawing_line.A = copy(mouse.point)
            self.drawing_line.B = None
        for shape in to_delete:
            self.world.remove(shape)
                
    def on_MOUSEMOTION(self, mouse):
        if mouse.pressed[0] and self.drawing_line.A:
            self.drawing_line.B = copy(mouse.point)
        if self.velocity_start:
            self.velocity_end = copy(mouse.point)
            delta_x = (self.velocity_end.x - self.velocity_start.x)
            delta_y = (self.velocity_end.y - self.velocity_start.y)
            if abs(delta_x) > 40: delta_x = copysign(40, delta_x)
            if abs(delta_y) > 40: delta_y = copysign(40, delta_y)
            self.velocity_end.x = self.velocity_start.x + delta_x
            self.velocity_end.y = self.velocity_start.y + delta_y 


    def on_MOUSEBUTTONUP(self, mouse):
        if self.velocity_start and self.velocity_end:
            b = CircleShape(mouse.point, 20)
            delta_x = (self.velocity_end.x - self.velocity_start.x)/5
            delta_y = (self.velocity_end.y - self.velocity_start.y)/5
            b.px = mouse.point.x + delta_x;
            b.py = mouse.point.y + delta_y;
            self.world.add(b)
        elif self.drawing_line.A and self.drawing_line.B:
            self.world.lines.append(self.drawing_line)
            self.drawing_line = Line(None, None)
        elif not self.drawing_line.B and mouse.last_pressed[0]:
            to_delete = []
            for line in self.world.lines:               
                MouseCircle = CircleShape(mouse.point, 3)
                contact_point = MouseCircle.line_contact(line)
                if contact_point:
                    to_delete.append(line)
            for line in to_delete:
                self.world.lines.remove(line)   
        self.velocity_start = self.velocity_end = None

    def on_KEY_s(self):
        new_fn = self.lines_xml+'.new'
        with open(new_fn, 'a') as lines_file:
            for line in self.world.lines:
                lines_file.write("%s %s %s %s\n" \
                    % (line.A.x, line.A.y, line.B.x, line.B.y))
        if exists(self.lines_xml):
            os.unlink(self.lines_xml)
        os.rename(new_fn, self.lines_xml)

    def on_KEY_c(self):
        self.world.lines = []
        self.world.bodies = []

    def on_KEY_space(self):
        for body in self.world.bodies:
            body.py = body.y + 5

g = JumperBall()
g.init()
g.startLoop()
