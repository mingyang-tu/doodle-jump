import pygame
from ..constants import *
from ..keys import *
from ..generate import draw_text, draw_image
from ..sprites.doodle import Doodle


def pause(surf: pygame.Surface, clock: pygame.time.Clock, assets: dict, all_sprites: pygame.sprite.LayeredUpdates, doodle: Doodle, score: int):
    selected = 0
    texts = ["Resume", "Menu"]

    button_x = HALF_WIDTH
    text_y = 150

    while True:
        clock.tick(FPS)

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
                elif event.key == K_PAUSE:
                    return 0

        all_sprites.draw(surf)
        doodle.draw(surf)
        surf.blit(assets["transparent_bg"], (0, 0))
        draw_text(surf, assets["font"], str(score), 32, BLACK, 10, 0)
        draw_text(
            surf, assets["font"],
            "Paused",
            32, BLACK, HALF_WIDTH, text_y, centerx=True
        )
        button_y = text_y + 100
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
        pygame.display.update()
