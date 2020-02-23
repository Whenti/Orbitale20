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
        self._items = []
        self._image = None
        self._parent = None
        self._transparency = 255

    def draw(self):
        parent = self._parent
        if parent is not None:
            translation = parent.pos
            theta = parent.theta
        else:
            translation = Vector2(0.0, 0.0)
            theta = 0.0
        zoom = self._camera.zoom

        width = int(zoom * self._size.x * self._camera.size.x)
        height = int(zoom * self._size.y * self._camera.size.y)
        self._image_to_draw = pygame.transform.scale(self._image, (width, height))

        rotation = int(self._theta + theta) % 360
        if rotation:
            self._image_to_draw = pygame.transform.rotate(self._image_to_draw, rotation)

        camera_pos = self._camera.pos * self._camera.size.x
        center = self._camera.size.x * zoom * (self._pos + translation) - zoom * camera_pos + 0.5 * self._camera.size
        self._scene_rect = self._image_to_draw.get_rect(center=center)
        if self._transparency != 255:
            self._image_to_draw.set_alpha(self._transparency)
        self._camera.screen.blit(self._image_to_draw, self._scene_rect.topleft)

    def update(self, parent: Item = None):
        self._parent = parent

    def set_size(self, size: Vector2):
        self._size = size

    def increase_transparency(self):
        self._transparency -= 30

    @property
    def size(self):
        return self._size

    @property
    def rect(self):
        rect = (self.pos.x - 0.5 * self.size.x, self.pos.y - 0.5 * self.size.y, self.size.x, self.size.y)
        l = 1000
        return pygame.Rect(rect[0]*l, rect[1]*l, rect[2]*l, rect[3]*l)


class ImageItem(RectItem):

    def __init__(self, camera: Camera,
                 pos: Vector2,
                 size: Vector2,
                 theta: float = 0.0,
                 color: Tuple[int, int, int] = None,
                 image: str = None):
        assert not (image is None and color is None)
        self._img = image
        super().__init__(camera, pos, size, theta)
        if image is not None:
            self.load_image(image)
        else:
            real_size = (int(self._size.x * self._camera.size.x), int(self._size.y * self._camera.size.x))
            self._image = Surface(real_size)
            self._image.fill(color)
            self._image.set_colorkey((255, 0, 0))

    def load_image(self, image):
        global _image_cache
        real_size = (int(self._size.x * self._camera.size.x), int(self._size.y * self._camera.size.x))
        if image in _image_cache:
            self._image = _image_cache[image]
        else:
            self._image = pygame.image.load(os.path.join('./resources/images/', image))
            # self._image.set_colorkey((0, 0, 0))
            _image_cache[image] = self._image



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
        real_size = (int(size * text_size[0] * self._camera.size.x), int(size * text_size[1] * self._camera.size.x))
        self._image = pygame.transform.scale(self._image, real_size)


class CompositeItem(Item):
    def __init__(self, camera: Camera, pos: Vector2, size: Vector2, rotation: float = 0.0):
        super().__init__(camera, pos, rotation)
        self._size = size
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
        rect = self._items[0].scene_rect
        for item in self._items[1:]:
            rect.union(item.scene_rect)
        return rect

    @property
    def size(self):
        return self._size

    @property
    def rect(self):
        rect = (self.pos.x - 0.5 * self.size.x, self.pos.y - 0.5 * self.size.y, self.size.x, self.size.y)
        l = 1000
        return pygame.Rect(rect[0]*l, rect[1]*l, rect[2]*l, rect[3]*l)
