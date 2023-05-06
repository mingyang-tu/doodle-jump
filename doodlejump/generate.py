import pygame
import random
from .constants import *
from .sprites.platform import Platform


def generate_platform(assets, all_sprites, platform_sprites, curr_stage=1):
    stage = min(DIFFICULTY, curr_stage)
    max_y = HEIGHT // 100 + 1

    platforms = {"green": assets["green_pf"], "blue": assets["blue_pf"]}

    for i in range(DIFFICULTY-stage+1):
        for j in range(0, max_y):
            if random.random() > BLUE_PROB:
                pf = "green"
            else:
                pf = "blue"

            platform = Platform(platforms[pf], (j*100, (j+1)*100), pf)
            all_sprites.add(platform)
            platform_sprites.add(platform)
