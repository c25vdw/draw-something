import pygame
from settings import *

def parse_drag_event(event, mouseDown, prevPos):
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouseDown = True
        prevPos = pygame.mouse.get_pos()
    elif event.type == pygame.MOUSEBUTTONUP:
        if event.button == 1:
            mouseDown = False
            print("mouse up")
    return mouseDown, prevPos

def parse_input_event(event, event_hub):
    # event_hub: a EventHub instance for a client pygame.
    if event.key == pygame.K_RETURN:
        print("input: submitted answer\ninput: {}".format(event_hub.input_txt))
        event_hub.flush_input_to_client_answer()
        print("input: input cleared, your answer is {}".format(
            event_hub.input_txt, event_hub.client_answer))
    elif event.key == pygame.K_BACKSPACE:
        print("input: backspace.\ninput: {}".format(event_hub.input_txt))
        event_hub.input_txt = event_hub.input_txt[:-1]
    else:
        event_hub.input_txt += event.unicode
        print("input: receive {}".format(event_hub.input_txt))


def draw_the_drags_from_pos(pos, screen):
    if not pos:
        pos = [[0,0], [0,0]]
    # pos: [(x, y), (prev_x, prev_y)]
    # print(pos)
    if pos != [[None, None], [None, None]]:
        pygame.draw.line(screen, BLACK, pos[0], pos[1], LINEWIDTH)
        pygame.draw.circle(screen, BLACK, pos[1], BRUSHRADIUS, 0)
    
def update_cursors_from_mouseDown(mouseDown, prevPos, local_event_hub):
    """
        update prevPos, local_event_hub.
    """
    if mouseDown:
        (x, y) = pygame.mouse.get_pos()
        # update local cursor position
        local_event_hub.cur_pos = [(x, y), prevPos]
        prevPos = (x, y)
    else:
        local_event_hub.cur_pos = [(None, None), (None, None)]
    # some instant between this, server will be syncd, by svh.
    return prevPos

def draw_input_from_eh(input_txt, screen, font):
    # draw a rect over
    # TODO: make it look nicer and put on the right.
    screen.blit(font.render("", True, NAVYBLUE), (WIDTH/2, HEIGHT/2))
    txt_surface = font.render(input_txt, True, NAVYBLUE)
    screen.blit(txt_surface, (WIDTH/2, HEIGHT/2))