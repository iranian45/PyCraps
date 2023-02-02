import pygame

from settings import *

class Chips:
    def __init__(self, player):
        self.player = player
        self.chip_values = [1, 5, 25, 100, 500, 1000]
        self.chip_colors = {1:white, 5:red, 25:green, 100:light_grey, 500:light_purple, 1000:orange}
        self.chip_buttons = []
        self.selected_chip = None
        for value in self.chip_values:
            x = 200 - (len(self.chip_values)*50)/2 + self.chip_values.index(value)*75
            y = screen_height - 50
            self.chip_buttons.append((x, y))
    def create(self):
        for button in self.chip_buttons:
            value = self.chip_values[self.chip_buttons.index(button)]
            color = self.chip_colors[value]
            if self.selected_chip == value:
                pygame.draw.circle(screen, yellow, button, screen_height/21, 5)
            pygame.draw.circle(screen, color, button, screen_height/25)
            font = pygame.font.SysFont('Algerian', int(screen_height/40))
            text_surface = font.render(str(value), True, black)
            text_rect = text_surface.get_rect()
            text_rect.center = button
            screen.blit(text_surface, text_rect)

    def handle_clicks(self, pos):
        for button in self.chip_buttons:
            if (pygame.math.Vector2(button)-pygame.math.Vector2(pos)).length() <= screen_height/25:
                self.selected_chip = self.chip_values[self.chip_buttons.index(button)]
                