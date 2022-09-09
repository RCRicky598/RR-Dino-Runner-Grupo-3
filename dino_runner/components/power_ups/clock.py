from dino_runner.components.power_ups.power_up import PowerUp
from dino_runner.utils.constants import CLOCK, CLOCK_TYPE

class Clock(PowerUp):
    def __init__(self):
        super().__init__(CLOCK, CLOCK_TYPE)

    def update(self, game_speed, power_ups):
        super().update(game_speed, power_ups)
        