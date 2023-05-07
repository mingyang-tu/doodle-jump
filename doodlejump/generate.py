import pygame
import random
from .constants import *
from .sprites.platform import Platform


def generate_init_platform(assets, sprites):
    space = WIDTH / 9
    for i in range(5):
        platform = Platform(assets["green_pf"], (0, HEIGHT), "green")
        platform.rect.x = i * space * 2
        platform.rect.y = HEIGHT - 50
        for sprite in sprites:
            sprite.add(platform)


def generate_platform(assets, sprites, y_range, difficulty=None):
    if difficulty is None:
        difficulty = random.randint(2, 4)

    if difficulty > 1:
        blue_prob = random.choice([0.2, 0.4, 0.6, 0.8, 1])
    else:
        blue_prob = 0.

    platforms = {"green": assets["green_pf"], "blue": assets["blue_pf"]}

    for i in range(y_range[0], y_range[1]-1, -100):
        for _ in range(5 - difficulty):
            if random.random() > blue_prob:
                pf = "green"
            else:
                pf = "blue"
            platform = Platform(platforms[pf], (i-100, i), pf)
            for sprite in sprites:
                sprite.add(platform)

