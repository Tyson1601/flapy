import pygame

from ..utils import GameConfig
from .entity import Entity


class Background(Entity):
    def __init__(self, config: GameConfig) -> None:
        super().__init__(config, config.images.background, 0, 0)

    def draw(self) -> None:
        """Tile background theo chiều ngang nếu màn hình rộng hơn ảnh."""
        img_w = self.image.get_width()
        screen_w = self.config.window.width
        x = 0
        while x < screen_w:
            self.config.screen.blit(self.image, (x, 0))
            x += img_w
