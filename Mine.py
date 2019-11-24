from math import floor
from random import randint

import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN

WIDTH, HEIGHT, SIZE = 20, 15, 50
NUM_OF_LEFT_BOMBS = NUM_OF_BOMBS = 30
EMPTY, BOMB, OPENED, EMPTY_FLAG, BOMB_FLAG, = 0, 1, 2, 3, 4
OPEN_COUNT = 0
CHECKED = [[0]*WIDTH for _ in range(HEIGHT)]

start_ticks = pygame.time.get_ticks()
pygame.init()
SURFACE = pygame.display.set_mode((WIDTH * SIZE, HEIGHT * SIZE))
FPSCLOCK = pygame.time.Clock()


def num_of_bomb(field, x_pos, y_pos):
    count = 0
    for yoffset in [-1, 0, 1]:
        for xoffset in [-1, 0, 1]:
            xpos, ypos = (x_pos + xoffset, y_pos + yoffset)
            if 0 <= xpos < WIDTH and 0 <= ypos < HEIGHT and field[ypos][xpos] == BOMB:
                count += 1
            elif 0 <= xpos < WIDTH and 0 <= ypos < HEIGHT and field[ypos][xpos] == BOMB_FLAG:
                count += 1
            elif 0 <= xpos < WIDTH and 0 <= ypos < HEIGHT and field[ypos][xpos] == EMPTY_FLAG:
                count += 1
    return count


def flag_tile(field, x_pos, y_pos):
    global NUM_OF_LEFT_BOMBS
    if field[y_pos][x_pos] == EMPTY_FLAG:
        NUM_OF_LEFT_BOMBS += 1
        field[y_pos][x_pos] = EMPTY

    elif field[y_pos][x_pos] == BOMB_FLAG:
        NUM_OF_LEFT_BOMBS += 1
        field[y_pos][x_pos] = BOMB

    elif field[y_pos][x_pos] == EMPTY:
        NUM_OF_LEFT_BOMBS -= 1
        field[y_pos][x_pos] = EMPTY_FLAG

    elif field[y_pos][x_pos] == BOMB:
        NUM_OF_LEFT_BOMBS -= 1
        field[y_pos][x_pos] = BOMB_FLAG


def open_tile(field, x_pos, y_pos):
    global OPEN_COUNT
    if CHECKED[y_pos][x_pos]:
        return

    CHECKED[y_pos][x_pos] = True

    for yoffset in [-1, 0, 1]:
        for xoffset in [-1, 0, 1]:
            xpos, ypos = (x_pos + xoffset, y_pos + yoffset)
            if 0 <= xpos < WIDTH and 0 <= ypos < HEIGHT and field[ypos][xpos] == EMPTY:
                field[ypos][xpos] = OPENED
                OPEN_COUNT += 1
                count = num_of_bomb(field, xpos, ypos)
                if count == 0 and not (xpos == x_pos and ypos == y_pos):
                    open_tile(field, xpos, ypos)


def main():
    smallfont = pygame.font.SysFont(None, 36)
    largefont = pygame.font.SysFont(None, 72)
    message_clear = largefont.render("!!CLEARED!!", True, (0, 255, 255))
    message_over = largefont.render("GAME OVER", True, (0, 255, 255))
    message_rect = message_clear.get_rect()
    message_rect.center = (WIDTH * SIZE / 2, HEIGHT * SIZE / 2)
    game_over = False

    field = [[EMPTY] * WIDTH for _ in range(HEIGHT)]
    count = 0
    while count < NUM_OF_BOMBS:
        xpos, ypos = randint(0, WIDTH - 1), randint(0, HEIGHT - 1)
        if field[ypos][xpos] == EMPTY:
            field[ypos][xpos] = BOMB
            count += 1

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                xpos, ypos = floor(event.pos[0] / SIZE), floor(event.pos[1] / SIZE)
                if field[ypos][xpos] == BOMB:
                    game_over = True
                elif field[ypos][xpos] == EMPTY:
                    open_tile(field, xpos, ypos)

            elif event.type == MOUSEBUTTONDOWN and event.button == 3:  # and 깃발이 없으면
                xpos, ypos = floor(event.pos[0] / SIZE), floor(event.pos[1] / SIZE)
                flag_tile(field, xpos, ypos)
        seconds = (pygame.time.get_ticks() - start_ticks) / 1000
        score = OPEN_COUNT

        SURFACE.fill((0, 0, 0))

        for ypos in range(HEIGHT):
            for xpos in range(WIDTH):
                tile = field[ypos][xpos]
                rect = (xpos * SIZE, ypos * SIZE, SIZE, SIZE)

                if tile == EMPTY or tile == BOMB:
                    pygame.draw.rect(SURFACE, (192, 192, 192), rect)
                    if game_over and tile == BOMB:
                        pygame.draw.ellipse(SURFACE, (225, 225, 0), rect)
                elif tile == EMPTY_FLAG or tile == BOMB_FLAG:
                    pygame.draw.rect(SURFACE, (0, 255, 0), rect)


                elif tile == OPENED or BOMB_FLAG or EMPTY_FLAG:
                    count = num_of_bomb(field, xpos, ypos)

                    if count > 0:
                        num_image = smallfont.render(""f'{count}', True, (255, 255, 0))
                        SURFACE.blit(num_image, (xpos * SIZE + 10, ypos * SIZE + 10))

        for index in range(0, WIDTH * SIZE, SIZE):
            pygame.draw.line(SURFACE, (96, 96, 96), (index, 0), (index, HEIGHT * SIZE))
            for index in range(0, HEIGHT * SIZE, SIZE):
                pygame.draw.line(SURFACE, (96, 96, 96), (0, index), (WIDTH * SIZE, index))

        if OPEN_COUNT == WIDTH * HEIGHT - NUM_OF_BOMBS:
            SURFACE.blit(message_clear, message_rect.topleft)
        elif game_over:
            SURFACE.blit(message_over, message_rect.topleft)

        message_score = smallfont.render("BOMB = "f'{NUM_OF_LEFT_BOMBS}', True, (0, 255, 255))
        message_time = smallfont.render("TIME = "f'{int(seconds)}', True, (0, 255, 255))
        SURFACE.blit(message_score, (WIDTH * SIZE / 2, 0))
        if not game_over:
            SURFACE.blit(message_time, (WIDTH * SIZE - 200, 0))

        pygame.display.update()
        FPSCLOCK.tick(10)


if __name__ == '__main__':
    main()
