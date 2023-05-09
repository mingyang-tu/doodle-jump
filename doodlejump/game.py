import pygame
import os
from .constants import *
from .sprites.doodle import Doodle
from .sprites.platform import Platform
from .generate import (
    generate_platform,
    generate_init_platform,
    draw_text,
    draw_image
)
from .collide import jump_platform


def load_assets(assets_root):
    assets = dict()
    assets["background"] = pygame.image.load(os.path.join(assets_root, "background.png")).convert()
    assets["green_pf"] = pygame.image.load(os.path.join(assets_root, "platforms", "green.png")).convert_alpha()
    assets["blue_pf"] = pygame.image.load(os.path.join(assets_root, "platforms", "blue.png")).convert_alpha()
    assets["doodle"] = pygame.image.load(os.path.join(assets_root, "doodle.png")).convert_alpha()
    assets["button"] = pygame.image.load(os.path.join(assets_root, "buttons", "button.png")).convert_alpha()
    assets["selected_button"] = pygame.image.load(os.path.join(
        assets_root, "buttons", "selected_button.png")).convert_alpha()

    assets["font"] = os.path.join(assets_root, "Gochi_Hand", "GochiHand-Regular.ttf")

    return assets


class Game:
    def __init__(self, assets_root="./doodlejump/assets/"):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Doodle Jump")
        self.clock = pygame.time.Clock()

        self.assets = load_assets(assets_root)

        # initial settings
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.platform_sprites = pygame.sprite.Group()

        self.doodle = Doodle(self.assets["doodle"])
        self.all_sprites.add(self.doodle)

        generate_init_platform(self.assets, [self.all_sprites, self.platform_sprites], HEIGHT-50)
        generate_platform(
            self.assets,
            [self.all_sprites, self.platform_sprites],
            [HEIGHT-100, -STAGE_LENGTH-BUFFER_LENGTH],
            1
        )

        self.camera_move = 0
        self.stage = 1
        self.score = 0
        self.running = True
        self.gameover = False
        self.showmenu = False

    def init_game(self):
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.platform_sprites = pygame.sprite.Group()

        self.doodle = Doodle(self.assets["doodle"])
        self.all_sprites.add(self.doodle)

        generate_init_platform(self.assets, [self.all_sprites, self.platform_sprites], HEIGHT-50)
        generate_platform(
            self.assets,
            [self.all_sprites, self.platform_sprites],
            [HEIGHT-100, -STAGE_LENGTH-BUFFER_LENGTH],
            1
        )

        self.camera_move = 0
        self.stage = 1
        self.score = 0
        self.running = True
        self.gameover = False
        self.showmenu = False

    def game_over(self):
        drop, target_pos = HEIGHT * 2, HEIGHT // 3
        camera_y = drop + target_pos

        def _draw_moving_text():
            draw_text(
                self.screen, self.assets["font"],
                "Game Over !",
                32, RED, HALF_WIDTH, camera_y-50, centerx=True
            )
            draw_text(
                self.screen, self.assets["font"],
                f"Your score: {self.score}",
                32, BLACK, HALF_WIDTH, camera_y, centerx=True
            )

        # dropping animation
        while True:
            if (self.doodle.rect.y > HEIGHT + 100) and (camera_y <= target_pos):
                break
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return -1

            self.all_sprites.update()
            if camera_y > target_pos:
                for sprite in self.all_sprites:
                    sprite.rect.y -= GG_SPEED
                camera_y -= GG_SPEED
            else:
                self.doodle.rect.y -= GG_SPEED

            self.screen.blit(self.assets["background"], (0, 0))
            self.all_sprites.draw(self.screen)
            _draw_moving_text()
            pygame.display.update()

        for sprite in self.all_sprites:
            sprite.kill()

        # choices
        selected = 0
        texts = ["Play Again", "Menu", "Exit"]
        button_x = HALF_WIDTH

        while True:
            self.clock.tick(FPS)

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

            self.screen.blit(self.assets["background"], (0, 0))
            _draw_moving_text()
            button_y = camera_y + 100
            for i in range(len(texts)):
                if i == selected:
                    image = self.assets["selected_button"]
                else:
                    image = self.assets["button"]
                draw_image(self.screen, image, button_x, button_y)
                draw_text(
                    self.screen, self.assets["font"],
                    texts[i],
                    24, BLACK, button_x, button_y, centerx=True, centery=True
                )
                button_y += 75
            draw_text(
                self.screen, self.assets["font"],
                "Use [up], [down], [enter] to select.",
                18, BLACK, HALF_WIDTH, HEIGHT-50, centerx=True
            )
            pygame.display.update()

    def menu(self):
        selected = 0
        texts = ["Play", "Exit"]

        all_sprites = pygame.sprite.LayeredUpdates()
        platform_sprites = pygame.sprite.Group()

        doodle = Doodle(self.assets["doodle"])
        doodle.rect.centerx = 75
        all_sprites.add(doodle)

        platform = Platform(self.assets["green_pf"], (0, HEIGHT), "green")
        platform.rect.centerx = 75
        platform.rect.y = HEIGHT - 100
        all_sprites.add(platform)
        platform_sprites.add(platform)

        button_x = HALF_WIDTH
        text_y = 100

        while True:
            self.clock.tick(FPS)
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
            self.screen.blit(self.assets["background"], (0, 0))

            draw_text(
                self.screen, self.assets["font"],
                "Doodle Jump",
                48, RED, HALF_WIDTH, text_y, centerx=True, centery=True
            )

            button_y = text_y + 100
            for i in range(len(texts)):
                if i == selected:
                    image = self.assets["selected_button"]
                else:
                    image = self.assets["button"]
                draw_image(self.screen, image, button_x, button_y)
                draw_text(
                    self.screen, self.assets["font"],
                    texts[i],
                    24, BLACK, button_x, button_y, centerx=True, centery=True
                )
                button_y += 75

            draw_text(
                self.screen, self.assets["font"],
                "[left], [right]: move doodle",
                18, BLACK, HALF_WIDTH, button_y, centerx=True
            )
            draw_text(
                self.screen, self.assets["font"],
                "[space]: shoot bullet",
                18, BLACK, HALF_WIDTH, button_y+50, centerx=True
            )
            draw_text(
                self.screen, self.assets["font"],
                "Use [up], [down], [enter] to select.",
                18, BLACK, HALF_WIDTH, HEIGHT-50, centerx=True
            )

            all_sprites.draw(self.screen)
            pygame.display.update()

    def run(self):
        self.showmenu = True

        while self.running:
            if self.gameover:
                close = self.game_over()
                self.gameover = False
                if close == 0:
                    self.init_game()
                elif close == 1:
                    self.showmenu = True
                elif close == -1 or close == 2:
                    break
                else:
                    raise ValueError("Unexpected value of [close]")

            if self.showmenu:
                close = self.menu()
                if close == 0:
                    self.init_game()
                elif close == -1 or close == 1:
                    break
                else:
                    raise ValueError("Unexpected value of [close]")

            self.clock.tick(FPS)

        # get inputs
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

        # update game
            self.all_sprites.update()
            jump_platform(self.doodle, self.platform_sprites)

            # move camera
            if self.doodle.rect.y < HALF_HEIGHT:
                diff = HALF_HEIGHT - self.doodle.rect.y
                self.camera_move += diff
                self.score += diff
                for sprite in self.all_sprites:
                    sprite.rect.y += diff
                if self.camera_move > STAGE_LENGTH:
                    self.stage += 1
                    generate_platform(
                        self.assets,
                        [self.all_sprites, self.platform_sprites],
                        [self.camera_move-STAGE_LENGTH-BUFFER_LENGTH, self.camera_move-STAGE_LENGTH*2-BUFFER_LENGTH],
                        self.stage
                    )
                    self.camera_move = 0

            if self.doodle.rect.y > HEIGHT:
                self.gameover = True

        # display
            self.screen.blit(self.assets["background"], (0, 0))
            self.all_sprites.draw(self.screen)
            draw_text(self.screen, self.assets["font"], str(self.score), 32, BLACK, 10, 0)
            pygame.display.update()

        pygame.quit()
