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

import os
import pygame
from pygame.locals import *
from pygame.color import *
from playspace import PlaySpace
from pymunk import Vec2d
from math import cos, sin

TARGET_FPS = 50

WAITING_PLAYER = 1
PLAYER_PUSHING = 2


class Game:


    def __init__(self):
        self.game_state = WAITING_PLAYER
        self.draw_count = 0
        flags = 0
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        winsize = 800, 600
        pygame.init()

        self.clock = pygame.time.Clock()
        screen = self.screen = pygame.display.set_mode(winsize, flags)
        self.width, self.height = screen.get_width(), screen.get_height()
        pygame.display.set_caption('Toing')
        self.space = PlaySpace(screen)
        self.pushing_shape = self.pushing_delta = None

    def run(self):
        # The target frames per second is used to "sleep" the main loop between
        # screen redraws

        # The Main Event Loop
        while self._handle_events() is not False:
            self._draw()
            self.space.simulate()
            self.clock.tick(TARGET_FPS)

    def _draw(self):

        ### Clear the screen
        self.screen.fill(THECOLORS["black"])

        self.space.draw()

        if self.pushing_delta:
            delta = self.pushing_delta
            bp = self.pushing_shape.body.position
            length = delta.get_length()
            if length > 40:
                length = 40
            angle = delta.get_angle()
            x_delta = length*cos(angle)
            y_delta = length*sin(angle)
            p = bp - Vec2d(x_delta, y_delta)
            print self.pushing_shape.body.position, p
            pygame.draw.line(self.screen, THECOLORS["red"],
                             self.space.flipy(self.pushing_shape.body.position) , self.space.flipy(p), 1)
        pygame.display.flip()

    def _handle_events(self):
        events = pygame.event.get()

        # Handle events
        for event in events:
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                return False
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:  # LMB:
                return self._on_left_mouse_button_down(event)
            elif event.type == MOUSEMOTION:
                return self._on_mouse_motion(event)
            elif event.type == MOUSEBUTTONUP and event.button == 1:  #LMB
                return self._on_left_mouse_button_up(event)

    def _on_left_mouse_button_down(self, event):
        print "mouse down"
        if self.game_state == WAITING_PLAYER:
            mpos = pygame.mouse.get_pos()
            clicked_shape = self.space.space.point_query_first(self.space.flipy(Vec2d(mpos)))
            print "clicked shape", clicked_shape
            if clicked_shape is None:
                return
            self.game_state = PLAYER_PUSHING
            self.pushing_position = mpos
            self.pushing_shape = clicked_shape
            print "Pushing space is", clicked_shape

    def _on_left_mouse_button_up(self, event):
        if not self.pushing_delta or self.game_state != PLAYER_PUSHING:
            return
        delta = self.pushing_delta
        length = delta.get_length()
        if length > 40:
            length = 40
        angle = delta.get_angle()
        x_delta = length*cos(angle)
        y_delta = length*sin(angle)
        p = Vec2d(-x_delta, -y_delta)
        self.pushing_shape.body.apply_impulse(p*30, (0, 0))
        self.pushing_delta = None
        self.game_state = WAITING_PLAYER

    def _on_mouse_motion(self, event):
        if self.game_state != PLAYER_PUSHING or not pygame.mouse.get_pressed()[0]:
            return
        mpos = pygame.mouse.get_pos()
        self.pushing_delta = self.pushing_shape.body.position - self.space.flipy(Vec2d(mpos))


