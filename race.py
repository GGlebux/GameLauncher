from __future__ import division
import pygame
import random
import time
import sys
import os

class CarGame:
    def __init__(self, menu_class=None):
        pygame.init()

        self.menu_class = menu_class  # Устанавливаем класс меню
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.width, self.height = self.screen.get_size()
        self.fps = 120
        self.clock = pygame.time.Clock()

        # Шрифты
        self.font = pygame.font.Font(None, int(self.height * 0.06))
        self.score_font = pygame.font.Font(None, int(self.height * 0.05))
        self.button_font = pygame.font.Font(None, int(self.height * 0.05))

        # Загрузка ресурсов
        self.background = self.load_image("ForRace/images/roadway.jpg", (self.width, self.height))
        self.carimg = self.load_image("ForRace/images/car.png", (int(self.width * 0.08), int(self.height * 0.2)))
        self.truckimg = self.load_image("ForRace/images/pickup.png", (int(self.width * 0.1), int(self.height * 0.3)))

        self.tires = self.load_sound("ForRace/sounds/tires_skid.ogg")
        self.crash = self.load_sound("ForRace/sounds/crash.ogg")
        self.countdown1 = self.load_sound("ForRace/sounds/countdown1.ogg")
        self.countdown2 = self.load_sound("ForRace/sounds/countdown2.ogg")
        self.soundtrack = self.load_sound("ForRace/sounds/soundtrack.ogg")

        # Настройки звука
        self.tires.set_volume(1)
        self.crash.set_volume(2)
        self.soundtrack.set_volume(0.5)

        # Параметры автомобиля и дороги
        self.car_width = int(self.width * 0.08)
        self.car_height = int(self.height * 0.2)
        self.road_left = int(self.width * 0.04)
        self.road_right = int(self.width * 0.96)

    def load_image(self, path, size=None):
        if not os.path.exists(path):
            print(f"Error: Image not found at {path}")
            pygame.quit()
            sys.exit()
        img = pygame.image.load(path)
        if size:
            img = pygame.transform.scale(img, size)
        return img

    def load_sound(self, path):
        if not os.path.exists(path):
            print(f"Error: Sound not found at {path}")
            pygame.quit()
            sys.exit()
        return pygame.mixer.Sound(path)

    def return_to_menu(self):
        pygame.mixer.stop()  # Остановить звуки

        if not self.menu_class:
            from Menu import GradientMenu  # Выполняем отложенный импорт
            self.menu_class = GradientMenu

        menu = self.menu_class()  # Создаем экземпляр GradientMenu
        menu.run()  # Запускаем меню
        sys.exit()  # Завершаем текущий процесс игры

    def draw_exit_button(self):
        button_width, button_height = int(self.width * 0.1), int(self.height * 0.08)
        button_rect = pygame.Rect(10, 10, button_width, button_height)
        pygame.draw.rect(self.screen, (200, 0, 0), button_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), button_rect, 3)
        button_text = self.button_font.render("EXIT", True, (255, 255, 255))
        text_rect = button_text.get_rect(center=button_rect.center)
        self.screen.blit(button_text, text_rect)
        return button_rect

    def loading_screen(self):
        self.screen.fill((0, 0, 0))
        pygame.display.flip()

        self.countdown1.play()
        time.sleep(1)
        self.countdown1.play()
        time.sleep(1)
        self.countdown2.play()
        time.sleep(1)

        self.soundtrack.play(-1)

    def avoided(self, count):
        score_text = self.score_font.render(f"Score: {count}", True, (0, 0, 0))
        self.screen.blit(score_text, (int(self.width * 0.05), int(self.height * 0.95)))

    def message(self, text):
        message_font = self.font.render(text, True, (0, 0, 0))
        rect = message_font.get_rect(center=(self.width // 2, self.height // 2))
        self.screen.blit(message_font, rect)
        pygame.display.update()
        time.sleep(3)
        self.playing()

    def playing(self):
        x = self.width // 2 - self.car_width // 2
        y = self.height - int(self.height * 0.2)

        xChange = 0
        truck_x = random.randrange(self.road_left, self.road_right - int(self.width * 0.1))
        truck_y = -int(self.height * 0.3)
        truck_speed = self.height * 0.002

        score = 0

        while True:
            self.clock.tick(self.fps)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        xChange = -int(self.width * 0.004)
                    if event.key == pygame.K_RIGHT:
                        xChange = int(self.width * 0.004)
                    if event.key == pygame.K_ESCAPE:
                        self.return_to_menu()

                if event.type == pygame.KEYUP:
                    if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                        xChange = 0

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if exit_button.collidepoint(event.pos):
                            self.return_to_menu()

            x += xChange

            self.screen.blit(self.background, self.background.get_rect())
            exit_button = self.draw_exit_button()
            self.screen.blit(self.truckimg, (truck_x, truck_y))
            truck_y += truck_speed
            self.screen.blit(self.carimg, (x, y))
            self.avoided(score)

            if x > self.road_right - self.car_width or x < self.road_left:
                self.tires.play()
                self.crash.play()
                self.message("You went off the road!")

            if truck_y > self.height:
                truck_y = -int(self.height * 0.3)
                truck_x = random.randrange(self.road_left, self.road_right - int(self.width * 0.1))
                score += 1
                truck_speed += self.height * 0.0002

            if y < truck_y + int(self.height * 0.3):
                if (x > truck_x and x < truck_x + int(self.width * 0.1)) or (
                    x + self.car_width > truck_x and x + self.car_width < truck_x + int(self.width * 0.1)
                ):
                    self.crash.play()
                    self.message("You hit a truck!")

            pygame.display.flip()

    def run(self):
        self.loading_screen()
        self.playing()


if __name__ == "__main__":
    from Menu import GradientMenu
    game = CarGame(menu_class=GradientMenu)
    game.run()