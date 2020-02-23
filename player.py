from enum import Enum

from pygame import Vector2
import math

from camera import Camera
from item import CompositeItem, ImageItem, Item


class PlayerAnimation(Enum):
    NONE = 0
    RUN = 1
    JUMP = 2
    REST = 3
    MOVE_HEAVY_OBJECT = 4
    WIN = 5



class Player(CompositeItem):
    def __init__(self, camera: Camera, pos: Vector2):
        super().__init__(camera, pos, Vector2(0.15, 0.15))

        self._height_delta = 0.0
        self._power = 1
        self._T = None
        self._t = 0
        self._BASE_BODY_SIZE = Vector2(0.06, 0.15)
        self._BASE_HEAD_SIZE = Vector2(0.08, 0.1)
        self._BASE_ARM_SIZE = Vector2(0.07, 0.15)
        self._BASE_LEG_SIZE = Vector2(0.1, 0.2)

        self._max_leg_rotation = 50
        self._max_arm_rotation = 60

        # ----------- initial body shape -------------
        self._muscle_level = 0
        self._image_body = 'body_w.png'
        self._image_right_arm = 'right_arm_w.png'
        self._image_left_arm = 'left_arm_w.png'
        self._image_left_leg = 'left_leg.png'
        self._image_right_leg = 'right_leg.png'
        self._image_head = 'head.png'

        # ----------- jump management ---------------
        self._z = 0
        self._ground = self.pos.y
        self._v_speed = 0.0

        color = (100, 100, 100)

        self._body = ImageItem(camera, Vector2(0, 0), self._BASE_BODY_SIZE, image=self._image_body)
        self._add_item(self._body)

        self._head = ImageItem(camera,
                               self._compute_head_position(),
                               self._BASE_HEAD_SIZE,
                               image=self._image_head)
        self._add_item(self._head)

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
        self._animation = None
        self._set_animation(PlayerAnimation.RUN)
        self._right = False
        self._left = False
        self._up = False
        self._speed = Vector2(0, 0)
        self._attacking_object = None

    def _compute_head_position(self):
        y = -(self._BASE_BODY_SIZE.y + self._BASE_HEAD_SIZE.y) * 0.2
        x = self._BASE_BODY_SIZE.x * 0.1

        return Vector2(x, y)

    def stop(self):
        self._speed = Vector2(0, 0)

    def _compute_leg_position(self, right):
        y = self._BASE_BODY_SIZE.y * 0.25
        x = self._BASE_BODY_SIZE.x * 0.1
        if right:
            x *= -1
        else:
            x += 0.015
        return Vector2(x, y)

    def _compute_arm_position(self, right):
        y = self._BASE_BODY_SIZE.y * (- 0.2)
        x = self._BASE_BODY_SIZE.x * 0.3
        if right:
            x *= -1
        return Vector2(x, y)

    def _set_animation(self, animation):
        if self._animation == PlayerAnimation.WIN:
            return
        if animation == self._animation:
            return
        print(animation)
        self._t = 0
        self._animation = animation
        if self._animation == PlayerAnimation.RUN:
            self._max_leg_rotation = 40
            self._T = 10
        elif self._animation == PlayerAnimation.JUMP:
            self._max_leg_rotation = 60
            self._t = 10
            self._T = 8
        elif self._animation == PlayerAnimation.REST:
            self._t = 5
            self._T = 8
        elif self._animation == PlayerAnimation.MOVE_HEAVY_OBJECT:
            self._T = 100
        elif self._animation == PlayerAnimation.WIN:
            self._max_leg_rotation = 40
            self._T = 10

    def draw(self):
        for item in [self._left_arm, self._left_leg,  self._body, self._head, self._right_leg, self._right_arm]:
            item.draw()

    def gain_power(self):
        protein_power = 5
        if self._power > 5:
            self._power = 10
        else:
            self._power += protein_power

    def loose_power(self):
        power_lost = 0.05
        self._power -= power_lost
        if self._power < 1:
            self._power = 1

    def update(self, parent: Item = None):
        self._t += 1
        if self._t == self._T:
            self._t = 0

        # ----------- move ---------------

        if not self._attacking_object:
            factor_speed = (2 + 7 / self._power) * 0.3
            if self._right and not self._left:
                if self._animation != PlayerAnimation.RUN and self._z <= 0:
                    self._set_animation(PlayerAnimation.RUN)
                    self._speed = Vector2(1, 0) * factor_speed
            elif self._left and not self._right and self._z <= 0:
                if self._animation != PlayerAnimation.RUN:
                    self._set_animation(PlayerAnimation.RUN)
                self._speed = Vector2(-1, 0) * factor_speed
            else:
                self._speed *= 0.6
                if self._speed.length() < 0.001:
                    self._speed = Vector2(0, 0)
                if self._z <= 0:
                    self._set_animation(PlayerAnimation.REST)

            if self._z > 0:
                self._v_speed -= 0.35

            # ----------- jump ---------------
            if self._up and self._z <= 0:
                factor_jump_height = 1 + 1.7 / self._power
                self._v_speed = 0.5 * factor_jump_height
                self._set_animation(PlayerAnimation.JUMP)

        else:
            self._attacking_object.life -= 2 + self._power
            if self._attacking_object.life < 0:
                self._attacking_object.fly()
                self._attacking_object = None

        self._z += self._v_speed * 0.05

        # ---------- lay down ------------
        if self._z < 0:
            self._z = 0
            self._v_speed = 0
            if (self._right and not self._left) or (not self._right and self._left):
                self._set_animation(PlayerAnimation.RUN)
            else:
                self._set_animation(PlayerAnimation.REST)

        self.set_pos(Vector2(self.pos.x + self._speed.x * 0.01, self._ground - self._z + self._height_delta))

        # ------------ decreasing power with time ---------------
        if self._animation != PlayerAnimation.WIN:
            self.loose_power()

        # ------------------------ arm synchronisation -----------------------

        self.update_body_members_size()
        self._height_delta = 0
        if self._animation == PlayerAnimation.REST:
            for part in [self._right_leg, self._left_leg, self._right_arm, self._left_arm]:
                part.set_rotation(0)

        elif self._animation == PlayerAnimation.RUN:
            lambda_ = self._t / self._T
            self._left_arm.set_rotation(self._max_arm_rotation * math.cos(lambda_ * 2 * math.pi))
            self._right_arm.set_rotation(-self._max_arm_rotation * math.cos(lambda_ * 2 * math.pi))
            self._left_leg.set_rotation(-self._max_leg_rotation * math.cos(lambda_ * 2 * math.pi))
            self._right_leg.set_rotation(self._max_leg_rotation * math.cos(lambda_ * 2 * math.pi))
            self._height_delta = 0.005 * math.cos(lambda_ * 2 * math.pi)

        elif self._animation == PlayerAnimation.MOVE_HEAVY_OBJECT:
            if self._attacking_object is not None:
                self._t = 100 - (self._attacking_object.life/self._attacking_object.max_life * 100)
            else:
                self._t = 100
            lambda_ = self._t / self._T
            if lambda_ < 0.5:
                self._left_arm.set_rotation(- 30)
                self._right_arm.set_rotation(- 30)
            else:
                self._left_arm.set_rotation(self._max_arm_rotation * 3 * 2 * (lambda_ - 0.5) - 30)
                self._right_arm.set_rotation(self._max_arm_rotation * 3 * 2 * (lambda_ - 0.5) - 30)

        elif self._animation == PlayerAnimation.JUMP:
            self._left_arm.set_rotation(90)
            self._right_arm.set_rotation(-90)
            self._left_leg.set_rotation(-90)
            self._right_leg.set_rotation(90)

        elif self._animation == PlayerAnimation.WIN:
            lambda_ = self._t / self._T
            self._left_arm.set_rotation(140)
            self._right_arm.set_rotation(140)
            self._left_leg.set_rotation(-self._max_leg_rotation * math.cos(lambda_ * 2 * math.pi))
            self._right_leg.set_rotation(self._max_leg_rotation * math.cos(lambda_ * 2 * math.pi))

        super().update()

    def set_winner(self):
        self._animation = PlayerAnimation.WIN
        self._power = 10

    def set_right(self, right):
        self._right = right

    def set_left(self, left):
        self._left = left

    def set_up(self, up):
        self._up = up

    def update_body_members_size(self):
        factor_members_size = 0.1*(self._power + 10)

        # body members size
        body_size = self._BASE_BODY_SIZE * factor_members_size
        self._body.set_size(Vector2(body_size.x, self._BASE_BODY_SIZE.y))

        head_size = self._BASE_HEAD_SIZE * factor_members_size
        #self._head.set_size(head_size)

        arm_size = self._BASE_ARM_SIZE * factor_members_size
        self._left_arm.set_size(Vector2(arm_size.x, self._BASE_ARM_SIZE.y))
        self._right_arm.set_size(Vector2(arm_size.x, self._BASE_ARM_SIZE.y))

        leg_size = self._BASE_LEG_SIZE
        self._left_leg.set_size(leg_size)
        self._right_leg.set_size(leg_size)

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

    def attack(self, car):
        if self._attacking_object is None:
            self._attacking_object = car
            car.shaking_status(True)
            self._set_animation(PlayerAnimation.MOVE_HEAVY_OBJECT)

