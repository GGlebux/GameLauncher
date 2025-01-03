import pygame
import datetime
import sys
import sqlite3
from tetris import Tetris
from race import CarGame



class GradientMenu:
    def __init__(self):
        pygame.init()

        self.WIDTH, self.HEIGHT = 1200, 600
        self.FPS = 60
        self.ICON_SIZE = 64
        self.FOLDER_SIZE = 100
        self.FOLDER_EXPANDED_SIZE = 200

        self.WHITE = (255, 255, 255)
        self.ORANGE = (255, 165, 0)
        self.PURPLE = (128, 0, 128)
        self.BLACK = (0, 0, 0)
        self.SHADOW_COLOR = (50, 50, 50, 128)

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.WIDTH, self.HEIGHT = self.screen.get_size()

        pygame.display.set_caption("Gradient Menu with Clock")

        self.font_large = pygame.font.SysFont("Verdana", 48)
        self.font_small = pygame.font.SysFont("Verdana", 24)
        self.font_icon_text = pygame.font.SysFont("Comic Sans MS", 20, bold=True)
        self.font_folder_label = pygame.font.SysFont("Arial", 20, bold=True)

        self.folder_position = (300, self.HEIGHT - 300)
        self.folder_rect = pygame.Rect(self.folder_position[0], self.folder_position[1], self.FOLDER_SIZE, self.FOLDER_SIZE)

        self.icons = [
            pygame.image.load("Pikchi/app1.png"),
            pygame.image.load("Pikchi/app2.png"),
        ]

        self.gradient_surface = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        self.folder_open = False
        self.precompute_gradient()

    def precompute_gradient(self):
        for y in range(self.HEIGHT):
            for x in range(self.WIDTH):
                t = (x + y) / (self.WIDTH + self.HEIGHT)
                r = int(self.ORANGE[0] * (1 - t) + self.PURPLE[0] * t)
                g = int(self.ORANGE[1] * (1 - t) + self.PURPLE[1] * t)
                b = int(self.ORANGE[2] * (1 - t) + self.PURPLE[2] * t)
                self.gradient_surface.set_at((x, y), (r, g, b))

    def draw_clock(self):
        now = datetime.datetime.now()
        time_str = now.strftime("%H:%M")
        date_str = now.strftime("%Y-%m-%d")

        time_surface = self.font_large.render(time_str, True, self.BLACK)
        date_surface = self.font_small.render(date_str, True, self.BLACK)

        time_rect = time_surface.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 4 - 20))
        date_rect = date_surface.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 4 + 30))

        self.screen.blit(time_surface, time_rect)
        self.screen.blit(date_surface, date_rect)

    def handle_icon_click(self, pos):
        if self.folder_open:
            expanded_icon_positions = self.get_expanded_icon_positions()
            for i, icon_pos in enumerate(expanded_icon_positions):
                rect = pygame.Rect(icon_pos[0], icon_pos[1], self.ICON_SIZE, self.ICON_SIZE)
                if rect.collidepoint(pos):
                    print(f"App {i + 1} clicked!")
                    if i == 0:
                        self.start_tetris_game()
                    elif i == 1:
                        self.start_car_game()

    def handle_folder_click(self, pos):
        rect = self.folder_rect if not self.folder_open else pygame.Rect(
            self.folder_position[0], self.folder_position[1], self.FOLDER_EXPANDED_SIZE, self.FOLDER_EXPANDED_SIZE
        )
        if rect.collidepoint(pos):
            self.folder_open = not self.folder_open

    def get_expanded_icon_positions(self):
        center_x = self.folder_position[0] + self.FOLDER_EXPANDED_SIZE // 2
        center_y = self.folder_position[1] + self.FOLDER_EXPANDED_SIZE // 2 - 60
        return [
            (center_x - self.ICON_SIZE - 20, center_y - self.ICON_SIZE // 2),
            (center_x + 20, center_y - self.ICON_SIZE // 2),
        ]

    def start_tetris_game(self):
        game = Tetris(16, 30)
        game.run()

    def start_car_game(self):
        cargame = CarGame()
        cargame.run()

    def draw_folder(self):
        rect = self.folder_rect if not self.folder_open else pygame.Rect(
            self.folder_position[0], self.folder_position[1], self.FOLDER_EXPANDED_SIZE, self.FOLDER_EXPANDED_SIZE
        )
        shadow_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        pygame.draw.rect(shadow_surface, self.SHADOW_COLOR, shadow_surface.get_rect(), border_radius=10)
        self.screen.blit(shadow_surface, rect.topleft)

        pygame.draw.rect(self.screen, self.BLACK, rect, width=2, border_radius=10)

        if not self.folder_open:
            icon_positions = [
                (self.folder_position[0] + 10, self.folder_position[1] + 10),
                (self.folder_position[0] + self.FOLDER_SIZE // 2 + 5, self.folder_position[1] + 10),
            ]
            for i, icon_pos in enumerate(icon_positions):
                scaled_icon = pygame.transform.scale(self.icons[i], (self.ICON_SIZE // 2, self.ICON_SIZE // 2))
                self.screen.blit(scaled_icon, icon_pos)

        if self.folder_open:
            expanded_icon_positions = self.get_expanded_icon_positions()
            for i, icon_pos in enumerate(expanded_icon_positions):
                self.screen.blit(pygame.transform.scale(self.icons[i], (self.ICON_SIZE, self.ICON_SIZE)), icon_pos)

               
                labels = ["Tetris", "Race"]
                label_surface = self.font_icon_text.render(labels[i], True, self.BLACK)
                label_rect = label_surface.get_rect(center=(icon_pos[0] + self.ICON_SIZE // 2, icon_pos[1] + self.ICON_SIZE + 15))
                self.screen.blit(label_surface, label_rect)

 
        label_y = self.folder_position[1] + self.FOLDER_SIZE + 20
        label_x = self.folder_position[0] + self.FOLDER_SIZE // 2

        if self.folder_open:
            label_y = self.folder_position[1] + self.FOLDER_EXPANDED_SIZE + 10
            label_x = self.folder_position[0] + self.FOLDER_EXPANDED_SIZE // 2

        label_surface = self.font_folder_label.render("Games", True, self.BLACK)
        label_rect = label_surface.get_rect(center=(label_x, label_y))
        self.screen.blit(label_surface, label_rect)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.handle_icon_click(event.pos)
                    self.handle_folder_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            if self.running:
                self.screen.blit(self.gradient_surface, (0, 0))
                self.draw_clock()
                self.draw_folder()

                pygame.display.flip()
                self.clock.tick(self.FPS)

            else:
                pygame.quit()
                sys.exit()

if __name__ == "__main__":
    menu = GradientMenu()
    menu.run()