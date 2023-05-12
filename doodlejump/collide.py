import pygame
from .constants import *
from .sprites.doodle import Doodle


def jump_platform(doodle: Doodle, platform_sprites: pygame.sprite.Group):
    if doodle.speed_y > 0:
        hits = pygame.sprite.spritecollide(doodle, platform_sprites, False)
        for hit in hits:
            if doodle.rect.bottom < hit.rect.bottom:
                if hit.layer == 0:
                    doodle.jump_spring()
                    hit.relocate(hit.uncompressed)
                elif hit.layer == 1:
                    doodle.jump()
                return
