from asyncio import shield
import pygame
import random
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.power_ups.clock import Clock
from dino_runner.components.power_ups.hammer import Hammer

from dino_runner.components.power_ups.shield import Shield
from dino_runner.utils.constants import GET_CLOCK_SOUND, GET_HAMMER_SOUND, SHIELD_SOUND


class PowerUpManager:
    def __init__(self):
        self.power_ups = []
        self.when_appears = 0
        self.shield = Shield()
        self.hammer = Hammer()
        self.clock = Clock()
        
    def generate_power_up(self, score):
            random_choise = [self.shield, self.hammer, self.clock]
            if len(self.power_ups) == 0 and self.when_appears == score:
                self.when_appears += random.randint(400, 700)
                self.power_ups.append(random.choice(random_choise))

    def update(self, score, game_speed, player: Dinosaur):
        self.generate_power_up(score)
        for power_up in self.power_ups:
            power_up.update(game_speed, self.power_ups)
            if player.dino_rect.colliderect(power_up.rect):
                if self.shield in self.power_ups:
                    SHIELD_SOUND.play()
                elif self.hammer in self.power_ups:
                    GET_HAMMER_SOUND.play()
                elif self.clock in self.power_ups:
                    GET_CLOCK_SOUND.play()
                power_up.start_time = pygame.time.get_ticks()
                player.has_power_up = True
                player.type = power_up.type
                player.power_up_time_up = power_up.start_time + (power_up.duration * 1000)
                self.power_ups.remove(power_up)


    def draw(self, screen):
        for power_up in self.power_ups:
            power_up.draw(screen)

    def reset_power_ups(self, score):
        self.power_ups = []
        self.when_appears = 0
        self.when_appears = score + random.randint(400, 700)
    
