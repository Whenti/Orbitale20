from asyncio import Event

import pygame
from pygame import Vector2

from camera import Camera
from game_callback import GameCallback
from item import ImageItem, CompositeItem
from scene import Scene

import random

from scene_quentin import Player


class Road(CompositeItem):
    def __init__(self, camera: Camera, pos: Vector2):
        super().__init__(camera, pos, Vector2(-0.2, -0.3))

        puzzle_width = 1/3
        puzzle_height = 1/20

        road_length = 10

        self._puzzle_pieces = []
        self._puzzle_pieces.append('road1.png')
        #self._puzzle_pieces_append('xxx.png')


        #affiche la route
        for i in range(road_length):
            rnd = random.randint(0, len(self._puzzle_pieces)-1)
            self._add_item( ImageItem(self._camera,
                                     Vector2( (-(1-puzzle_width)/2)+ i * puzzle_width, 0),
                                     Vector2(puzzle_width, puzzle_height),
                                     image=self._puzzle_pieces[rnd]) )


class Protein(ImageItem):
    def __init__(self, camera, pos):
        protein_size = Vector2(0.05, 0.05)
        super().__init__(camera, pos, protein_size, color=(50, 50, 50))


class SceneNolwenn(Scene):
    def __init__(self,  game_callback: GameCallback, screen: pygame.Surface):
        #copy from SceneTest
        super().__init__(game_callback, screen)
        self._camera = Camera(self._screen)

        # item image background
        self._camera_background = Camera(self._screen);
        self._image_background = ImageItem(self._camera_background, Vector2(0, 0), Vector2(1, 9/16), image='background.png')
        self._add_item(self._image_background)

        # item image composite roads
        self._road1 = Road(self._camera, Vector2(0, 0))
        self._road1.set_z_value(20)
        self._add_item(self._road1)

        self._road2 = Road(self._camera, Vector2(0, 0.2))
        self._road2.set_z_value(20)
        self._add_item(self._road2)

        # roads
        self._player = Player(self._camera, Vector2(0, 0))
        self._player.set_z_value(10)
        self._add_item(self._player)

        # proteins
        self._proteins1 = []
        self._proteins2 = []

        self._proteins1.append(Protein(self._camera, Vector2(0, -0.05)))
        self._proteins1.append(Protein(self._camera, Vector2(0.3, -0.05)))
        self._proteins1.append(Protein(self._camera, Vector2(0.7, -0.05)))
        self._proteins1.append(Protein(self._camera, Vector2(1, -0.05)))

        for protein in self._proteins1 + self._proteins2:
            self._add_item(protein)

    def manage_events(self, event: Event):
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self._player.set_right(True)
                elif event.key == pygame.K_LEFT:
                    self._player.set_left(True)
                elif event.key == pygame.K_UP:
                    self._player.set_up(True)

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self._player.set_right(False)
                elif event.key == pygame.K_LEFT:
                    self._player.set_left(False)
                elif event.key == pygame.K_UP:
                    self._player.set_up(False)

    def update(self):
        self._camera_background.move(Vector2(0.5, 0))
        self._camera.move(Vector2(2, 0))
        super().update()
        for protein in self._proteins1:
            if self._player.rect.colliderect(protein.rect):
                self._remove_item(protein)
                self._proteins1.remove(protein)

