from asyncio import Event

import pygame
from pygame import Vector2

from camera import Camera
from game_callback import GameCallback
from item import ImageItem, CompositeItem
from player import Player
from scene import Scene

import random

#from scene_quentin import Player
from utils import Road, Protein, Car, Obstacle


class SceneNolwenn(Scene):
    def __init__(self,  game_callback: GameCallback, screen: pygame.Surface):
        #copy from SceneTest
        super().__init__(game_callback, screen)
        self._camera = Camera(self._screen)

        # item image background
        self._camera_background = Camera(self._screen);
        self._image_background = ImageItem(self._camera_background, Vector2(0, 0), Vector2(1, 1), image='background.png')
        self._add_item(self._image_background)

        # defining roads y position
        road_y_1 = 0.0
        road_y_2 = 0.2

        # item image composite roads
        self._road1 = Road(self._camera, Vector2(0, road_y_1))
        self._road1.set_z_value(20)
        self._add_item(self._road1)

        self._road2 = Road(self._camera, Vector2(0, road_y_2))
        self._road2.set_z_value(20)
        self._add_item(self._road2)

        # roads
        self._player1 = Player(self._camera, Vector2(0, road_y_1 - 0.08))
        self._player1.set_z_value(30)
        self._add_item(self._player1)

        self._player2 = Player(self._camera, Vector2(0, road_y_2 - 0.08))
        self._player2.set_z_value(30)
        self._add_item(self._player2)

        # proteins
        self._proteins1 = []
        self._proteins2 = []

        # obstacles
        self._obstacles1 = []
        self._obstacles2 = []

        # cars
        self._cars1 = []
        self._cars2 = []

        # setting the road for both player
        for protein_list, road_y in zip([self._proteins1, self._proteins2], [road_y_1, road_y_2]):
            prot_delta = -0.02
            protein_list.append(Protein(self._camera, Vector2(0, road_y + prot_delta)))
            protein_list.append(Protein(self._camera, Vector2(0.3, road_y + prot_delta)))

        for obstacle_list, road_y in zip([self._obstacles1, self._obstacles2], [road_y_1, road_y_2]):
            obstacle_delta = -0.02
            obstacle_list.append(Obstacle(self._camera, Vector2(0.8, road_y + obstacle_delta)))

        for car_list, road_y in zip([self._cars1, self._cars2], [road_y_1, road_y_2]):
            car_delta = -0.02
            car_list.append(Car(self._camera, Vector2(0.5, road_y + car_delta)))

        for protein in self._proteins1 + self._proteins2:
            self._add_item(protein)
        for obstacle in self._obstacles1 + self._obstacles2:
            self._add_item(obstacle)
        for car in self._cars1 + self._cars2:
            self._add_item(car)

    def manage_events(self, event: Event):
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self._player1.set_right(True)
                elif event.key == pygame.K_LEFT:
                    self._player1.set_left(True)
                elif event.key == pygame.K_UP:
                    self._player1.set_up(True)

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self._player1.set_right(False)
                elif event.key == pygame.K_LEFT:
                    self._player1.set_left(False)
                elif event.key == pygame.K_UP:
                    self._player1.set_up(False)

    def _update_cameras(self):
        camera_pos = Vector2(0.5 * self._player1.pos.x + 0.5 * self._player2.pos.x + 0.1/self._camera.zoom, 0)
        self._camera.set_pos(camera_pos)

        diff = abs((self._camera.pos - self._player1.pos).length())
        if diff > 0.3 / self._camera.zoom:
            self._camera.set_zoom(0.3 / diff)

        self._camera_background.set_pos(0.1 * (self._camera.pos / self._screen.get_width()))

    def update(self):
        self._update_cameras()
        super().update()
        for player, protein_list in zip([self._player1, self._player2], [self._proteins1, self._proteins2]):
            for protein in protein_list:
                if player.rect.colliderect(protein.rect):
                    self._remove_item(protein)
                    protein_list.remove(protein)
                    player.gain_power()

        for player, obstacle_list in zip([self._player1, self._player2], [self._obstacles1, self._obstacles2]):
            for obstacle in obstacle_list:
                if player.rect.colliderect(obstacle.rect):
                    player.set_pos(Vector2(obstacle.pos.x - obstacle.size.x / 1.3, player.pos.y))
                    player.stop()

        for player, car_list in zip([self._player1, self._player2], [self._cars1, self._cars2]):
            for car in car_list:
                if player.rect.colliderect(car.rect):
                    player.attack(car)
                    player.set_pos(Vector2(car.pos.x - car.size.x / 1.3, player.pos.y))
                    player.stop()

