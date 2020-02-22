from asyncio import Event

import pygame
from pygame import Vector2

from camera import Camera
from game_callback import GameCallback
from item import ImageItem, CompositeItem
from scene import Scene

import random

class Road(CompositeItem):
    def __init__(self, camera: Camera, pos: Vector2):
        super().__init__(camera, pos, Vector2(-0.2, -0.3))

        brown1 = (153, 76, 0)
        brown2 = (153, 0, 0)
        brown3 = (204, 102, 0)

        puzzle_width = 1/3
        puzzle_height = 1/20

        road_length = 10

        self._puzzle_pieces = []
        self._puzzle_pieces.append(brown1)
        self._puzzle_pieces.append(brown2)
        self._puzzle_pieces.append(brown3)


        #affiche la route
        for i in range(road_length):
            rnd = random.randint(0, len(self._puzzle_pieces)-1)
            self._add_item( ImageItem(self._camera,
                                     Vector2( (-(1-puzzle_width)/2)+ i * puzzle_width, 0),
                                     Vector2(puzzle_width, puzzle_height),
                                     color=self._puzzle_pieces[rnd]) )


    #def update(self, parent: Item = None):
        # add update: fait avancer l'image (camera ?)
        #super().update()

class SceneNolwenn(Scene):
    def __init__(self,  game_callback: GameCallback, screen: pygame.Surface):
        #copy from SceneTest
        super().__init__(game_callback, screen)
        self._camera = Camera(self._screen)

        # item image background
        self._camera_background = Camera(self._screen);
        self._image_background = ImageItem(self._camera_background, Vector2(0, 0), Vector2(1, 1), color=(0, 0, 250))
        self._image_background.set_z_value = 10
        self._add_item(self._image_background)


        # item image composite roads
        self._road1 = Road(self._camera, Vector2(0, 0))
        self._road1.set_z_value(20)
        self._add_item(self._road1)

        self._road2 = Road(self._camera, Vector2(0, 0.2))
        self._road2.set_z_value(20)
        self._add_item(self._road2)



    def manage_events(self, event: Event):
        pass

    def update(self):
        self._camera_background.move(Vector2(0.1, 0))
        self._camera.move(Vector2(2, 0))
        super().update()