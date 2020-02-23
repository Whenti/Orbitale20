#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import pygame

from pygame.event import Event
from pygame import Vector2
from game_callback import GameCallback, SceneId
from scene import Scene

from camera import Camera
from item import CompositeItem, Item, TextItem, ImageItem


class SceneFinish(Scene):
    def __init__(self, game_callback: GameCallback, screen: pygame.Surface):
        super().__init__(game_callback, screen)
        self._camera = Camera(self._screen)

        self._width_funny_object = 0.3
        self._height_funny_object = 0.3

        self._victory_word = TextItem(self._camera,
                                       Vector2(0, 0),
                                       Vector2(self._width_funny_object, self._height_funny_object),
                                       'Bravo Monsieur !')

        self._add_item(self._victory_word)

        self._t = 0
        self._T = 20

    def manage_events(self, event: Event):
        pass

    def update(self):
        self._t += 1

        if self._t <= self._T:
            self._victory_word.set_rotation(- 360 * self._t / self._T)

        super().update()
