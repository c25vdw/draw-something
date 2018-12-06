import pygame
from client.settings import *


class InfoScreen:
    def __init__(self, width, height,
                 root_screen, server_handler, font_path,
                 timeout=5000):
        self.timeout = timeout
        self.svh = server_handler
        self.screen = root_screen

        self.width = width
        self.height = height

        self.surface = pygame.Surface((width, height))
        self.surface.fill(YELLOW_2)

        # fonts
        self.font = pygame.font.Font(font_path, 32)
        self.answer_font = pygame.font.Font(font_path, 32)
        self.score_font = pygame.font.Font(font_path, 24)
        self.winner_font = pygame.font.Font(font_path, 40)

        # surfaces
        self.score_surface = pygame.Surface((width // 3, height // 2))

    def fill_background(self, color):
        self.surface.fill(color)
        self.score_surface.fill(color)

    def draw(self, answer, end_game, winner):
        # answer is a cached answer variable done in Game
        self.fill_background(YELLOW_2)

        self.draw_answer(answer)
        self.draw_score()
        self.draw_winner(winner)
        if end_game:
            self.draw_game_over()
        self.screen.blit(self.surface, (0, 0))

    def draw_answer(self, answer):
        # "dog"
        answer_txt_surface = self.answer_font.render(
            "\"" + str(answer) + "\"", True, BLACK)

        width, height = answer_txt_surface.get_size()
        self.surface.blit(answer_txt_surface, (self.get_middle_x(
            answer_txt_surface, self.surface), self.height // 5))

    def draw_winner(self, winner):
        # "it's a tie!" or "p1 wins!"
        if len(winner) == 1:
            winner_txt_surface = self.winner_font.render(
                "P" + str(winner[0]) + " wins!", True, BLACK)
        elif len(winner) > 1:
            winner_txt_surface = self.winner_font.render(
                "It's a tie!", True, BLACK)
        else:
            winner_txt_surface = self.winner_font.render("", True, BLACK)

        middle_x = self.get_middle_x(winner_txt_surface, self.surface)
        self.surface.blit(winner_txt_surface, (middle_x, 40))

    def draw_game_over(self):
        txt_surface = self.winner_font.render("game over", True, BLACK)

        x = self.get_middle_x(txt_surface, self.surface)
        self.surface.blit(txt_surface, (x, self.height - 200))

    def draw_score(self):
        '''
             score
            player1: 1
            player2: 0
            ...
        '''
        self.score_surface.fill(YELLOW_2)

        score_lines = self.render_score_txt_surfaces()
        LINEHEIGHT = 50
        for i, text_surface in enumerate(score_lines):
            self.score_surface.blit(text_surface, (self.get_middle_x(
                text_surface, self.score_surface), i * LINEHEIGHT))

        self.surface.blit(self.score_surface,
                          (self.get_middle_x(self.score_surface, self.surface), self.height // 3))

    def render_score_txt_surfaces(self):
        # render score and the player scores as multiple lines rendered
        score_text_surfaces = []

        title = self.score_font.render(
            "Score", True, BLACK)
        score_text_surfaces.append(title)

        for key, val in self.svh.score.items():
            line = self.score_font.render(
                "Player{}: {}".format(key, val), True, BLACK)
            score_text_surfaces.append(line)

        return score_text_surfaces

    def get_middle_x(self, surface, parent):
        # get the x position that place surface in the middle of parent.
        inner_w, inner_h = surface.get_size()
        parent_w, parent_h = parent.get_size()
        return (parent_w - inner_w) // 2
