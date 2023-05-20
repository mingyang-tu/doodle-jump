import pygame
from typing import Any, Union
from ..constants import *
from ..keys import *


class Doodle(pygame.sprite.Sprite):
    def __init__(self, assets: dict[str, pygame.Surface]):
        pygame.sprite.Sprite.__init__(self)
        self.assets = assets
        self.images = [assets["doodle"], pygame.transform.flip(assets["doodle"], True, False)]
        self.imgs_shoot = [assets["doodle_shoot"], pygame.transform.flip(assets["doodle_shoot"], True, False)]
        self.imgs_dead = [pygame.transform.flip(assets["doodle"], False, True),
                          pygame.transform.flip(assets["doodle"], True, True)]

        self.rect = self.images[0].get_rect()
        self.layer = 10

        self.radius = self.rect.height // 2

        self.rect.center = (HALF_WIDTH, HEIGHT*2//3)

        self.speed_x = MOV_SPEED
        self.speed_y = 0

        self.acce_y = GRAVITY
        self.jump_speed = -JUMP_SPEED

        self.direction = 0

        self.shoot_time = 0
        self.shooting = False

        self.dead = False

    def update(self):
        now = pygame.time.get_ticks()
        if self.shooting and now - self.shoot_time > SHOOT_TIME:
            shift = SHOOT_SHIFT if self.direction == 0 else -SHOOT_SHIFT
            self.relocate(self.images[self.direction], self.rect.centerx+shift, self.rect.bottom)
            self.shooting = False
        key_pressed = pygame.key.get_pressed()

        if key_pressed[K_RIGHT]:
            self.direction = 0
            self.rect.x += self.speed_x
        if key_pressed[K_LEFT]:
            self.direction = 1
            self.rect.x -= self.speed_x

        self.speed_y += self.acce_y
        self.rect.y += round(self.speed_y)

        if self.rect.centerx < 0:
            self.rect.centerx = WIDTH
        if self.rect.centerx > WIDTH:
            self.rect.centerx = 0

    def draw(self, screen: pygame.Surface):
        if self.dead:
            screen.blit(self.imgs_dead[self.direction], self.rect)
        elif self.shooting:
            screen.blit(self.imgs_shoot[self.direction], self.rect)
        else:
            screen.blit(self.images[self.direction], self.rect)

    def jump(self):
        self.speed_y = self.jump_speed

    def jump_spring(self):
        self.speed_y = self.jump_speed * 1.5

    def shoot(self, img_bullet: pygame.Surface, sprites: list[Union[pygame.sprite.Group, Any]]):
        if not self.shooting:
            shift = SHOOT_SHIFT if self.direction == 0 else -SHOOT_SHIFT
            self.relocate(self.imgs_shoot[self.direction], self.rect.centerx-shift, self.rect.bottom)

        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top)
        for sprite in sprites:
            sprite.add(bullet)

        self.shoot_time = pygame.time.get_ticks()
        self.shooting = True

    def touch_monster(self):
        self.dead = True
        self.speed_y = 0

    def relocate(self, image: pygame.Surface, x: int, y: int):
        self.rect = image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y


class Bullet(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y

        self.layer = 9

        self.radius = self.rect.height // 2

        self.speed_y = -BULLET_SPEED

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0:
            self.kill()
