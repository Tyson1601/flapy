import random
from typing import List

from ..utils import GameConfig
from .entity import Entity

BASE_PIPE_GAP = 120   # gap gốc ở 512px chiều cao
BASE_VEL_X = -5      # tốc độ pipe gốc


class Pipe(Entity):
    def __init__(self, *args, vel_x=BASE_VEL_X, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.vel_x = vel_x

    def draw(self) -> None:
        self.x += self.vel_x
        super().draw()


class Pipes(Entity):
    upper: List[Pipe]
    lower: List[Pipe]

    def __init__(self, config: GameConfig) -> None:
        super().__init__(config)
        # Scale pipe_gap và vel_x theo chiều cao màn hình
        scale = config.window.height / 512
        self.pipe_gap = int(BASE_PIPE_GAP * scale)
        self.pipe_vel_x = int(BASE_VEL_X * scale)
        self.top = 0
        self.bottom = self.config.window.viewport_height
        self.upper = []
        self.lower = []
        self.spawn_initial_pipes()

    def tick(self) -> None:
        if self.can_spawn_pipes():
            self.spawn_new_pipes()
        self.remove_old_pipes()

        for up_pipe, low_pipe in zip(self.upper, self.lower):
            up_pipe.tick()
            low_pipe.tick()

    def stop(self) -> None:
        for pipe in self.upper + self.lower:
            pipe.vel_x = 0

    def can_spawn_pipes(self) -> bool:
        last = self.upper[-1]
        if not last:
            return True
        return self.config.window.width - (last.x + last.w) > last.w * 2.5

    def spawn_new_pipes(self):
        upper, lower = self.make_random_pipes()
        self.upper.append(upper)
        self.lower.append(lower)

    def remove_old_pipes(self):
        for pipe in self.upper:
            if pipe.x < -pipe.w:
                self.upper.remove(pipe)
        for pipe in self.lower:
            if pipe.x < -pipe.w:
                self.lower.remove(pipe)

    def spawn_initial_pipes(self):
        upper_1, lower_1 = self.make_random_pipes()
        upper_1.x = self.config.window.width + upper_1.w * 3
        lower_1.x = self.config.window.width + upper_1.w * 3
        self.upper.append(upper_1)
        self.lower.append(lower_1)

        upper_2, lower_2 = self.make_random_pipes()
        upper_2.x = upper_1.x + upper_1.w * 3.5
        lower_2.x = upper_1.x + upper_1.w * 3.5
        self.upper.append(upper_2)
        self.lower.append(lower_2)

    def make_random_pipes(self):
        """returns a randomly generated pipe"""
        base_y = self.config.window.viewport_height

        gap_y = random.randrange(0, int(base_y * 0.6 - self.pipe_gap))
        gap_y += int(base_y * 0.2)
        pipe_height = self.config.images.pipe[0].get_height()
        pipe_x = self.config.window.width + 10

        upper_pipe = Pipe(
            self.config,
            self.config.images.pipe[0],
            pipe_x,
            gap_y - pipe_height,
            vel_x=self.pipe_vel_x,
        )

        lower_pipe = Pipe(
            self.config,
            self.config.images.pipe[1],
            pipe_x,
            gap_y + self.pipe_gap,
            vel_x=self.pipe_vel_x,
        )

        return upper_pipe, lower_pipe
