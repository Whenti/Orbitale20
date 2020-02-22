#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from typing import Tuple, Optional

import pygame
import os
from pygame.font import Font
from pygame.math import Vector2
from pygame import Rect, Surface

from camera import Camera

_image_cache = {}


class Item:

    def __init__(self, camera: Camera, pos: Vector2, theta: float = 0.0):
        self._camera = camera
        self._pos = pos
        self._theta = theta
        self._z_value = 0.0

    def draw(self):
        raise NotImplementedError

    def collides(self, other: 'Item'):
        pass

    def update(self, parent: 'Item' = None):
        pass

    def set_pos(self, pos: Vector2):
        self._pos = pos

    def move(self, dpos: Vector2):
        self._pos += dpos

    def set_rotation(self, theta: float):
        self._theta = theta

    def rotate(self, dtheta: float):
        self._theta += dtheta

    def set_z_value(self, z_value: float):
        self._z_value = z_value

    def mouse_over(self) -> bool:
        return self.scene_rect.collidepoint(pygame.mouse.get_pos())

    @property
    def scene_rect(self) -> Optional[Rect]:
        return self._scene_rect

    @property
    def pos(self) -> Vector2:
        return self._pos

    @property
    def theta(self) -> float:
        return self._theta

    @property
    def z_value(self) -> float:
        return self._z_value


class RectItem(Item):
    def __init__(self, camera: Camera, pos: Vector2, size: Vector2, theta: float = 0.0):
        super().__init__(camera, pos, theta)
        self._size = size
        self._image_to_draw = None
        self._scene_rect = None

    def draw(self):
        self._camera.screen.blit(self._image_to_draw, self._scene_rect.topleft)

    def update(self, parent: Item = None):
        if parent is not None:
            translation = parent.pos
            theta = parent.theta
        else:
            translation = Vector2(0.0, 0.0)
            theta = 0.0
        zoom = self._camera.zoom

        if zoom != 1.0:
            width = int(zoom * self._image.get_width())
            height = int(zoom * self._image.get_height())
            self._image_to_draw = pygame.transform.scale(self._image, (width, height))
        else:
            self._image_to_draw = self._image

        rotation = int(self._theta + theta) % 360
        if rotation:
            self._image_to_draw = pygame.transform.rotate(self._image_to_draw, rotation)
        center = self._camera.size.x * zoom * (self._pos + translation) - self._camera.pos + 0.5 * self._camera.size
        self._scene_rect = self._image_to_draw.get_rect(center=center)


class ImageItem(RectItem):

    def __init__(self, camera: Camera,
                 pos: Vector2,
                 size: Vector2,
                 theta: float = 0.0,
                 color: Tuple[int, int, int] = None,
                 image: str = None):
        assert not (image is None and color is None)

        super().__init__(camera, pos, size, theta)
        real_size = (int(self._size.x * self._camera.size.x), int(self._size.y * self._camera.size.x))
        if image is not None:
            global _image_cache
            if image in _image_cache:
                self._image = _image_cache[image]
            else:
                self._image = pygame.image.load(os.path.join('./resources/images/', image))
                self._image = pygame.transform.scale(self._image, real_size)
                self._image.set_colorkey((255, 0, 0))
                _image_cache[image] = self._image
        else:
            self._image = Surface(real_size)
            self._image.fill(color)
            self._image.set_colorkey((255, 0, 0))


class TextItem(RectItem):

    def __init__(self,
                 camera: Camera,
                 pos: Vector2,
                 size: Vector2,
                 text: str,
                 foreground_color: Tuple[int, int, int] = (255, 255, 255),
                 background_color: Tuple[int, int, int] = None,
                 theta: float=0.0):
        super().__init__(camera, pos, size)
        font = Font('freesansbold.ttf', 32)
        self._font = font
        self._foreground_color = foreground_color
        if background_color is None:
            self._background_color = (0, 0, 0)
        self._background_color = background_color
        self._text = None
        self._image = None
        self.set_text(text)
        self._scene_rect = self._image.get_rect()

    def set_text(self, text: str):
        self._text = text
        self._image = self._font.render(self._text, True, self._foreground_color, self._background_color)
        if self._background_color is None:
            self._image.set_colorkey((255, 0, 0))
        text_size = self._image.get_size()
        h_ratio = self._size.x/text_size[0]
        v_ratio = self._size.y/text_size[1]
        size = min(h_ratio, v_ratio)
        print(size)
        real_size = (int(size * text_size[0] * self._camera.size.x), int(size * text_size[1] * self._camera.size.x))
        self._image = pygame.transform.scale(self._image, real_size)


class CompositeItem(Item):
    def __init__(self, camera: Camera, pos: Vector2, size: Vector2, rotation: float = 0.0):
        super().__init__(camera, pos, rotation)
        self._items = []

    def draw(self):
        for item in self._items:
            item.draw()

    def collides(self, other: 'Item'):
        for item in self._items:
            item.collides(other)

    def update(self, parent: Item = None):
        for item in self._items:
            item.update(self)

    def _add_item(self, item: Item):
        self._items.append(item)

    def _remove_item(self, item: Item):
        self._items.remove(item)

    @property
    def scene_rect(self) -> Rect:
        if not self._items:
            return None
        rect = self._items[0].scene_rect
        for item in self._items[1:]:
            rect.union(item.scene_rect)
        return rect
