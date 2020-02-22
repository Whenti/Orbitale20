#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from enum import Enum

import pygame
import math

from pygame.event import Event
from pygame import Vector2
from game_callback import GameCallback
from scene import Scene


from camera import Camera
from item import CompositeItem, Item, ImageItem


class PlayerAnimation(Enum):
    NONE = 0
    RUN = 1
    JUMP = 2
    REST = 3



class Player(CompositeItem):
    def __init__(self, camera: Camera, pos: Vector2):
        super().__init__(camera, pos, Vector2(0.15, 0.15))

        self._power = 4
        self._T = None
        self._t = 0
        self._BASE_BODY_SIZE = Vector2(0.06, 0.08)
        self._BASE_ARM_SIZE = Vector2(0.07, 0.1)
        self._BASE_LEG_SIZE = Vector2(0.07, 0.13)

        self._max_leg_rotation = 40
        self._max_arm_rotation = 40

        # ----------- initial body shape -------------
        self._muscle_level = 0
        self._image_body = 'body_m.png'
        self._image_right_arm = 'right_arm_w.png'
        self._image_left_arm = 'left_arm_w.png'
        self._image_left_leg = 'left_leg.png'
        self._image_right_leg = 'right_leg.png'

        # ----------- jump management ---------------
        self._z = 0
        self._ground = self.pos.y
        self._v_speed = 0.0

        color = (100, 100, 100)

        self._body = ImageItem(camera, Vector2(0, 0), self._BASE_BODY_SIZE, image=self._image_body)
        self._add_item(self._body)

        self._left_leg = ImageItem(camera,
                                   self._compute_leg_position(False),
                                   self._BASE_LEG_SIZE,
                                   image=self._image_left_leg)
        self._add_item(self._left_leg)

        self._right_leg = ImageItem(camera,
                                    self._compute_leg_position(True),
                                    self._BASE_LEG_SIZE,
                                    image=self._image_right_leg)
        self._add_item(self._right_leg)

        self._right_arm = ImageItem(camera,
                                    self._compute_arm_position(True),
                                    self._BASE_ARM_SIZE,
                                    image=self._image_right_arm)
        self._add_item(self._right_arm)

        self._left_arm = ImageItem(camera,
                                   self._compute_arm_position(False),
                                   self._BASE_ARM_SIZE,
                                   image=self._image_left_arm)
        self._add_item(self._left_arm)

        self._set_animation(PlayerAnimation.RUN)
        self._right = False
        self._left = False
        self._up = False
        self._speed = Vector2(0, 0)


    def _compute_leg_position(self, right):
        y = self._BASE_BODY_SIZE.y * 0.5
        x = self._BASE_BODY_SIZE.x * 0.2
        if right:
            x *= -1
        return Vector2(x, y)

    def _compute_arm_position(self, right):
        y = self._BASE_BODY_SIZE.y * (- 0.2)
        x = self._BASE_BODY_SIZE.x * 0.3
        if right:
            x *= -1
        return Vector2(x, y)

    def _set_animation(self, animation):
        self._t = 0
        self._animation = animation
        if self._animation == PlayerAnimation.RUN:
            self._max_leg_rotation = 40
            self._T = 25
        elif self._animation == PlayerAnimation.JUMP:
            self._max_leg_rotation = 60
            self._t = 10
        elif self._animation == PlayerAnimation.REST:
            self._t = 5


    def draw(self):
        for item in [self._left_leg, self._left_arm, self._body, self._right_leg, self._right_arm]:
            item.draw()

    def update(self, parent: Item = None):
        self._t += 1
        if self._t == self._T:
            self._t = 0

        # ----------- move ---------------
        factor_speed = 7-self._power
        if self._right and not self._left:
            self._speed = Vector2(1, 0)*factor_speed
        elif self._left and not self._right:
            self._speed = Vector2(-1, 0)*factor_speed
        else:
            self._speed *= 0.9
            if self._speed.length() < 0.001:
                self._speed = Vector2(0, 0)
            self._set_animation(PlayerAnimation.REST)

        if self._z > 0:
            self._v_speed -= 0.09

        # ----------- jump ---------------
        if self._up and self._z <= 0:
            factor_jump_height = 5-self._power
            self._v_speed = 1.0 * factor_jump_height
            self._set_animation(PlayerAnimation.JUMP)

        self._z += self._v_speed * 0.005

        # ---------- lay down ------------
        if self._z < 0:
            self._z = 0
            self._v_speed = 0
            self._set_animation(PlayerAnimation.RUN)

        self.set_pos(Vector2(self.pos.x + self._speed.x * 0.01, self._ground - self._z))

        lambda_ = self._t/self._T

        self._left_arm.set_rotation(self._max_arm_rotation * math.cos(lambda_ * 2 * math.pi))
        self._right_arm.set_rotation(-self._max_arm_rotation * math.cos(lambda_ * 2 * math.pi))

        self._left_leg.set_rotation(-self._max_leg_rotation * math.cos(lambda_ * 2 * math.pi))
        self._right_leg.set_rotation(self._max_leg_rotation * math.cos(lambda_ * 2 * math.pi))

        self.update_body_size()

        super().update()

    def set_right(self, right):
        self._right = right

    def set_left(self, left):
        self._left = left

    def set_up(self, up):
        self._up = up

    def update_body_size(self):
        factor = self._power

        # thresholds
        muscle_level_m = 5
        muscle_level_s = 8

        # muscle level - update images
        if self._power > muscle_level_s:
            new_muscle_level = 2
        elif self._power > muscle_level_m:
            new_muscle_level = 1
        else:
            new_muscle_level = 0

        if new_muscle_level != self._muscle_level:
            # right_arm
            right_arms = ['right_arm_w.png', 'right_arm_m.png', 'right_arm_s.png']
            self._right_arm.load_image(right_arms[new_muscle_level])
            # left_arm
            left_arms = ['left_arm_w.png', 'left_arm_m.png', 'left_arm_s.png']
            self._left_arm.load_image(left_arms[new_muscle_level])
            # body
            bodies = ['body_w.png', 'body_m.png', 'body_s.png']
            self._body.load_image(bodies[new_muscle_level])

            self._muscle_level = new_muscle_level


        # body size
        body_size = self._BASE_BODY_SIZE * factor
        arm_size = self._BASE_ARM_SIZE * factor
        leg_size = self._BASE_LEG_SIZE





class SceneQuentin(Scene):
    def __init__(self, game_callback: GameCallback, screen: pygame.Surface):
        super().__init__(game_callback, screen)
        self._camera = Camera(self._screen)
        self._player = Player(self._camera, Vector2(0, 0))
        self._player.set_z_value(10)
        self._add_item(self._player)

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
