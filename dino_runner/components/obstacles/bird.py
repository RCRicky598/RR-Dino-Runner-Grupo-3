import pygame
import random

from dino_runner.components.obstacles.obstacle import Obstacle
from dino_runner.utils.constants import BIRD

class Bird(Obstacle):
    
    def __init__(self):
        self.type = 0
        self.flutter_index = 0
        super().__init__(BIRD, self.type)
        self.rect.y = random.randint(225,300)
    
    def update(self, game_speed, obstacles):
        self.obstacle_draw = BIRD[0] if self.flutter_index < 7 else BIRD[1]
        self.flutter_index += 1
        if self.flutter_index >= 14:
            self.flutter_index = 0
        super().update(game_speed, obstacles)
    
    
        