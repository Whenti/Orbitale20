from item import Item, DynamicItem, CompositeItem
from scene_callback import SceneCallback


class ItemTest(Item, DynamicItem, CompositeItem):

    def __init__(self, scene: SceneCallback, x: float, y: float):
        super(self, Item).__init__(scene)