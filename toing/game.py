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

    ************************************************************************
    The "Game" class provides the main game event loop and event handlers
"""

import os
import pygame
from pygame.locals import *
from pygame.color import *
from playspace import PlaySpace
from pymunk import Vec2d
from math import cos, sin

# Target frames per second is used to "sleep" the main loop between frame updates
TARGET_FPS = 50

WAITING_PLAYER_MOVE = 1
PLAYER_PUSHING_BALL = 2


class Game:

    def __init__(self):
        self.game_state = WAITING_PLAYER_MOVE
        flags = 0
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        winsize = 800, 600
        pygame.init()

        self.push_arrow = pygame.image.load(os.path.join('data', 'green_arrow.png'))
        self.clock = pygame.time.Clock()
        screen = self.screen = pygame.display.set_mode(winsize, flags)
        self.width, self.height = screen.get_width(), screen.get_height()
        pygame.display.set_caption('Toing')
        self.space = PlaySpace(screen)
        self.pushing_shape = None
        self.pushing_position = None


    def run(self):

        # The Main Event Loop
        while self._handle_events() is not False:
            self._draw()
            self.space.simulate()
            self.clock.tick(TARGET_FPS)

    def _draw(self):

        ### Clear the screen
        self.screen.fill(THECOLORS["black"])

        ### Draw the physics space
        self.space.draw()

        # Draw the ball push pointer
        if self.game_state == PLAYER_PUSHING_BALL:
            delta = self.pushing_position - self.pushing_shape.body.position
            length = min(delta.get_length(), 40)  # Limit length to 40
            if length < 1:
                return
            angle = delta.get_angle()
            angle_degrees = round(delta.get_angle_degrees())
            print angle_degrees
            x_delta = length*cos(angle)
            y_delta = length*sin(angle)
            p = self.pushing_shape.body.position + Vec2d(x_delta, y_delta)

            sized_push_arrow = pygame.transform.smoothscale(self.push_arrow, (int(length), 10))

            # Arrow center position is a point in the angular direction
            arrow_center_pos = self.pushing_shape.body.position + Vec2d(x_delta/2, y_delta/2)
            # Rotate the image
            rotated_arrow = pygame.transform.rotate(sized_push_arrow, angle_degrees)
            # Draw the image centered at the arrow_center_pos
            rotated_w, rotated_h = rotated_arrow.get_size()
            draw_pos = Vec2d(arrow_center_pos.x - rotated_w / 2, arrow_center_pos.y + rotated_h / 2)
            self.screen.blit(rotated_arrow, self.space.flipy(draw_pos))

        pygame.display.flip()

    def _handle_events(self):
        events = pygame.event.get()

        # Handle events
        for event in events:
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                return False
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:  # LMB
                return self._on_left_mouse_button_down()
            elif event.type == MOUSEMOTION:
                return self._on_mouse_motion()
            elif event.type == MOUSEBUTTONUP and event.button == 1:  # LMB
                return self._on_left_mouse_button_up()

    def _on_left_mouse_button_down(self):
        if self.game_state != WAITING_PLAYER_MOVE:
            return
        mouse_pos = self.space.flipy(Vec2d(pygame.mouse.get_pos()))
        clicked_shape = self.space.space.point_query_first(mouse_pos)
        if clicked_shape is None:
            return
        self.game_state = PLAYER_PUSHING_BALL
        self.pushing_position = mouse_pos
        self.pushing_shape = clicked_shape
        pygame.mouse.set_visible(False)

    def _on_left_mouse_button_up(self):
        pygame.mouse.set_visible(True)
        if self.game_state != PLAYER_PUSHING_BALL:
            return
        delta = self.pushing_position - self.pushing_shape.body.position
        length = min(delta.get_length(), 40)  # Limit length to 40
        angle = delta.get_angle()
        force = Vec2d(length*cos(angle), length*sin(angle))
        self.pushing_shape.body.apply_impulse(force*40, (0, 0))
        self.game_state = WAITING_PLAYER_MOVE

    def _on_mouse_motion(self):
        if self.game_state != PLAYER_PUSHING_BALL or not pygame.mouse.get_pressed()[0]:
            return
        mouse_pos = self.space.flipy(Vec2d(pygame.mouse.get_pos()))
        self.pushing_position = mouse_pos


