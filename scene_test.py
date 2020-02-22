#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import pygame
import math

from pygame.event import Event
from pygame import Vector2
from game_callback import GameCallback, SceneId
from scene import Scene


from camera import Camera
from item import CompositeItem, Item, TextItem, ImageItem


class Player(CompositeItem):
    def __init__(self, camera: Camera, pos: Vector2):
        super().__init__(camera, pos, Vector2(-0.2, -0.3))

        self._center_item = ImageItem(camera, Vector2(0, 0), Vector2(0.1, 0.1), color=(255, 255, 0))
        self._rotating_item = ImageItem(camera, Vector2(0, 0), Vector2(0.05, 0.05), color=(0, 255, 0))
        self._text_item = TextItem(camera, Vector2(0, 0), Vector2(0.2, 0.2), "oui bonjour")
        self._add_item(self._center_item)
        self._add_item(self._rotating_item)
        self._add_item(self._text_item)

    def update(self, parent: Item = None):
        self._rotating_item.rotate(-3)
        rotation = self._rotating_item.theta*math.pi/180.0
        pos = Vector2(0.10 * math.cos(rotation), 0.10 * math.sin(rotation))
        self._rotating_item.set_pos(pos)
        self._center_item.rotate(1)
        super().update()


class SceneTest(Scene):
    def __init__(self, game_callback: GameCallback, screen: pygame.Surface):
        super().__init__(game_callback, screen)
        self._camera = Camera(self._screen)

        self._player = Player(self._camera, Vector2(-0.2, -0.2))
        self._player.set_z_value(10)
        self._add_item(self._player)

        self._rectangle = ImageItem(self._camera, Vector2(0.2, 0.2), Vector2(0.1, 0.1), color=(0, 0, 250))
        #self._rectangle = ImageItem(self._camera, Vector2(0.2, 0.2), Vector2(0.1, 0.1), image='img.png')
        self._add_item(self._rectangle)

        self._TIME = 100
        self._t = 0

    def manage_events(self, event: Event):
        pass

    def update(self):
        self._t += 1
        if self._t == self._TIME:
            self._game_callback.set_scene_id(SceneId.TEST)
        self._camera.dzoom(0.99)
        self._player.move(Vector2(0.01, 0))
        super().update()
