import pygame
from pygame.sprite import Sprite

from dino_runner.utils.constants import SCREEN_WIDTH


class Obstacle(Sprite):
    def __init__(self, image, obstacle_type):
        self.image = image
        self.obstacle_type = obstacle_type
        self.obstacle_draw = self.image[self.obstacle_type]
        self.rect = self.obstacle_draw.get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self, game_speed, obstacles):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, screen):
        screen.blit(self.obstacle_draw, (self.rect.x, self.rect.y))