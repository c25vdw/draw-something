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

        self.winner_font = pygame.font.Font(None, 46)
        self.winner_surface = pygame.Surface((width,300))       #need to position

        self.score_surface_size = (width // 3, height // 2)
        self.score_surface = pygame.Surface((width // 3, height // 2))
        self.score_surface.fill(SILVER)

    def draw(self, answer, end_game, winner):  # answer is a cached answer variable done in Game
        self._draw_answer(answer)
        self._draw_score()
        if end_game:
            self._draw_winner(winner)

        self.surface.blit(self.answer_surface, (self.width // 3.5, 0))
        self.surface.blit(self.score_surface,
                          (self.width // 3, self.height // 3))

        self.surface.blit(self.winner_surface,(0,0))        #need to position

        self.screen.blit(self.surface, (0, 0))

    def _draw_answer(self, answer):
        self.answer_surface.fill(YELLOW_1)

        answer_txt_surface = self.answer_font.render(
            "The answer was " + str(answer), True, BLACK)
        self.answer_surface.blit(answer_txt_surface, (0, self.height // 6))

    def _draw_winner(self,winner):
        self.winner_surface.fill(YELLOW_1)

        if len(winner) == 1:
            winner_txt_surface = self.winner_font.render("The winner is P" + str(winner[0]), True, BLACK)
        elif len(winner) > 1:
            display_txt = "A tie between "
            for i in range(0,len(winner) - 1):
                display_txt += "P" + winner[i]
                if len(winner) == 2:
                    display_txt += " "
                else:
                    display_txt += ", " 
            display_txt += "and P" + winner[-1]
            winner_txt_surface = self.winner_font.render(display_txt, True, BLACK)
        self.winner_surface.blit(winner_txt_surface, (0,0))         #need to position

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
