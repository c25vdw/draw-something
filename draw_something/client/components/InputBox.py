import pygame

INPUT_BG = (200, 200, 200)
INPUT_COLOR = (10, 10, 10)
MARGIN = 10


class InputBox:
    def __init__(self, screen, font_path):
        self.screen = screen
        self.container = pygame.Surface((100, 60))

        self.font = pygame.font.Font(font_path, 32)
        self.txt_surface = pygame.Surface((80, 40))
        self.default_txt = "..."
        self.txt = ""
        self.cached_txt = self.txt
        self.update("...")

    def draw(self):
        self.container.fill(INPUT_BG)
        self.container.blit(self.txt_surface, (MARGIN, MARGIN))

        self.screen.blit(self.container, self.get_container_pos())

    def update(self, input_txt):
        if self.cached_txt == input_txt:
            return

        if len(input_txt) < 1:
            txt = self.default_txt
        else:
            txt = input_txt
        self.cached_txt = txt

        self.txt_surface = self.font.render(txt, True, INPUT_COLOR)
        self.resize_container(*self.txt_surface.get_size())

    def resize_container(self, width, height):
        self.container = pygame.Surface(
            (width + 2 * MARGIN, height + 2 * MARGIN))

    def get_container_pos(self):
        screen_width, screen_height = self.screen.get_size()
        container_width, container_height = self.container.get_size()
        container_x = (screen_width - container_width) // 2
        container_y = (screen_height - 100)

        return (container_x, container_y)
