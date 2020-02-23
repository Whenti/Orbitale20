#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import pygame

from pygame.event import Event
from pygame import Vector2
from game_callback import GameCallback, SceneId
from scene import Scene


from camera import Camera
from item import CompositeItem, Item, TextItem, ImageItem


class SceneStart(Scene):
    def __init__(self, game_callback: GameCallback, screen: pygame.Surface):
        super().__init__(game_callback, screen)
        self._camera = Camera(self._screen)

        self._width_funny_object = 0.3
        self._height_funny_object = 0.5

        self._pos3 = Vector2(-(1+self._width_funny_object)*0.5, 0)
        self._pos2 = Vector2((1+self._width_funny_object)*0.5, 0)
        self._pos1 = Vector2(0, (1+self._height_funny_object)*0.5)
        self._pos_start = Vector2(0, -(1+self._height_funny_object)*0.5)

        self._funny_object = ImageItem(self._camera,
                                       self._pos3,
                                       Vector2(self._width_funny_object, self._height_funny_object),
                                       image='funny3.png')
        self._funny_object.set_z_value(100)

        self._current_step=3
        self._add_item(self._funny_object)

        self._t = 0
        self._T = 30
        self._done = False


    def manage_events(self, event: Event):
        pass

    def update(self):
        self._t += 1
        i = self._t % self._T

        if self._t < self._T:
            step = 3
            self._funny_object.set_pos(self._pos3 + Vector2(i*0.05, 0))

        elif self._t < 2*self._T:
            step = 2
            self._funny_object.set_pos(self._pos2 - Vector2(i*0.05, 0))

        elif self._t < 3*self._T:
            step = 1
            self._funny_object.set_pos(self._pos1 - Vector2(0, i*0.05))

        elif self._t < 3.5*self._T:
            step = 0
            if i < - self._pos_start.y / 0.05:
                self._funny_object.set_pos(self._pos_start + Vector2(0, i*0.05))
            else:
                self._funny_object.increase_transparency()
        else:
            step = 0
            self._done = True


        if self._current_step - step > 0:
             funny_numbers = ['go.png', 'funny1.png', 'funny2.png', 'funny3.png']
             self._funny_object.load_image(funny_numbers[step])
             self._current_step = step

        print(step)



        super().update()
