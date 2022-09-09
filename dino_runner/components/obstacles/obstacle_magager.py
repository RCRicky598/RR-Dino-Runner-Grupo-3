import pygame, random

from dino_runner.components.obstacles.bird import Bird
from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.components.power_ups.hammer import Hammer
from dino_runner.utils.constants import HAMMER_TYPE, HIT_HAMMER_SOUND, HIT_SHIELD_SOUND, SHIELD_TYPE, SMALL_CACTUS, LARGE_CACTUS, GAME_OVER_SOUND


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
                if game.player.type != SHIELD_TYPE and game.player.type != HAMMER_TYPE:
                    GAME_OVER_SOUND.play()
                    pygame.time.delay(1500)
                    game.playing = False
                    game.death_count += 1
                    break
                else:
                    if game.player.type == HAMMER_TYPE:
                        HIT_HAMMER_SOUND.play()
                        game.hammer_count -= 1
                    elif game.player.type == SHIELD_TYPE:
                        HIT_SHIELD_SOUND.play()
                    self.obstacles.remove(obstacle)

    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)
    
    def reset_obstacles(self):
            self.obstacles = []

    