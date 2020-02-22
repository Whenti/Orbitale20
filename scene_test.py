from item import Item, Image
from scene import Scene


class SceneTest(Scene):

    def __init__(self, width: int, height: int):
        super().__init__(width, height)
        self._add_item(Image(self, 0.2, 0.2, 0.1, 0.1, img="test.png"))
