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
    Main script that creates and runs the game object
"""
from toing.game import Game

def main():
    game = Game()
    game.run()

if __name__=="__main__":
    main()