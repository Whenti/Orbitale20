import sys
from enum import Enum

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsView

from scene import Scene
from scene_test import SceneTest


class SceneMode(Enum):
    TEST = 0


class ViewWindow:

    def __init__(self, width: int, height: int, window: QMainWindow):
        super().__init__()
        self._WIDTH = width
        self._HEIGHT = height
        self._x = 0
        self._y = 0

        self._view = QGraphicsView()
        self._view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._view.setFixedSize(self._WIDTH, self._HEIGHT)

        self._window = window
        self._window.setCentralWidget(self._view)
        self._window.setFixedSize(self._WIDTH, self._HEIGHT)
        self._window.show()

        self._scene = None

    def set_scene_mode(self, scene_mode: SceneMode):
        scene = None
        if scene_mode == SceneMode.TEST:
            scene = SceneTest(self._WIDTH, self._HEIGHT)

        if scene is not None:
            self._view.setScene(scene.scene)


if __name__ == "__main__":

    app = QApplication(sys.argv)

    WIDTH = 1200
    HEIGHT = 800

    main_window = QMainWindow()
    view_window = ViewWindow(WIDTH, HEIGHT, main_window)
    view_window.set_scene_mode(SceneMode.TEST)

    app.exec()
