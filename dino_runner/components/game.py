from typing import Text
import pygame

from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacle_magager import ObstacleManager
from dino_runner.utils.constants import BG, FONT_STYLE, ICON, RESET_GAME, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS


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

        self.running = False
        self.score = 0
        self.max_score = 0
        self.death_count = 0

    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                self.show_menu()

    def run(self):
        # Game loop: events - update - draw
        self.playing = True
        self.obstacle_mamager.reset_obstacles()
        self.score = 0
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

    def update_score(self):
        self.score += 1
        if self.score % 100 == 0:
            self.game_speed += 2
        if self.max_score < self.score:
            self.max_score = self.score
    
    def draw_deaht_count(self):
        if self.death_count > 0:
            print_message(self, f"Deaths counter: {self.death_count}", 18, 100, 50, (0, 0, 0))

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        self.draw_score()
        self.player.draw(self.screen)
        self.obstacle_mamager.draw(self.screen)
        self.draw_deaht_count()
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

    def draw_score(self):
        print_message(self, f"Best score: {self.max_score}  Score: {self.score}", 18, 950, 50, (0, 0, 0))

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
            print_message(self, "Press any key to start", 30, half_screen_width, half_screen_height, (0, 0, 0))
        else:
            print_message(self, "Press any key to play again", 30, half_screen_width, half_screen_height, (0, 0, 0))
            print_message(self, f"Best score: {self.max_score} Round score: {self.score} Deaths counter: {self.death_count}", 20, half_screen_width, half_screen_height+35, (0, 0, 0))
            self.screen.blit(RESET_GAME, (half_screen_width -37, half_screen_height + 60))

        self.screen.blit(ICON, (half_screen_width -48, half_screen_height -140))
        pygame.display.update()
        self.handle_events_on_menu()
        

def print_message(self, message, size, half_screen_width, half_screen_height, color):
            font = pygame.font.Font(FONT_STYLE, size)
            text = font.render(message, True, color)
            text_rect = text.get_rect()
            text_rect.center = (half_screen_width, half_screen_height)
            self.screen.blit(text, text_rect)