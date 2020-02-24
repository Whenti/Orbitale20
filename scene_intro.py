#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import pygame
import math

from pygame.event import Event
from pygame import Vector2
from game_callback import GameCallback, SceneId
from player import Player
from scene import Scene


from camera import Camera
from item import CompositeItem, Item, TextItem, ImageItem
from utils import Protein, Car, Building



class SceneIntro(Scene):
    def __init__(self, game_callback: GameCallback, screen: pygame.Surface):
        super().__init__(game_callback, screen)
        self._state = 0
        self._t = 0
        self._t_protein = 0
        self._t_destroy = 0
        self._end_time = 0
        self._t_entree = 0

        self._zoom = 0.7

        self._camera_entree = Camera(self._screen)
        self._entree = ImageItem(self._camera_entree, Vector2(0.3, 0.2), Vector2(0.10, 0.20), image='enter.png')
        self._add_item(self._entree)

        self._camera = Camera(self._screen)
        self._camera.set_pos(Vector2(0.0, -0.3))
        self._camera.set_zoom(3.1)

        self._title = TextItem(self._camera, Vector2(0.0, -0.30), Vector2(0.30, 0.10), "Gonflette Racing!")
        self._title.set_text_size(300)
        self._add_item(self._title)

        self._tuto = TextItem(self._camera, Vector2(0.0, -0.30), Vector2(0.30, 0.10), "Tutorial !")
        self._tuto.set_text_size(300)

        self._credits = TextItem(self._camera, Vector2(-0.07, -0.34), Vector2(0.15, 0.02), "La famille LÉVÊQUE présente...")
        self._add_item(self._credits)

        self._player_left = Player(self._camera, Vector2(0.6, -0.1))
        self._player_left._power = 10
        self._player_right = Player(self._camera, Vector2(0.5, -0.1))
        self._player_right._power = 1

        self._player_run_w = Player(self._camera, Vector2(-0.5, 0.18))
        self._player_run_w._power = 1
        self._player_run_w.set_right(True)
        self._player_run_s = Player(self._camera, Vector2(0.5, 0.18))
        self._player_run_s._power = 10
        self._player_run_s.set_right(True)

        self._player_inflating = Player(self._camera, Vector2(-0.55, -0.1))
        self._add_item(self._player_inflating)

        self._player_car = Player(self._camera, Vector2(-0.20, -0.1))
        self._player_building = Player(self._camera, Vector2(0.15, -0.1))
        self._player_building._power = 10
        self._car = Car(self._camera, self._player_car.pos + Vector2(0.10, 0.03), 0.0)
        self._car.set_size(Vector2(0.5 * self._car.size.x, 0.5 * self._car.size.y))
        self._building = Building(self._camera, self._player_building.pos + Vector2(0.10, -0.03), 0.0)
        self._building.set_size(Vector2(0.5 * self._building.size.x, 0.5 * self._building.size.y))
        self._player_car.attack(self._car)
        self._player_building.attack(self._building)


        for player in [self._player_left, self._player_right, self._player_run_s, self._player_run_w,
                       self._player_car, self._player_building, self._building, self._car]:
            self._add_item(player)
            player.test = True

        self._proteins = []

    def manage_events(self, event: Event):
        if event.type == pygame.KEYUP:
            if event.key == 13:
                if self._state != 0:
                    self._end_time = 1
                else:
                    self._state = 1

    def update(self):
        # self._car.life = 300
        # self._building.life = 300
        self._t += 1
        for player in [self._player_run_w, self._player_run_s]:
            if player.pos.x >= 0.6:
                player.pos.x = -0.6

        if self._t == 15:
            self._t = 0
            for player in [self._player_right, self._player_left]:
                player.set_up(True)
        else:
            for player in [self._player_right, self._player_left]:
                player.set_up(False)

        self._player_inflating.loose_power()
        self._t_protein += 1
        if self._t_protein == 35:
            self._t_protein = 0
            self._proteins.append(Protein(self._camera, Vector2(-0.55, -0.4), 0.0))
            self._add_item(self._proteins[-1])

        for protein in self._proteins:
            protein.move(Vector2(0, 0.01))
            if protein.pos.y >= -0.1:
                self._remove_item(protein)
                self._proteins.remove(protein)
                self._player_inflating.gain_power()

        self._t_destroy += 1
        if self._t_destroy >= 50:
            self._t_destroy = 0
            for item in [self._car, self._building]:
                self._remove_item(item)
            self._car = Car(self._camera, self._player_car.pos + Vector2(0.10, 0.03), 0.0)
            self._car.set_size(Vector2(0.5 * self._car.size.x, 0.5 * self._car.size.y))
            self._building = Building(self._camera, self._player_building.pos + Vector2(0.10, -0.03), 0.0)
            self._building.set_size(Vector2(0.5 * self._building.size.x, 0.5 * self._building.size.y))
            for item in [self._car, self._building]:
                self._add_item(item)
            self._player_car.attack(self._car)
            self._player_building.attack(self._building)

        TT = 15
        if self._state and self._state < 15:
            if self._state == 1:
                self._add_item(self._tuto)
                self._remove_item(self._title)
                if self._entree in self._items:
                    self._remove_item(self._entree)
            self._state += 1
            lb = self._state/TT
            self._camera.set_pos(Vector2(0.0, 0.0) * lb + (1-lb) * Vector2(0.0, -0.3))
            self._camera.set_zoom(self._zoom * lb + 3.1 * (1-lb))
        elif self._end_time:
            if self._entree in self._items:
                self._remove_item(self._entree)
            self._end_time += 1
            self._camera.set_zoom(self._camera.zoom * 0.9)
            self._camera.move(Vector2(-0.40/self._camera.zoom, 0))
            if self._end_time >= 20:
                self._game_callback.set_scene_id(SceneId.FINAL)
        else:
            self._t_entree += 1
            if self._t_entree == 5:
                self._t_entree = 0
                if self._entree in self._items:
                    self._remove_item(self._entree)
                else:
                    self._add_item(self._entree)

        super().update()
