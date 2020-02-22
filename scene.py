from PyQt5.QtWidgets import QGraphicsScene

from item import Item
from scene_callback import SceneCallback


class Scene(SceneCallback):

    def __init__(self, width: int, height: int):
        self._scene = QGraphicsScene()
        self._scene.setSceneRect(0, 0, width, height)
        self._WIDTH = width
        self._HEIGHT = height
        self._RATIO = self._HEIGHT/self._WIDTH

    def _add_item(self, item: Item):
        for graphic in item.graphic_items:
            self._scene.addItem(graphic)

    @property
    def width(self) -> float:
        return float(self._WIDTH)

    @property
    def ratio(self) -> float:
        return self._RATIO

    @property
    def scene(self):
        return self._scene
