import random

import pygame
from pygame import Vector2

from camera import Camera
from item import ImageItem


def construct_roads(camera: Camera, pos: Vector2, image_keyboard: str, plus_z_value):
    puzzle_width = 1/3
    puzzle_height = 1/8

    road_length = 40

    puzzle_pieces = []
    items = []
    puzzle_pieces.append('road.png')

    c = +0.2
    items.append(ImageItem(camera,
                           Vector2((-(1 - puzzle_width) / 2)+c, 0) + pos,
                           Vector2(puzzle_width * 1.01, puzzle_height * 1.01),
                           image=image_keyboard,
                           plus_z_value=plus_z_value))

    #affiche la route
    for i in range(1, road_length):
        rnd = random.randint(0, len(puzzle_pieces)-1)
        items.append(ImageItem(camera,
                               Vector2((-(1-puzzle_width)/2)+ i * puzzle_width + c, 0) + pos,
                               Vector2(puzzle_width * 1.01, puzzle_height * 1.01),
                               image=puzzle_pieces[rnd],
                               plus_z_value=plus_z_value))

    items.append(ImageItem(camera,
                           Vector2((-(1 - puzzle_width) / 2) + road_length * puzzle_width + c, 0) + pos,
                           Vector2(puzzle_width * 1.01, puzzle_height * 1.01),
                           image='roadFinish.png',
                           plus_z_value=plus_z_value))

    for item in items:
        item.set_z_value(20)
    return items


class Protein(ImageItem):
    def __init__(self, camera, pos, pzv):
        protein_size = Vector2(0.04, 0.07)
        super().__init__(camera, pos, protein_size, image='proteins.png', plus_z_value=pzv)
        self.set_z_value(25)

    @property
    def rect(self):
        size = Vector2(self.size.x, self.size.y * 0.5)
        rect = (self.pos.x - 0.5 * size.x + 0.05, self.pos.y - 0.5 * size.y, size.x, size.y * 0.05)
        l = 1000
        return pygame.Rect(rect[0]*l, rect[1]*l, rect[2]*l, rect[3]*l)


class Obstacle(ImageItem):
    def __init__(self, camera, pos, pzv):
        obstacle_size = Vector2(0.2, 0.25)
        super().__init__(camera, pos, obstacle_size, image='obstacle.png', plus_z_value=pzv)
        self.set_z_value(40)

    @property
    def rect(self):
        size = Vector2(self.size.x * 0.05, self.size.y * 0.19)
        rect = (self.pos.x - 0.5 * size.x + 0.05, self.pos.y - 0.5 * size.y, size.x, size.y * 0.05)
        l = 1000
        return pygame.Rect(rect[0]*l, rect[1]*l, rect[2]*l, rect[3]*l)


class Car(ImageItem):
    def __init__(self, camera, pos, pzv):
        car_size = Vector2(0.3, 0.3)
        super().__init__(camera, pos, car_size, image='car.png', plus_z_value=pzv)
        self.set_z_value(40)
        self._shaking = False
        self.life = 150
        self.max_life = self.life
        self._is_flying = False
        self._t = 0
        self._T = 10
        self._initial_pos = pos

    def fly(self):
        self._is_flying = True
        self._shaking = False

    def shaking_status(self, shake):
        self._shaking = shake

    def update(self, parent=None):
        if self._is_flying and self._t < self._T:
            self._t += 1
            delta = self._t/self._T
            self.set_rotation(-delta * 90.0)
            self.set_pos(self._initial_pos - delta * Vector2(0.05, -0.09))

        if self._shaking:
            self.set_pos(self._initial_pos + (random.randint(0, 2) - 1) * Vector2(0.01, 0))

        super().update(parent)

    @property
    def rect(self):
        if not self._is_flying:
            size = Vector2(self.size.x * 0.3, self.size.y)
            rect = (self.pos.x - 0.5 * size.x, self.pos.y - 0.5 * size.y, size.x, size.y)
            l = 1000
            return pygame.Rect(rect[0]*l, rect[1]*l, rect[2]*l, rect[3]*l)
        else:
            return pygame.Rect(0, 0, 0, 0)

class Rock(ImageItem):
    def __init__(self, camera, pos, pzv):
        car_size = Vector2(0.3, 0.3)
        super().__init__(camera, pos, car_size, image='rock.png', plus_z_value=pzv)
        self.set_z_value(40)
        self._shaking = False
        self.life = 50
        self.max_life = self.life
        self._is_flying = False
        self._t = 0
        self._T = 10
        self._initial_pos = pos

    def fly(self):
        self._is_flying = True
        self._shaking = False

    def shaking_status(self, shake):
        self._shaking = shake


    def update(self, parent=None):
        if self._is_flying and self._t < self._T:
            self._t += 1
            delta = self._t/self._T
            self.set_rotation(-delta * 90.0)
            self.set_pos(self._initial_pos - delta * Vector2(0.05, -0.09))

        if self._shaking:
            self.set_pos(self._initial_pos + (random.randint(0, 2) - 1) * Vector2(0.01, 0))

        super().update(parent)

    @property
    def rect(self):
        if not self._is_flying:
            size = Vector2(self.size.x * 0.3, self.size.y)
            rect = (self.pos.x - 0.5 * size.x, self.pos.y - 0.5 * size.y, size.x, size.y)
            l = 1000
            return pygame.Rect(rect[0]*l, rect[1]*l, rect[2]*l, rect[3]*l)
        else:
            return pygame.Rect(0, 0, 0, 0)

class Building(ImageItem):
    def __init__(self, camera, pos, pzv):
        car_size = Vector2(0.35, 1)
        super().__init__(camera, pos, car_size, image='building.png', plus_z_value=pzv)
        self.set_z_value(40)
        self._shaking = False
        self.life = 350
        self.max_life = self.life
        self._is_flying = False
        self._t = 0
        self._T = 10
        self._initial_pos = pos

    def fly(self):
        self._is_flying = True
        self._shaking = False

    def shaking_status(self, shake):
        self._shaking = shake

    def update(self, parent=None):
        if self._is_flying and self._t < self._T:
            self._t += 1
            delta = self._t/self._T
            self.set_rotation(-delta * 90.0)
            self.set_pos(self._initial_pos - delta * Vector2(0.0, -0.15))

        if self._shaking:
            self.set_pos(self._initial_pos + (random.randint(0, 2) - 1) * Vector2(0.01, 0))

        super().update(parent)

    @property
    def rect(self):
        if not self._is_flying:
            size = Vector2(self.size.x * 0.3, self.size.y)
            rect = (self.pos.x - 0.5 * size.x, self.pos.y - 0.5 * size.y, size.x, size.y)
            l = 1000
            return pygame.Rect(rect[0]*l, rect[1]*l, rect[2]*l, rect[3]*l)
        else:
            return pygame.Rect(0, 0, 0, 0)
