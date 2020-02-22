from typing import List

from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsPixmapItem, QGraphicsItem

from scene_callback import SceneCallback


class Item:

    def __init__(self, scene: SceneCallback, x: float, y: float):
        self._scene = scene
        w = self._scene.width
        self._x, self._y = x*w, y*w
        self._graphic_item = None

    @property
    def graphic_items(self) -> List[QGraphicsItem]:
        return [self._graphic_item]


class Image(Item):

    def __init__(self,
                 scene: SceneCallback,
                 x: float,
                 y: float,
                 width: float,
                 height: float = None,
                 img: str = None):
        super().__init__(scene, x, y)

        w = scene.width
        width *= w
        if height is not None:
            height *= w

        image = None
        if img is not None:
            image = QImage(img)
            if height is None:
                image = image.scaledToWidth(width)
                height = image.height()
            else:
                image = image.scaled(width, height)

        if height is None:
            height = width

        self._rect = QRectF(self._x - width / 2.0, self._y - height / 2.0, width / 2.0, height / 2.0)

        if image is not None:
            self._graphic_item = QGraphicsPixmapItem()
            self._graphic_item.setPos(self._rect.topLeft())
            self._graphic_item.setPixmap(QPixmap.fromImage(image))
        else:
            self._graphic_item = QGraphicsRectItem(self._rect)


class DynamicItem(Item):

    def __init__(self, scene: SceneCallback, x: float, y: float):
        super().__init__(scene, x, y)

    def update(self):
        raise NotImplementedError


class CompositeItem(Item):

    def __init__(self, scene: SceneCallback, x: float, y: float):
        super().__init__(scene, x, y)
        self._items = []

    @property
    def graphic_items(self) -> List[QGraphicsItem]:
        r = []
        for item in self._items:
            r += item.graphic_items
        return r


