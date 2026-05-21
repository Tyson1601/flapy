from ..utils import GameConfig
from .entity import Entity


class Floor(Entity):
    def __init__(self, config: GameConfig) -> None:
        super().__init__(config, config.images.base, 0, config.window.vh)
        self.vel_x = int(4 * config.window.height / 512)
        # x_extra: khoảng dư để scroll, tính theo ảnh base gốc
        self.x_extra = max(self.w - config.window.w, self.w)

    def stop(self) -> None:
        self.vel_x = 0

    def draw(self) -> None:
        # Scroll offset
        self.x = -((-self.x + self.vel_x) % self.x_extra)
        # Tile floor theo chiều ngang
        x = self.x
        while x < self.config.window.width:
            self.config.screen.blit(self.image, (x, self.y))
            x += self.w
