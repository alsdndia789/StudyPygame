import random
import pygame
from pygame import mixer
from pygame.locals import QUIT, KEYDOWN, K_LEFT, K_RIGHT, K_UP, \
    K_DOWN, K_SPACE, Rect

pygame.init()
SURFACE = pygame.display.set_mode((600, 600))
FPSCLOCK = pygame.time.Clock()

mixer.init()
mixer.music.load("C:/Users/User/PycharmProjects/untitled2/Escape.mp3")
mixer.music.play(-1)
FOODS = []
SNAKE = []
BOMBS = []
ENEMY = []
(W, H) = (20, 20)


def add_food():
    while True:
        pos = (random.randint(0, W - 1), random.randint(0, H - 1))
        if pos in FOODS or pos in SNAKE:
            continue
        FOODS.append(pos)
        break


def add_bomb():
    while True:
        pos = (random.randint(0, W - 1), random.randint(0, H - 1))
        if pos in FOODS or pos in SNAKE or pos in BOMBS:
            continue
        BOMBS.append(pos)
        break


def move_food(pos):
    i = FOODS.index(pos)
    del FOODS[i]
    add_food()


def paint(message):
    SURFACE.fill((0, 0, 0))
    for food in FOODS:
        pygame.draw.ellipse(SURFACE, (0, 255, 0),
                            Rect(food[0] * 30, food[1] * 30, 30, 30))
    for bomb in BOMBS:
        pygame.draw.ellipse(SURFACE, (255, 0, 0),
                            Rect(bomb[0] * 30, bomb[1] * 30, 30, 30))
    for body in SNAKE:
        pygame.draw.rect(SURFACE, (0, 255, 255),
                         Rect(body[0] * 30, body[1] * 30, 30, 30))
    for enemy in ENEMY:
        pygame.draw.rect(SURFACE, (255, 30, 30),
                         Rect(enemy[0] * 30, enemy[1] * 30, 30, 30))
    for index in range(20):
        pygame.draw.line(SURFACE, (64, 64, 64), (index * 30, 0),
                         (index * 30, 600))
        pygame.draw.line(SURFACE, (64, 64, 64), (0, index * 30),
                         (600, index * 30))
    if message is not None:
        SURFACE.blit(message, (150, 300))

    smallfont = pygame.font.SysFont(None, 36)
    message_score = smallfont.render("SCORE = {}".format(len(SNAKE)), True, (0, 255, 255))
    SURFACE.blit(message_score, (250, 0))

    pygame.display.update()


def main():
    myfont = pygame.font.SysFont(None, 80)
    key = K_DOWN
    message = None
    speed = 40
    game_over = False
    SNAKE.append((int(W / 2), int(H / 2)))
    ENEMY.append((int(W / 4), int(H / 4)))
    for _ in range(10):
        add_food()
    for _ in range(3):
        add_bomb()

    while True:
        move = random.randint(1, 4)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                key = event.key

        if not game_over:
            # user snake
            if key == K_LEFT:
                head = (SNAKE[0][0] - 1, SNAKE[0][1])
            elif key == K_RIGHT:
                head = (SNAKE[0][0] + 1, SNAKE[0][1])
            elif key == K_UP:
                head = (SNAKE[0][0], SNAKE[0][1] - 1)
            elif key == K_DOWN:
                head = (SNAKE[0][0], SNAKE[0][1] + 1)
            elif key == K_SPACE:
                game_over = True

            ## computer snake
            if move == 1 and ENEMY[0][0] > 0:
                head1 = (ENEMY[0][0] - 1, ENEMY[0][1])
            if move == 2 and ENEMY[0][0] < W:
                head1 = (ENEMY[0][0] + 1, ENEMY[0][1])
            if move == 3 and ENEMY[0][1] > 0:
                head1 = (ENEMY[0][0], ENEMY[0][1] - 1)
            if move == 4 and ENEMY[0][1] < H:
                head1 = (ENEMY[0][0], ENEMY[0][1] + 1)

            ## speed limit
            if speed < 150:
                speed += 1


            if head in SNAKE or \
                    head[0] < 0 or head[0] >= W or \
                    head[1] < 0 or head[1] >= H or \
                    head in BOMBS or head in ENEMY:
                message = myfont.render("GAME OVER!", True, (255, 255, 0))
                game_over = True

            SNAKE.insert(0, head)
            ENEMY.insert(0, head1)
            if head in FOODS:
                move_food(head)
            else:
                SNAKE.pop()
                ENEMY.pop()
        paint(message)
        FPSCLOCK.tick(speed / 10)


if __name__ == '__main__':
    main()
