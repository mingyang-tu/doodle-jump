import pygame
import os
from .constants import *
from .sprites import Doodle
from .generate import generate_platform, generate_init_platform
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

    generate_init_platform(assets, [all_sprites, platform_sprites])
    generate_platform(assets, [all_sprites, platform_sprites], [500, -1100], 1)

    camera_move = 0
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

        if doodle.rect.y < HALF_HEIGHT:
            diff = (HALF_HEIGHT - doodle.rect.y) // 30 + 1
            camera_move += diff
            for sprite in all_sprites:
                sprite.rect.y += diff
            if camera_move > 1000:
                generate_platform(assets, [all_sprites, platform_sprites], [camera_move-1200, camera_move-2100])
                camera_move = 0

        # 畫面顯示
        screen.blit(assets["background"], (0, 0))
        all_sprites.draw(screen)
        pygame.display.update()


pygame.quit()
