import pygame
import os
from .constants import *
from .sprites import Doodle
from .generate import generate_platform
from .collide import jump_platform


def load_assets(assets_root):
    assets = dict()
    assets["background"] = pygame.image.load(os.path.join(assets_root, "background.png")).convert()
    assets["green_pf"] = pygame.image.load(os.path.join(assets_root, "platforms", "green.png")).convert_alpha()
    assets["blue_pf"] = pygame.image.load(os.path.join(assets_root, "platforms", "blue.png")).convert_alpha()
    assets["doodle"] = pygame.image.load(os.path.join(assets_root, "doodle.png")).convert_alpha()

    return assets


def start_game(assets_root="./doodlejump/assets/"):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Doodle Jump")
    clock = pygame.time.Clock()

    assets = load_assets(assets_root)

    all_sprites = pygame.sprite.LayeredUpdates()
    platform_sprites = pygame.sprite.Group()

    doodle = Doodle(assets["doodle"])
    all_sprites.add(doodle)

    generate_platform(assets, all_sprites, platform_sprites)

    running = True

    while running:
        clock.tick(FPS)
        # 取得輸入
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 更新遊戲
        all_sprites.update()
        jump_platform(doodle, platform_sprites)

        # 畫面顯示
        screen.blit(assets["background"], (0, 0))
        all_sprites.draw(screen)
        pygame.display.update()


pygame.quit()
