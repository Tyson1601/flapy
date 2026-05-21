import pygame

from ..utils import GameConfig
from .entity import Entity


class Score(Entity):
    # Lưu high score xuyên suốt các ván chơi (class variable)
    high_score = 0

    def __init__(self, config: GameConfig) -> None:
        super().__init__(config)
        self.y = self.config.window.height * 0.1
        self.score = 0
        # Font để vẽ chữ "BEST" và high score
        font_size = max(18, int(22 * config.window.height / 512))
        self.font = pygame.font.SysFont("Arial", font_size, bold=True)

    def reset(self) -> None:
        # Cập nhật high score trước khi reset
        if self.score > Score.high_score:
            Score.high_score = self.score
        self.score = 0

    def add(self) -> None:
        self.score += 1
        self.config.sounds.point.play()

    @property
    def rect(self) -> pygame.Rect:
        score_digits = [int(x) for x in list(str(self.score))]
        images = [self.config.images.numbers[digit] for digit in score_digits]
        w = sum(image.get_width() for image in images)
        x = (self.config.window.width - w) / 2
        h = max(image.get_height() for image in images)
        return pygame.Rect(x, self.y, w, h)

    def draw(self) -> None:
        # --- Score hiện tại ở giữa màn hình ---
        score_digits = [int(x) for x in list(str(self.score))]
        images = [self.config.images.numbers[digit] for digit in score_digits]
        digits_width = sum(image.get_width() for image in images)
        x_offset = (self.config.window.width - digits_width) / 2

        for image in images:
            self.config.screen.blit(image, (x_offset, self.y))
            x_offset += image.get_width()

        # --- High score ở góc trên phải ---
        padding = int(16 * self.config.window.height / 512)
        best_label = self.font.render("BEST", True, (255, 255, 255))
        best_value = self.font.render(str(Score.high_score), True, (255, 215, 0))  # màu vàng

        # Căn phải
        label_x = self.config.window.width - best_label.get_width() - padding
        value_x = self.config.window.width - best_value.get_width() - padding
        label_y = padding
        value_y = label_y + best_label.get_height() + 2

        # Vẽ bóng chữ để dễ đọc trên mọi nền
        shadow_offset = 2
        shadow_label = self.font.render("BEST", True, (0, 0, 0))
        shadow_value = self.font.render(str(Score.high_score), True, (0, 0, 0))
        self.config.screen.blit(shadow_label, (label_x + shadow_offset, label_y + shadow_offset))
        self.config.screen.blit(shadow_value, (value_x + shadow_offset, value_y + shadow_offset))

        self.config.screen.blit(best_label, (label_x, label_y))
        self.config.screen.blit(best_value, (value_x, value_y))
