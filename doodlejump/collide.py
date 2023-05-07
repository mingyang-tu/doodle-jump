import pygame
from .constants import *


def jump_platform(doodle, platform_sprites):
    if doodle.speed_y > 0:
        hits = pygame.sprite.spritecollide(doodle, platform_sprites, False)
        for hit in hits:
            if doodle.rect.centery < hit.rect.top:
                doodle.jump()
                return
