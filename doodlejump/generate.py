import pygame
import random
from .constants import *
from .sprites.platform import Platform
from .sprites.doodle import Doodle
from .collide import jump_platform


def menu(surf, clock, assets):
    selected = 0
    texts = ["Play", "Exit"]

    button_x = HALF_WIDTH
    top = 100

    all_sprites = pygame.sprite.LayeredUpdates()
    platform_sprites = pygame.sprite.Group()

    doodle = Doodle(assets["doodle"])
    doodle.rect.centerx = 75
    all_sprites.add(doodle)

    platform = Platform(assets["green_pf"], (0, HEIGHT), "green")
    platform.rect.centerx = 75
    platform.rect.y = HEIGHT - 100
    all_sprites.add(platform)
    platform_sprites.add(platform)

    while True:
        clock.tick(FPS)
    # get inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return -1
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected -= 1
                    selected %= len(texts)
                elif event.key == pygame.K_DOWN:
                    selected += 1
                    selected %= len(texts)
                elif event.key == pygame.K_RETURN:
                    return selected

    # update game
        all_sprites.update()
        jump_platform(doodle, platform_sprites)
        if doodle.rect.top > HEIGHT:
            doodle.rect.centerx = 75
            doodle.rect.y = 0

    # display
        surf.blit(assets["background"], (0, 0))

        draw_text(
            surf, assets["font"],
            "Doodle Jump",
            48, RED, HALF_WIDTH, top, centerx=True, centery=True
        )

        button_y = top + 100
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

        draw_text(
            surf, assets["font"],
            "[left], [right]: move doodle",
            18, BLACK, HALF_WIDTH, button_y, centerx=True
        )
        draw_text(
            surf, assets["font"],
            "[space]: shoot bullet",
            18, BLACK, HALF_WIDTH, button_y+50, centerx=True
        )
        draw_text(
            surf, assets["font"],
            "Use [up], [down], [enter] to select.",
            18, BLACK, HALF_WIDTH, HEIGHT-50, centerx=True
        )

        all_sprites.draw(surf)
        pygame.display.update()


def game_over(surf, clock, assets, all_sprites, doodle, score):
    drop, target_pos = HEIGHT * 2, HEIGHT // 3
    camera_y = drop + target_pos

    def _draw_moving_text():
        draw_text(
            surf, assets["font"],
            "Game Over !",
            32, RED, HALF_WIDTH, camera_y-50, centerx=True
        )
        draw_text(
            surf, assets["font"],
            f"Your score: {score}",
            32, BLACK, HALF_WIDTH, camera_y, centerx=True
        )

    while True:
        if doodle.rect.y > HEIGHT + 100:
            break
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return -1

        all_sprites.update()
        if camera_y > target_pos:
            for sprite in all_sprites:
                sprite.rect.y -= GG_SPEED
            camera_y -= GG_SPEED
        else:
            doodle.rect.y -= GG_SPEED

        surf.blit(assets["background"], (0, 0))
        all_sprites.draw(surf)
        _draw_moving_text()
        pygame.display.update()

    for sprite in all_sprites:
        sprite.kill()

    selected = 0
    texts = ["Play Again", "Menu", "Exit"]

    button_x = HALF_WIDTH

    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return -1
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected -= 1
                    selected %= len(texts)
                elif event.key == pygame.K_DOWN:
                    selected += 1
                    selected %= len(texts)
                elif event.key == pygame.K_RETURN:
                    return selected

        surf.blit(assets["background"], (0, 0))
        _draw_moving_text()
        button_y = camera_y + 100
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
        draw_text(
            surf, assets["font"],
            "Use [up], [down], [enter] to select.",
            18, BLACK, HALF_WIDTH, HEIGHT-50, centerx=True
        )
        pygame.display.update()


def draw_image(surf, image, x, y):
    rect = image.get_rect()
    rect.centerx = x
    rect.centery = y
    surf.blit(image, rect)


def draw_text(surf, font_name, text, size, color, x, y, centerx=False, centery=False):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if centerx:
        text_rect.centerx = x
    else:
        text_rect.x = x
    if centery:
        text_rect.centery = y
    else:
        text_rect.y = y
    surf.blit(text_surface, text_rect)


def generate_init_platform(assets, sprites, y):
    space = WIDTH / 9
    for i in range(5):
        platform = Platform(assets["green_pf"], (0, HEIGHT), "green")
        platform.rect.x = i * space * 2
        platform.rect.y = y
        for sprite in sprites:
            sprite.add(platform)


def generate_platform(assets, sprites, y_range, difficulty):
    if difficulty > 1:
        if random.random() > 0.9 or difficulty == 5:
            blue_prob = 1.
        else:
            blue_prob = BLUE_PROB
    else:
        blue_prob = 0.

    if difficulty > 4:
        difficulty = random.randint(2, 4)

    platforms = {"green": assets["green_pf"], "blue": assets["blue_pf"]}

    for i in range(y_range[0], y_range[1], -100):
        min_i = max(i-100, y_range[1])
        for _ in range(5 - difficulty):
            if random.random() > blue_prob:
                pf = "green"
            else:
                pf = "blue"
            platform = Platform(platforms[pf], (min_i, i), pf)
            for sprite in sprites:
                sprite.add(platform)
