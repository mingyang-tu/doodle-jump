import pygame
from ..constants import *
from ..keys import *
from ..generate import draw_text, draw_image
from ..sprites.platform import Platform
from ..sprites.doodle import Doodle
from ..collide import jump_platform


def menu(surf: pygame.Surface, clock: pygame.time.Clock, assets: dict, best_score: int):
    selected = 0
    texts = ["Play", "Exit"]
    tutorial = ["[left], [right]: move doodle", "[space]: shoot bullet", "[p]: pause the game"]

    all_sprites = pygame.sprite.LayeredUpdates()
    platform_sprites = pygame.sprite.Group()

    doodle = Doodle(assets)
    doodle.rect.centerx = 75

    platform = Platform(assets["green_pf"], (0, HEIGHT), "green")
    platform.rect.centerx = 75
    platform.rect.y = HEIGHT - 100
    all_sprites.add(platform)
    platform_sprites.add(platform)

    button_x = HALF_WIDTH
    text_y = 100

    while True:
        clock.tick(FPS)
    # get inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return -1
            elif event.type == pygame.KEYDOWN:
                if event.key == K_UP:
                    selected -= 1
                    selected %= len(texts)
                elif event.key == K_DOWN:
                    selected += 1
                    selected %= len(texts)
                elif event.key == K_RETURN:
                    return selected

    # update game
        all_sprites.update()
        doodle.update()
        jump_platform(doodle, platform_sprites)
        if doodle.rect.top > HEIGHT:
            doodle.rect.centerx = 75
            doodle.rect.y = 0

    # display
        surf.blit(assets["background"], (0, 0))

        draw_text(
            surf, assets["font"],
            "Doodle Jump",
            48, RED, HALF_WIDTH, text_y, centerx=True, centery=True
        )
        draw_text(
            surf, assets["font"],
            f"Your high score: {best_score}",
            24, BLACK, HALF_WIDTH, text_y+50, centerx=True, centery=True
        )

        button_y = text_y + 120
        for i in range(len(texts)):
            if i == selected:
                image = assets["selected_button"]
            else:
                image = assets["button"]
            draw_image(surf, image, button_x, button_y)
            draw_text(
                surf, assets["font"],
                texts[i],
                24, BLACK, button_x, button_y, centerx=True, centery=True
            )
            button_y += 75

        for text in tutorial:
            draw_text(
                surf, assets["font"],
                text,
                18, BLACK, HALF_WIDTH, button_y, centerx=True
            )
            button_y += 30

        draw_text(
            surf, assets["font"],
            "Use [up], [down], [enter] to select.",
            18, BLACK, HALF_WIDTH, HEIGHT-50, centerx=True
        )

        all_sprites.draw(surf)
        doodle.draw(surf)
        pygame.display.update()
