#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import pygame

from game_callback import GameCallback, SceneId
from scene_finish import SceneFinish
from scene_intro import SceneIntro
from scene_nolwenn import SceneNolwenn, GameScene
from scene_quentin import SceneQuentin
from scene_start import SceneStart
from scene_test import SceneTest
import os


class Game(GameCallback):

    TITLE = "PyGame Test"
    WIDTH = 800
    RATIO = 16.0 / 9.0
    TICK = 40

    def __init__(self):
        pygame.display.set_caption(self.TITLE)
        self._run = True
        self._screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self._scene = None
        self._scene_id = None
        self.set_scene_id(SceneId.INTRO)
        self._image = pygame.image.load(os.path.join('./resources/images/', 'background.png'))
        self._image = pygame.transform.scale(self._image, (int(self.WIDTH), int(self.HEIGHT)))
        pygame.mixer.init()

    def loop(self):
        while self._run:
            pygame.time.delay(self.TICK)
            self.manage_events()

            self._screen.blit(self._image, pygame.Vector2(0.0, 0.0))

            if self._scene_id is not None:
                self._set_scene()

            if self._scene is not None:
                self._scene.update()
                self._scene.draw()
            pygame.display.update()

    def manage_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()

            keys = pygame.key.get_pressed()

            if keys[pygame.K_ESCAPE]:
                self.quit()

            if self._scene is not None:
                self._scene.manage_events(event)

    def quit(self):
        self._run = False

    def set_scene_id(self, scene_id: SceneId):
        self._scene_id = scene_id

    def _set_scene(self):
        if self._scene_id == SceneId.TEST:
            self._scene = SceneTest(self, self._screen)
        elif self._scene_id == SceneId.NOLWENN:
            self._scene = SceneNolwenn(self, self._screen)
        elif self._scene_id == SceneId.QUENTIN:
            self._scene = SceneQuentin(self, self._screen)
        elif self._scene_id == SceneId.START:
            self._scene = SceneStart(self, self._screen)
        elif self._scene_id == SceneId.FINISH:
            self._scene = SceneFinish(self, self._screen)
        elif self._scene_id == SceneId.FINAL:
            self._scene = GameScene(self, self._screen)
        elif self._scene_id == SceneId.INTRO:
            self._scene = SceneIntro(self, self._screen)
        self._scene_id = None

    @property
    def HEIGHT(self):
        return int(Game.WIDTH / Game.RATIO)


if __name__ == "__main__":
    pygame.init()
    game = Game()
    game.loop()
    pygame.quit()
