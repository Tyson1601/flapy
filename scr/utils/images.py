import random
from typing import List, Tuple

import pygame

from .constants import BACKGROUNDS, PIPES, PLAYERS


def _scale_image(img: pygame.Surface, scale: float) -> pygame.Surface:
    """Scale một ảnh theo hệ số scale, giữ tỷ lệ gốc."""
    w = int(img.get_width() * scale)
    h = int(img.get_height() * scale)
    return pygame.transform.scale(img, (w, h))


class Images:
    numbers: List[pygame.Surface]
    game_over: pygame.Surface
    welcome_message: pygame.Surface
    base: pygame.Surface
    background: pygame.Surface
    player: Tuple[pygame.Surface]
    pipe: Tuple[pygame.Surface]

    def __init__(self, scale: float = 1.0) -> None:
        self.scale = scale

        self.numbers = [
            _scale_image(
                pygame.image.load(f"assets/sprites/{n}.png").convert_alpha(),
                scale,
            )
            for n in range(10)
        ]

        self.game_over = _scale_image(
            pygame.image.load("assets/sprites/gameover.png").convert_alpha(),
            scale,
        )
        self.welcome_message = _scale_image(
            pygame.image.load("assets/sprites/message.png").convert_alpha(),
            scale,
        )
        self.base = _scale_image(
            pygame.image.load("assets/sprites/base.png").convert_alpha(),
            scale,
        )
        self.randomize()

    def randomize(self):
        rand_bg = random.randint(0, len(BACKGROUNDS) - 1)
        rand_player = random.randint(0, len(PLAYERS) - 1)
        rand_pipe = random.randint(0, len(PIPES) - 1)

        # Background: scale theo chiều cao, chiều ngang sẽ tile nếu cần
        bg_raw = pygame.image.load(BACKGROUNDS[rand_bg]).convert()
        self.background = _scale_image(bg_raw, self.scale)

        self.player = tuple(
            _scale_image(
                pygame.image.load(PLAYERS[rand_player][i]).convert_alpha(),
                self.scale,
            )
            for i in range(3)
        )

        pipe_raw = pygame.image.load(PIPES[rand_pipe]).convert_alpha()
        pipe_scaled = _scale_image(pipe_raw, self.scale)
        self.pipe = (
            pygame.transform.flip(pipe_scaled, False, True),
            pipe_scaled,
        )
