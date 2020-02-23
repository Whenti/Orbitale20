import random

import pygame
from pygame import Vector2

from camera import Camera
from item import CompositeItem, ImageItem


class Road(CompositeItem):
    def __init__(self, camera: Camera, pos: Vector2):
        super().__init__(camera, pos, Vector2(-0.2, -0.3))

        puzzle_width = 1/3
        puzzle_height = 1/8

        road_length = 10

        self._puzzle_pieces = []
        self._puzzle_pieces.append('road1.png')
        #self._puzzle_pieces_append('xxx.png')


        #affiche la route
        for i in range(road_length):
            rnd = random.randint(0, len(self._puzzle_pieces)-1)
            self._add_item(ImageItem(self._camera,
                                      Vector2( (-(1-puzzle_width)/2)+ i * puzzle_width, 0),
                                      Vector2(puzzle_width, puzzle_height),
                                      image=self._puzzle_pieces[rnd]) )


class Protein(ImageItem):
    def __init__(self, camera, pos):
        protein_size = Vector2(0.2, 0.27)
        super().__init__(camera, pos, protein_size, image='proteins.png')
        self.set_z_value(25)


class Obstacle(ImageItem):
    def __init__(self, camera, pos):
        obstacle_size = Vector2(0.2, 0.2)
        super().__init__(camera, pos, obstacle_size, image='obstacle.png')
        self.set_z_value(27)


class Car(ImageItem):
    def __init__(self, camera, pos):
        car_size = Vector2(0.3, 0.3)
        super().__init__(camera, pos, car_size, image='car.png')
        self.set_z_value(40)
        self.life = 100
        self.max_life = self.life
        self._is_flying = False
        self._t = 0
        self._T = 10
        self._initial_pos = pos

    def fly(self):
        self._is_flying = True

    def update(self, parent=None):
        if self._is_flying and self._t < self._T:
            self._t += 1
            delta = self._t/self._T
            self.set_rotation(-delta * 90.0)
            self.set_pos(self._initial_pos - delta * Vector2(0.05, -0.05))
        super().update(parent)

    @property
    def rect(self):
        if not self._is_flying:
            rect = (self.pos.x - 0.5 * self.size.x, self.pos.y - 0.5 * self.size.y, self.size.x, self.size.y)
            l = 1000
            return pygame.Rect(rect[0]*l, rect[1]*l, rect[2]*l, rect[3]*l)
        else:
            return pygame.Rect(0, 0, 0, 0)