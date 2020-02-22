#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import pygame
from pygame.event import Event

from game_callback import GameCallback
from item import Item


class Scene:
    def __init__(self, game_callback: GameCallback, screen: pygame.Surface):
        self._game_callback = game_callback
        self._screen = screen
        self._items = []

    def _add_item(self, item: Item):
        self._items.append(item)

    def _remove_item(self, item: Item):
        self._items.remove(item)

    def manage_events(self, event: Event):
        pass

    def update(self):
        for item in self._items:
            item.update()

    def draw(self):
        sorted_items = sorted(self._items, key=lambda item_: item_.z_value)
        for item in sorted_items:
            item.draw()


class CompositeScene(Scene):
    def __init__(self, game_callback: GameCallback, screen: pygame.Surface):
        super().__init__(game_callback, screen)
        self._scenes = []

    def _add_scene(self, scene: Scene):
        self._scenes.append(scene)

    def _remove_scene(self, scene: Scene):
        self._scenes.remove(scene)

    def manage_events(self, event: Event):
        for scene in self._scenes:
            scene.manage_events(event)

    def update(self):
        for scene in self._scenes:
            scene.update()

    def draw(self):
        for scene in self._scenes:
            scene.draw()
