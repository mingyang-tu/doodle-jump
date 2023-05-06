import pygame
import random
from ..constants import *


class Platform(pygame.sprite.Sprite):
    def __init__(self, image, y_range, type):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.type = type

        self.rect = self.image.get_rect()

        self.rect.centerx = random.randrange(0, WIDTH)
        self.rect.centery = random.randrange(*y_range)

        SPEEDS = list(range(-5, -1)) + list(range(2, 6))
        self.speed_x = random.choice(SPEEDS)

    def update(self):
        if self.type == "blue":
            self.rect.x += self.speed_x
            if self.rect.right < 0:
                self.rect.left = WIDTH
            if self.rect.left > WIDTH:
                self.rect.right = 0
        if self.rect.top > HEIGHT:
            self.kill()
