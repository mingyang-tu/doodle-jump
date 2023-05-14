import pygame
import random
from ..constants import *


class Monster(pygame.sprite.Sprite):
    def __init__(self, images: list[pygame.Surface], y_range: tuple[int, int]):
        pygame.sprite.Sprite.__init__(self)
        self.image = random.choice(images)

        self.rect = self.image.get_rect()
        self.layer = 5

        self.radius = self.rect.height // 2

        self.rect.centerx = random.randint(0, WIDTH)
        self.rect.centery = random.randint(*y_range)

        self.speed_x = MONSTER_MAX_SPEED
        self.origin_x = self.rect.x

    def update(self):
        self.speed_x += (self.origin_x - self.rect.x) * MONSTER_ACC_CONST
        self.rect.x += round(self.speed_x)

        if self.rect.top > HEIGHT:
            self.kill()
