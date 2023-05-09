import pygame
import os
from .constants import *
from .sprites.doodle import Doodle
from .generate import (
    generate_platform,
    generate_init_platform,
    draw_text,
    game_over,
    menu
)
from .collide import jump_platform


def load_assets(assets_root):
    assets = dict()
    assets["background"] = pygame.image.load(os.path.join(assets_root, "background.png")).convert()
    assets["green_pf"] = pygame.image.load(os.path.join(assets_root, "platforms", "green.png")).convert_alpha()
    assets["blue_pf"] = pygame.image.load(os.path.join(assets_root, "platforms", "blue.png")).convert_alpha()
    assets["doodle"] = pygame.image.load(os.path.join(assets_root, "doodle.png")).convert_alpha()
    assets["button"] = pygame.image.load(os.path.join(assets_root, "buttons", "button.png")).convert_alpha()
    assets["selected_button"] = pygame.image.load(os.path.join(assets_root, "buttons", "selected_button.png")).convert_alpha()

    assets["font"] = os.path.join(assets_root, "Gochi_Hand", "GochiHand-Regular.ttf")

    return assets


def init_game(assets):
    all_sprites = pygame.sprite.LayeredUpdates()
    platform_sprites = pygame.sprite.Group()

    doodle = Doodle(assets["doodle"])
    all_sprites.add(doodle)

    generate_init_platform(assets, [all_sprites, platform_sprites], HEIGHT-50)
    generate_platform(assets, [all_sprites, platform_sprites], [HEIGHT-100, -STAGE_LENGTH-BUFFER_LENGTH], 1)

    camera_move = 0
    stage = 1
    score = 0
    running = True
    gameover = False
    showmenu = False

    return (
        all_sprites, platform_sprites,
        doodle,
        camera_move, stage, score,
        running, gameover, showmenu
    )


def start_game(assets_root="./doodlejump/assets/"):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Doodle Jump")
    clock = pygame.time.Clock()

    assets = load_assets(assets_root)

    (
        all_sprites, platform_sprites,
        doodle,
        camera_move, stage, score,
        running, gameover, showmenu
    ) = init_game(assets)

    showmenu = True

    while running:
        if gameover:
            close = game_over(screen, clock, assets, all_sprites, doodle, score)
            gameover = False
            if close == 0:
                (
                    all_sprites, platform_sprites,
                    doodle,
                    camera_move, stage, score,
                    running, gameover, showmenu
                ) = init_game(assets)
            elif close == 1:
                showmenu = True
            elif close == -1 or close == 2:
                break
            else:
                raise ValueError("Unexpected value of [close]")

        if showmenu:
            close = menu(screen, clock, assets)
            if close == 0:
                (
                    all_sprites, platform_sprites,
                    doodle,
                    camera_move, stage, score,
                    running, gameover, showmenu
                ) = init_game(assets)
            elif close == -1 or close == 1:
                break
            else:
                raise ValueError("Unexpected value of [close]")

        clock.tick(FPS)

    # get inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    # update game
        all_sprites.update()
        jump_platform(doodle, platform_sprites)

        # move camera
        if doodle.rect.y < HALF_HEIGHT:
            diff = HALF_HEIGHT - doodle.rect.y
            camera_move += diff
            score += diff
            for sprite in all_sprites:
                sprite.rect.y += diff
            if camera_move > STAGE_LENGTH:
                stage += 1
                generate_platform(
                    assets,
                    [all_sprites, platform_sprites],
                    [camera_move-STAGE_LENGTH-BUFFER_LENGTH, camera_move-STAGE_LENGTH*2-BUFFER_LENGTH],
                    stage
                )
                camera_move = 0

        if doodle.rect.y > HEIGHT:
            gameover = True

    # display
        screen.blit(assets["background"], (0, 0))
        all_sprites.draw(screen)
        draw_text(screen, assets["font"], str(score), 32, BLACK, 10, 0)
        pygame.display.update()

    pygame.quit()
