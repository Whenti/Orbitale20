from asyncio import Event
from enum import Enum

import pygame
from pygame import Vector2

from camera import Camera
from game_callback import GameCallback, SceneId
from item import ImageItem
from player import Player
from scene import Scene, CompositeScene
from scene_finish import SceneFinish
from scene_start import SceneStart

from utils import Road, Protein, Car, Obstacle, Rock
import random

from utils import Road, Protein, Car, Obstacle, Building


class GameMode(Enum):
    START = 0
    GAME = 1
    END = 2
    DONE = 3

#from scene_quentin import Player
from utils import Road, Protein, Car, Obstacle, Building


class SceneNolwenn(Scene):
    def __init__(self,  game_callback: GameCallback, screen: pygame.Surface):
        super().__init__(game_callback, screen)
        self._camera = Camera(self._screen)

        self._finish_line = 13.3
        self._winner = None
        self._cam_initial_pos = None

        self._mode = GameMode.START
        self._timer = 0
        # item image background
        self._camera_background = Camera(self._screen)
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
            protein_list.append(Protein(self._camera, Vector2(0.8, road_y + prot_delta)))
            protein_list.append(Protein(self._camera, Vector2(0.9, road_y + prot_delta)))
            protein_list.append(Protein(self._camera, Vector2(1.0, road_y + prot_delta)))
            protein_list.append(Protein(self._camera, Vector2(1.1, road_y + prot_delta)))

            protein_list.append(Protein(self._camera, Vector2(3, road_y + prot_delta)))
            protein_list.append(Protein(self._camera, Vector2(3.4, road_y + prot_delta)))

            protein_list.append(Protein(self._camera, Vector2(4.4, road_y + prot_delta)))
            protein_list.append(Protein(self._camera, Vector2(4.8, road_y + prot_delta)))
            protein_list.append(Protein(self._camera, Vector2(5.0, road_y + prot_delta)))

            protein_list.append(Protein(self._camera, Vector2(5.6, road_y + prot_delta)))
            protein_list.append(Protein(self._camera, Vector2(5.9, road_y + prot_delta)))

            protein_list.append(Protein(self._camera, Vector2(6.5, road_y + prot_delta)))

            protein_list.append(Protein(self._camera, Vector2(7, road_y + prot_delta)))

            protein_list.append(Protein(self._camera, Vector2(8, road_y + prot_delta)))

            protein_list.append(Protein(self._camera, Vector2(11.8, road_y + prot_delta)))
            protein_list.append(Protein(self._camera, Vector2(12.1, road_y + prot_delta)))
            protein_list.append(Protein(self._camera, Vector2(12.4, road_y + prot_delta)))


        for obstacle_list, road_y in zip([self._obstacles1, self._obstacles2], [road_y_1, road_y_2]):
            obstacle_delta = -0.01
            obstacle_list.append(Obstacle(self._camera, Vector2(2.5, road_y + obstacle_delta)))
            obstacle_list.append(Obstacle(self._camera, Vector2(6.5, road_y + obstacle_delta)))
            obstacle_list.append(Obstacle(self._camera, Vector2(6.8, road_y + obstacle_delta)))

        for car_list, road_y in zip([self._cars1, self._cars2], [road_y_1, road_y_2]):
            rock_delta = -0.002
            car_delta = -0.02
            building_delta = -0.2
            car_list.append(Rock(self._camera, Vector2(4.8, road_y + car_delta)))

            car_list.append(Car(self._camera, Vector2(5.9, road_y + car_delta)))
            car_list.append(Car(self._camera, Vector2(6.1, road_y + car_delta)))

            car_list.append(Car(self._camera, Vector2(9, road_y + car_delta)))

            car_list.append(Building(self._camera, Vector2(12.5, road_y + building_delta)))

        for protein in self._proteins1 + self._proteins2:
            self._add_item(protein)
        for obstacle in self._obstacles1 + self._obstacles2:
            self._add_item(obstacle)
        for car in self._cars1 + self._cars2:
            self._add_item(car)

    def manage_events(self, event: Event):
        if self._mode == GameMode.GAME:
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

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    self._player2.set_right(True)
                elif event.key == pygame.K_a:
                    self._player2.set_left(True)
                elif event.key == pygame.K_w:
                    self._player2.set_up(True)

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    self._player2.set_right(False)
                elif event.key == pygame.K_a:
                    self._player2.set_left(False)
                elif event.key == pygame.K_w:
                    self._player2.set_up(False)


    def camera_pos(self):
        return Vector2(0.5 * self._player1.pos.x + 0.5 * self._player2.pos.x + 0.1, 0)


    def _update_cameras(self):
        self._camera.set_pos(self.camera_pos())

        referent_player = self._player2 if self._player2.pos.x > self._player1.pos.x else self._player2
        diff = abs((self._camera.pos - referent_player.pos).length())
        if diff > 0.48:
            self._camera.set_zoom(0.48 / diff)
        elif diff < 0.37:
            if diff < 0.35:
                diff = 0.35
            self._camera.set_zoom(0.37 / diff)

        self._camera_background.set_pos(0.1 * (self._camera.pos / self._screen.get_width()))

    def done(self):
        return self._mode == GameMode.DONE

    def update(self):
        self._update_cameras()
        super().update()
        self._timer += 1
        if self._mode == GameMode.START:
            if self._timer >= 70:
                self._timer = 70
            lb = self._timer/70
            self._camera.set_pos((1-lb) * Vector2(1.5, -1.1) + 0.5 * lb * self.camera_pos())
            self._camera.set_zoom(0.3 * (1-lb) + lb)

        if self._mode == GameMode.END:
            T = 70
            if self._timer >= T:
                self._mode = GameMode.DONE
            lb = self._timer/T
            self._camera.set_pos(self._winner.pos * lb + (1-lb) * self._cam_initial_pos)
            self._camera.set_zoom(4 * lb + self._initial_zoom * (1-lb))

        for player, protein_list in zip([self._player1, self._player2], [self._proteins1, self._proteins2]):
            for protein in protein_list:
                if player.rect.colliderect(protein.rect):
                    self._remove_item(protein)
                    protein_list.remove(protein)
                    player.gain_power()

        for player, obstacle_list in zip([self._player1, self._player2], [self._obstacles1, self._obstacles2]):
            for obstacle in obstacle_list:
                if obstacle.pos.x - player.pos.x < 0:
                    obstacle.set_z_value(25)
                else:
                    obstacle.set_z_value(37)
                if player.rect.colliderect(obstacle.rect) and player.pos.x - obstacle.pos.x < 0.020:
                    player.set_pos(Vector2(obstacle.pos.x - obstacle.size.x * 0.1, player.pos.y))
                    player.stop()

        for player, car_list in zip([self._player1, self._player2], [self._cars1, self._cars2]):
            for car in car_list:
                if player.rect.colliderect(car.rect):
                    player.attack(car)
                    player.set_pos(Vector2(car.pos.x - car.size.x / 3, player.pos.y))
                    player.stop()

        if self._player1.pos.x >= self._finish_line:
            self._winner = self._player1

        elif self._player2.pos.x >= self._finish_line:
            self._winner = self._player2

        if self._winner is not None and self._mode == GameMode.GAME:
            self._mode = GameMode.END
            self._timer = 0
            self._cam_initial_pos = self._camera.pos
            self._initial_zoom = self._camera.zoom
            self._winner.set_winner()

    def start_game(self):
        self._mode = GameMode.GAME

    def winner(self):
        return self._winner


class GameScene(CompositeScene):

    def __init__(self, game_callback: GameCallback, screen: pygame.Surface):
        super().__init__(game_callback, screen)
        self._scene_nol = SceneNolwenn(game_callback, screen)
        self._scene_start = SceneStart(game_callback, screen)
        self._scene_end = None

        self._add_scene(self._scene_nol)
        self._add_scene(self._scene_start)

    def update(self):
        if self._scene_start is not None and self._scene_start._done:
            self._remove_scene(self._scene_start)
            self._scene_start = None
            self._scene_nol.start_game()

        if self._scene_nol.winner() is not None and self._scene_end is None:
            self._scene_end = SceneFinish(self._game_callback, self._screen)
            self._add_scene(self._scene_end)

        if self._scene_nol.done():
            self._game_callback.set_scene_id(SceneId.INTRO)

        super().update()
