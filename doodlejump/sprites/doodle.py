import pygame
from ..constants import *


class Doodle(pygame.sprite.Sprite):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.images = [image, pygame.transform.flip(image, True, False)]

        self.image = self.images[0]

        self.rect = self.image.get_rect()
        self.layer = 10

        self.rect.center = (WIDTH // 2, HEIGHT // 2)

        self.speed_x = MOV_SPEED
        self.speed_y = 0

        self.acce_y = GRAVITY
        self.jump_speed = -JUMP_SPEED

        self.direction = 0

    def update(self):
        key_pressed = pygame.key.get_pressed()

        if key_pressed[pygame.K_RIGHT]:
            self.flip_lr(0)
            self.rect.x += self.speed_x
        if key_pressed[pygame.K_LEFT]:
            self.flip_lr(1)
            self.rect.x -= self.speed_x

        self.speed_y += self.acce_y
        self.rect.y += self.speed_y

        if self.rect.right < 0:
            self.rect.left = WIDTH
        if self.rect.left > WIDTH:
            self.rect.right = 0

        if self.rect.bottom >= HEIGHT:
            self.jump()

    def jump(self):
        self.speed_y = self.jump_speed

    def flip_lr(self, flip_direction):
        if flip_direction != self.direction:
            self.direction = flip_direction
            self.image = self.images[self.direction]
