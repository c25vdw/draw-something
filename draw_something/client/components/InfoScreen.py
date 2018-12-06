import pygame
from client.settings import *


class InfoScreen:
    def __init__(self, width, height,
                 root_screen, server_handler,
                 timeout=5000):
        self.timeout = timeout
        self.svh = server_handler
        self.screen = root_screen

        self.width = width
        self.height = height

        self.surface = pygame.Surface((width, height))
        self.surface.fill(YELLOW_1)

        self.font = pygame.font.Font(None, 38)
        self.answer_font = pygame.font.Font(None, 46)
        self.answer_surface_size = (width, height // 3)
        self.answer_surface = pygame.Surface((width // 1.5, height // 3))
        self.answer_surface.fill(BLUE)

        self.score_surface_size = (width // 3, height // 2)
        self.score_surface = pygame.Surface((width // 3, height // 2))
        self.score_surface.fill(SILVER)

    def draw(self, answer):  # answer is a cached answer variable done in Game
        self._draw_answer(answer)
        self._draw_score()

        self.surface.blit(self.answer_surface, (self.width // 3.5, 0))
        self.surface.blit(self.score_surface,
                          (self.width // 3, self.height // 3))
        self.screen.blit(self.surface, (0, 0))

    def _draw_answer(self, answer):
        self.answer_surface.fill(YELLOW_1)

        answer_txt_surface = self.answer_font.render(
            "The answer was " + str(answer), True, BLACK)
        self.answer_surface.blit(answer_txt_surface, (0, self.height // 6))

    def _render_score_txt_surfaces(self):
        score_text_surfaces = []

        title = self.font.render(
            "Score", True, BLACK)
        score_text_surfaces.append(title)

        for key, val in self.svh.score.items():
            line = self.font.render(
                "Player {}: {}".format(key, val), True, BLACK)
            score_text_surfaces.append(line)

        return score_text_surfaces

    def _draw_score(self):
        self.score_surface.fill(YELLOW_1)

        score_lines = self._render_score_txt_surfaces()
        LINEHEIGHT = 50
        for i, text_surface in enumerate(score_lines):
            self.score_surface.blit(text_surface, (0, i * LINEHEIGHT))
