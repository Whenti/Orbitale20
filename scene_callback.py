from typing import Tuple


class SceneCallback:

    @property
    def width(self) -> float:
        raise NotImplementedError

    @property
    def ratio(self) -> float:
        raise NotImplementedError
