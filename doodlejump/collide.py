import pygame


def jump_platform(doodle, platform_sprites):
    if doodle.speed_y > 0:
        hits = pygame.sprite.spritecollide(doodle, platform_sprites, False)
        if hits:
            doodle.jump()
