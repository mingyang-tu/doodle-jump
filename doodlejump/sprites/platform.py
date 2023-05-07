import pygame
import random
from ..constants import *


class Platform(pygame.sprite.Sprite):
    def __init__(self, image, y_range, type):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.type = type

        self.rect = self.image.get_rect()
        self.layer = 0

        self.rect.centerx = random.randrange(0, WIDTH)
        self.rect.centery = random.randrange(*y_range)

        if random.random() >= 0.5:
            self.speed_x = BLUE_SPEED
        else:
            self.speed_x = -BLUE_SPEED

    def update(self):
        if self.type == "blue":
            self.rect.x += self.speed_x
            if self.rect.left <= 0:
                self.speed_x = BLUE_SPEED
            elif self.rect.right >= WIDTH:
                self.speed_x = -BLUE_SPEED
                
        if self.rect.top > HEIGHT:
            self.kill()
