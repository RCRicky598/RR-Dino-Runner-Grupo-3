import pygame, random

from dino_runner.components.obstacles.bird import Bird
from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.utils.constants import SMALL_CACTUS, LARGE_CACTUS, BIRD


class ObstacleManager:
    def __init__(self):
        self.obstacles = []
    
    def update(self, game):
        obstacle_random = random.randint(1,3)
        if obstacle_random == 1:
            if len(self.obstacles) == 0:
                cactus = Cactus(SMALL_CACTUS)
                self.obstacles.append(cactus)
        elif obstacle_random == 2:
            if len(self.obstacles) == 0:
                cactus = Cactus(LARGE_CACTUS)
                self.obstacles.append(cactus)
                cactus.rect.y = 300
        elif obstacle_random == 3:
            if len(self.obstacles) == 0:
                    self.obstacles.append(Bird())                                   

        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if game.player.dino_rect.colliderect(obstacle.rect):
                game.playing = False
                game.death_count += 1
                game.game_speed = 20
                break

    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)
    
    def reset_obstacles(self):
            self.obstacles = []