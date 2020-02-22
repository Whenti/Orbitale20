import random

from pygame import Vector2

from camera import Camera
from item import CompositeItem, ImageItem


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
            self._add_item(ImageItem(self._camera,
                                      Vector2( (-(1-puzzle_width)/2)+ i * puzzle_width, 0),
                                      Vector2(puzzle_width, puzzle_height),
                                      image=self._puzzle_pieces[rnd]) )


class Protein(ImageItem):
    def __init__(self, camera, pos):
        protein_size = Vector2(0.05, 0.05)
        super().__init__(camera, pos, protein_size, color=(50, 50, 50))
        self.set_z_value(25)

