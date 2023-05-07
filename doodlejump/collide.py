import pygame
from .constants import *


def jump_platform(doodle, platform_sprites):
    if doodle.speed_y > JUMP_THRESHOLD:
        hits = pygame.sprite.spritecollide(doodle, platform_sprites, False)
        if hits:
            doodle.jump()
