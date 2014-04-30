#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    Copyright 2014, Open Source Game Seed <devs at osgameseed dot org>

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
       limitations under the License.

"""

from pymunk import Vec2d
from random import randint
from pygame.color import *
import pymunk
import pygame


class PlaySpace:

    def flipy(self, p):
        """Small hack to convert pymunk to pygame coordinates"""
        return int(p.x), int(-p.y+self.h)

    def __init__(self, screen):
        self.screen = screen
        self.w, self.h = screen.get_width(), screen.get_height()

        self.pushing_delta = None

        self.space = pymunk.Space()
        self.space.gravity = (0.0, -900.0)
        self.space. sleep_time_threshold = 2

        self.walls = []
        self.polys = []
        self.balls = []

        # Created border walls
        self.create_wall_segments(
            map(Vec2d, [(0, 0), (0, self.h)
                        , (self.w-1, self.h)
                        , (self.w-1, 1)
                        , (0, 1)
            ]))

        self._create_random_walls()

        # Create a box in a random position at the top of the screen
        x = randint(20, self.w-20)
        y = self.h-20
        p = Vec2d(x, y)
        self.goal_box = self.create_box(p, 20, 20, mass=2)
        self.polys.append(self.goal_box)

        # Place ball
        bp = Vec2d(20, 100)
        ball = self.create_ball(bp)
        self.balls.append(ball)

        # Set collision handler
        self.space.add_collision_handler(0, 0, None, None, self._on_collision, None)

    def _on_collision(self, space, arb):
        if self.balls[0] in arb.shapes:
            if self.goal_box in arb.shapes:
                print "Hitting goal  box"
            if abs(self.balls[0].body.angular_velocity) > 0:
                self.balls[0].body.angular_velocity *= 0.99  # Apply rolling friction

    def _create_random_walls(self):
        for i in range(30):
            x = randint(0, self.w)
            y = randint(0, self.h-50)
            dx = randint(-200, 200)
            if abs(dx) < 10:
                dx = dx*10
            if randint(1, 2) == 1:
                dy = randint(-100, 100)
            else:
                dy = 0
            self.create_wall_segments([Vec2d(x, y), Vec2d(x+dx, y+dy)])

    def create_ball(self, point, mass=1.0, radius=15.0):

        moment = pymunk.moment_for_circle(mass, radius, 0.0, Vec2d(0, 0))
        ball_body = pymunk.Body(mass, moment)
        ball_body.position = Vec2d(point)

        ball_shape = pymunk.Circle(ball_body, radius, Vec2d(0, 0))
        ball_shape.friction = 1
        ball_shape.elasticity = 0.5
        #ball_shape.collision_type = COLLTYPE_DEFAULT
        self.space.add(ball_body, ball_shape)
        return ball_shape

    def create_box(self, pos, hsize=10, vsize=10, mass=5.0):
        box_points = map(Vec2d, [(-hsize, -vsize), (-hsize, vsize), (hsize, vsize), (hsize, -vsize)])
        return self.create_poly(box_points, mass=mass, pos=pos)

    def create_poly(self, points, mass=5.0, pos=(0, 0)):
        moment = pymunk.moment_for_poly(mass, points, Vec2d(0, 0))
        body = pymunk.Body(mass, moment)
        body.position = Vec2d(pos)
        shape = pymunk.Poly(body, points, Vec2d(0, 0))
        shape.friction = 1
        #shape.collision_type = COLLTYPE_DEFAULT
        self.space.add(body, shape)
        return shape

    def create_wall_segments(self, points):
        """Create a number of wall segments connecting the points"""
        if len(points) < 2:
            return []
        points = map(Vec2d, points)
        for i in range(len(points) - 1):
            v1 = Vec2d(points[i].x, points[i].y)
            v2 = Vec2d(points[i + 1].x, points[i + 1].y)
            wall_body = pymunk.Body()
            wall_shape = pymunk.Segment(wall_body, v1, v2, 3)
            wall_shape.friction = 1.0
            wall_shape.elasticity = 0.95
            #wall_shape.collision_type = COLLTYPE_DEFAULT
            self.space.add(wall_shape)
            self.walls.append(wall_shape)

    def simulate(self):
            x = 5
            dt = 1.0 / 60.0 / x
            for x in range(x):
                self.space.step(dt)

    def draw_ball(self, ball):
        body = ball.body
        v = body.position + ball.offset.cpvrotate(body.rotation_vector)
        p = self.flipy(v)
        r = ball.radius
        pygame.draw.circle(self.screen, THECOLORS["darkblue"], p, int(r), 0)
        pygame.draw.circle(self.screen, THECOLORS["blue"], p, int(r), 2)

    def draw_wall(self, wall):
        body = wall.body
        pv1 = self.flipy(body.position + wall.a.cpvrotate(body.rotation_vector))
        pv2 = self.flipy(body.position + wall.b.cpvrotate(body.rotation_vector))
        pygame.draw.lines(self.screen, THECOLORS["darkred"], False, [pv1, pv2], max(int(wall.radius*2), 1))

    def draw_poly(self, poly):
        body = poly.body
        ps = poly.get_vertices()
        ps.append(ps[0])
        ps = map(self.flipy, ps)
        color = THECOLORS["green"]
        pygame.draw.lines(self.screen, color, False, ps)

    def draw(self):


        ### Draw balls
        for ball in self.balls:
            self.draw_ball(ball)

        ### Draw walls
        for wall in self.walls:
            self.draw_wall(wall)

        ### Draw polys
        for poly in self.polys:
            self.draw_poly(poly)