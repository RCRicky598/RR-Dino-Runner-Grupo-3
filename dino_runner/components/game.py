from typing import Text
from unittest.mock import DEFAULT
import pygame

from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacle_magager import ObstacleManager
from dino_runner.components.power_ups.power_up_manager import PowerUpManager
from dino_runner.utils.constants import BG, DEFAULT_TYPE, FONT_STYLE, ICON, RESET_GAME, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS



class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 380

        self.player = Dinosaur()
        self.obstacle_mamager = ObstacleManager()
        self.power_up_manager = PowerUpManager()

        self.running = False
        self.score = 0
        self.max_score = 0
        self.death_count = 0
        self.text_color = (0, 0, 0)


    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                self.show_menu()

    def run(self):
        # Game loop: events - update - draw
        self.playing = True
        self.obstacle_mamager.reset_obstacles()
        self.power_up_manager.reset_power_ups()
        self.score = 0
        self.game_speed = 20
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False

    def update(self):
        self.update_score()
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_mamager.update(self)
        self.power_up_manager.update(self.score, self.game_speed, self.player)

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        self.draw_score()
        self.draw_power_up_time()
        self.player.draw(self.screen)
        self.obstacle_mamager.draw(self.screen)
        self.draw_deaht_count()
        self.power_up_manager.draw(self.screen)
        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed
    
    def update_score(self):
        self.score += 1
        if self.score % 100 == 0:
            self.game_speed += 0.5

        if self.max_score < self.score:
            self.max_score = self.score
    
    def draw_deaht_count(self):
        if self.death_count > 0:
            print_message(self.screen, 
            f"Deaths counter: {self.death_count}", 
            18, 
            100, 
            50, 
            self.text_color
        )

    def draw_score(self):
        print_message(
            self.screen, 
            f"Best score: {self.max_score}  Score: {self.score}", 
            18, 
            950, 
            50, 
            self.text_color
        )

    def draw_power_up_time(self):
        if self.player.has_power_up:
            time_to_show = round((self.player.power_up_time_up - pygame.time.get_ticks()) / 1000,2)
            if time_to_show >= 0:
                print_message(
                    self.screen,
                    f"{self.player.type.capitalize()} enabled for {time_to_show} seconds.",
                    18,
                    (SCREEN_WIDTH // 2),
                    ((SCREEN_HEIGHT // 2) - 200),
                    self.text_color
                )
            else:
                self.player.has_power_up = False
                self.player.type = DEFAULT_TYPE

    def handle_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.run()

    def show_menu(self):
        self.screen.fill((255, 255, 255))
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2
        if self.death_count == 0:
            print_message(
                self.screen, 
                "Press any key to start", 
                30, 
                half_screen_width, 
                half_screen_height, 
                self.text_color
            )
            self.screen.blit(ICON, (half_screen_width -48, half_screen_height -140))
        else:
            print_message(
                self.screen,
                "Press any key to play again",
                30,
                half_screen_width,
                half_screen_height-85,
                self.text_color
            )
            print_message(
                self.screen, 
                f"Best score: {self.max_score}", 
                20, 
                half_screen_width, 
                half_screen_height+5, 
                self.text_color
            )
            print_message(
                self.screen, 
                f"Round score: {self.score}", 
                20, 
                half_screen_width, 
                half_screen_height-15, 
                self.text_color 
            )
            print_message(
                self.screen, 
                f"Deaths counter: {self.death_count}", 
                20, 
                half_screen_width, 
                half_screen_height-35, 
                self.text_color 
            )
            self.screen.blit(RESET_GAME, (half_screen_width -37, half_screen_height +35))

        pygame.display.update()
        self.handle_events_on_menu()
        

def print_message(draw_screen, message, size, half_screen_width, half_screen_height, color):
    font = pygame.font.Font(FONT_STYLE, size)
    text = font.render(message, True, color)
    text_rect = text.get_rect()
    text_rect.center = (half_screen_width, half_screen_height)
    draw_screen.blit(text, text_rect)