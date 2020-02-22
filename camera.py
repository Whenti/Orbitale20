#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from pygame.math import Vector2


class Camera:

    def __init__(self, screen):
        self._screen = screen
        self._zoom = 1
        self._pos = Vector2(0.0, 0.0)

    def set_pos(self, pos: Vector2):
        self._pos = pos

    def move(self, dpos: Vector2):
        self._pos += dpos

    def set_zoom(self, zoom: float):
        self._zoom = zoom

    def dzoom(self, dzoom: float):
        self._zoom *= dzoom

    @property
    def size(self) -> Vector2:
        return Vector2(self._screen.get_size())

    @property
    def zoom(self):
        return self._zoom

    @property
    def pos(self):
        return self._pos

    @property
    def screen(self):
        return self._screen
