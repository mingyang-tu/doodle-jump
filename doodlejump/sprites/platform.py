import pygame
import random
from ..constants import *


class Platform(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, y_range: tuple[int, int], type: str):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.type = type

        self.rect = self.image.get_rect()
        self.layer = 0

        self.rect.centerx = random.randint(0, WIDTH)
        self.rect.centery = random.randint(*y_range)

        if random.random() > 0.95:
            self.blue_speed = random.choice(SPECIAL_BLUE)
        else:
            self.blue_speed = BLUE_SPEED

        if random.random() >= 0.5:
            self.speed_x = self.blue_speed
        else:
            self.speed_x = -self.blue_speed

    def update(self):
        if self.type == "blue":
            self.rect.x += self.speed_x
            if self.rect.left <= 0:
                self.speed_x = self.blue_speed
            elif self.rect.right >= WIDTH:
                self.speed_x = -self.blue_speed

        if self.rect.top > HEIGHT:
            self.kill()
