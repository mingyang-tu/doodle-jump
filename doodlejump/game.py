import pygame
import os
from .constants import *
from .keys import *
from .sprites.doodle import Doodle
from .pages.game_over import game_over
from .pages.menu import menu
from .pages.pause import pause
from .generate import (
    generate_platform,
    generate_init_platform,
    generate_monster,
    draw_text
)
from .collide import (
    jump_platform,
    touch_monster,
    kill_monster
)


def load_assets(assets_root):
    assets = dict()
    assets["background"] = pygame.image.load(os.path.join(assets_root, "background.png")).convert()
    assets["transparent_bg"] = assets["background"].copy()
    assets["transparent_bg"].set_alpha(200)
    assets["green_pf"] = pygame.image.load(os.path.join(assets_root, "platforms", "green.png")).convert_alpha()
    assets["blue_pf"] = pygame.image.load(os.path.join(assets_root, "platforms", "blue.png")).convert_alpha()
    assets["doodle"] = pygame.image.load(os.path.join(assets_root, "doodles", "doodle.png")).convert_alpha()
    assets["doodle_shoot"] = pygame.image.load(os.path.join(assets_root, "doodles", "doodle_shoot.png")).convert_alpha()
    assets["button"] = pygame.image.load(os.path.join(assets_root, "buttons", "button.png")).convert_alpha()
    assets["selected_button"] = pygame.image.load(os.path.join(
        assets_root, "buttons", "selected_button.png")).convert_alpha()
    assets["spring"] = pygame.image.load(os.path.join(assets_root, "springs", "spring.png")).convert_alpha()
    assets["compressed_spring"] = pygame.image.load(os.path.join(
        assets_root, "springs", "compressed_spring.png")).convert_alpha()
    assets["bullet"] = pygame.image.load(os.path.join(assets_root, "bullet.png")).convert_alpha()
    assets["monsters"] = [
        pygame.image.load(os.path.join(assets_root, "monsters", f"monster{i}.png")).convert_alpha()
        for i in range(1, 4)
    ]

    assets["font"] = os.path.join(assets_root, "Gochi_Hand", "GochiHand-Regular.ttf")

    return assets


class Game:
    def __init__(self, assets_root=os.path.join("doodlejump", "assets")):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Doodle Jump")
        self.clock = pygame.time.Clock()

        self.assets = load_assets(assets_root)
        self.best_score_path = os.path.join(assets_root, "best_score.txt")
        if not os.path.exists(self.best_score_path):
            with open(self.best_score_path, 'w') as f:
                f.write("0")
        with open(self.best_score_path) as f:
            lines = f.readlines()
            self.best_score = int(lines[0])

        # initial settings
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.platform_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.monster_sprites = pygame.sprite.Group()
        self.doodle = Doodle(self.assets)

        self.camera_move = 0
        self.stage = 1
        self.score = 0
        self.running = True
        self.gameover = False
        self.showmenu = False
        self.touch_monster = False

    def init_game(self):
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.platform_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.monster_sprites = pygame.sprite.Group()

        self.doodle = Doodle(self.assets)

        generate_init_platform(self.assets, [self.all_sprites, self.platform_sprites], HEIGHT-50)
        generate_platform(
            self.assets,
            [self.all_sprites, self.platform_sprites],
            (HEIGHT-100, -STAGE_LENGTH-BUFFER_LENGTH),
            1
        )
        generate_monster(
            self.assets,
            [self.all_sprites, self.monster_sprites],
            (-STAGE_LENGTH-BUFFER_LENGTH+MONSTER_SPACE, -STAGE_LENGTH-BUFFER_LENGTH)
        )

        self.camera_move = 0
        self.stage = 1
        self.score = 0
        self.running = True
        self.gameover = False
        self.showmenu = False
        self.touch_monster = False

    def run(self):
        self.showmenu = True

        while self.running:
            if self.gameover:
                close = game_over(
                    self.screen, self.clock, self.assets,
                    self.all_sprites, self.doodle,
                    self.score, self.best_score
                )
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
                close = menu(self.screen, self.clock, self.assets, self.best_score)
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
                elif event.type == pygame.KEYDOWN:
                    if event.key == K_PAUSE:
                        close = pause(
                            self.screen, self.clock, self.assets,
                            self.all_sprites, self.doodle,
                            self.score, self.best_score
                        )
                        if close == 0:
                            pass
                        elif close == 1:
                            self.showmenu = True
                        elif close == -1:
                            self.running = False
                        else:
                            raise ValueError("Unexpected value of [close]")
                    elif event.key == K_SHOOT and not self.touch_monster:
                        self.doodle.shoot(self.assets["bullet"], [self.all_sprites, self.bullet_sprites])
            if not self.running:
                break

        # update game
            self.all_sprites.update()
            self.doodle.update()

            if not self.touch_monster:
                jump_platform(self.doodle, self.platform_sprites)
                self.score += kill_monster(self.monster_sprites, self.bullet_sprites)
                if touch_monster(self.doodle, self.monster_sprites):
                    self.touch_monster = True

            if self.doodle.rect.y > HEIGHT:
                self.gameover = True
                if self.score > self.best_score:
                    self.best_score = self.score
                    with open(self.best_score_path, 'w') as f:
                        f.write(str(self.best_score))

            # move camera
            if self.doodle.rect.bottom < HALF_HEIGHT:
                diff = HALF_HEIGHT - self.doodle.rect.bottom
                self.camera_move += diff
                self.score += diff
                for sprite in self.all_sprites:
                    sprite.rect.y += diff
                self.doodle.rect.y += diff
                if self.camera_move > STAGE_LENGTH:
                    self.stage += 1
                    bot = self.camera_move-STAGE_LENGTH-BUFFER_LENGTH
                    generate_platform(
                        self.assets,
                        [self.all_sprites, self.platform_sprites],
                        (bot, bot-STAGE_LENGTH),
                        self.stage
                    )
                    generate_monster(
                        self.assets,
                        [self.all_sprites, self.monster_sprites],
                        (bot, bot-STAGE_LENGTH)
                    )
                    self.camera_move = 0

        # display
            self.screen.blit(self.assets["background"], (0, 0))
            self.all_sprites.draw(self.screen)
            self.doodle.draw(self.screen)
            draw_text(self.screen, self.assets["font"], str(self.score), 32, BLACK, 10, 0)
            if self.best_score > 0 and self.score > self.best_score:
                draw_text(self.screen, self.assets["font"], "Best Score !!!", 18, RED, 10, 30)
            pygame.display.update()

        pygame.quit()
