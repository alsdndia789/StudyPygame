import sys
import math
import random
import pygame
from pygame.locals import QUIT, KEYDOWN, K_LEFT, K_RIGHT, Rect


class Block:

    def __init__(self, col, rect, speed=0, act=0):
        self.col = col
        self.rect = rect
        self.speed = speed
        self.dir = random.randint(-45, 45) + 270
        self.act = act

    def move(self):
        self.rect.centerx += math.cos(math.radians(self.dir)) * self.speed
        self.rect.centery -= math.sin(math.radians(self.dir)) * self.speed

    def draw(self):
        if self.speed == 0:
            pygame.draw.rect(SURFACE, self.col, self.rect)
        elif self.speed > 5:
            pygame.draw.ellipse(SURFACE, self.col, self.rect)


def move(self):
    global BLOCKS
    if self.act != 0:
        if self.rect.centery < 1000:
            self.move()

            # 블럭과 충돌
        numblock = len(BLOCKS)
        BLOCKS = [x for x in BLOCKS if not x.rect.colliderect(self.rect)]
        # 블럭의 개수가 달라졌으면 == 공이 블럭에 맞았으면
        if len(BLOCKS) != numblock:
            self.dir *= -1

            # 유저와 충돌
        if PADDLE.rect.colliderect(self.rect):
            self.dir = 90 + (PADDLE.rect.centerx - self.rect.centerx) / PADDLE.rect.width * 80

            # 벽과 충돌
        if self.rect.centerx < 0 or self.rect.centerx > 600:
            self.dir = 180 - self.dir
        if self.rect.centery < 0:
            self.dir *= -1
            self.speed = 15


pygame.init()
pygame.key.set_repeat(5, 5)
SURFACE = pygame.display.set_mode((600, 800))
FPSCLOCK = pygame.time.Clock()
BLOCKS = []
ITEMS = []
balls = []
PADDLE = Block((242, 242, 0), Rect(300, 700, 100, 30))
BALL1 = Block((242, 242, 0), Rect(300, 400, 20, 20), 10, 1)
while len(balls) < 4:
    balls.append(Block((242, 242, 0),
                       Rect(random.randint(100, 500), random.randint(100, 300),
                            20, 20), 10, 0))


def main():
    myfont = pygame.font.SysFont(None, 80)
    mess_clear = myfont.render("Cleared!", True, (255, 255, 0))
    mess_over = myfont.render("Game Over!", True, (255, 255, 0))
    colors = [(255, 0, 0), (255, 165, 0), (242, 242, 0), (0, 128, 0),
              (128, 0, 128), (0, 0, 250)]

    for ypos, color in enumerate(colors, start=0):
        for xpos in range(0, 5):
            BLOCKS.append(Block(color, Rect(xpos * 100 + 60, ypos * 50 + 40, 80, 30)))

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_LEFT and PADDLE.rect.centerx > 0:
                    PADDLE.rect.centerx -= 14
                elif event.key == K_RIGHT and PADDLE.rect.centerx < 600:
                    PADDLE.rect.centerx += 14

        SURFACE.fill((0, 0, 0))
        BALL1.draw()
        move(BALL1)
        for BALL in balls:
            BALL.draw()
            if BALL.rect.colliderect(BALL1.rect):
                BALL.act = 1
            move(BALL)
        PADDLE.draw()
        for block in BLOCKS:
            block.draw()

            if len(BLOCKS) == 0:
                SURFACE.blit(mess_clear, (200, 400))
            for BALL in balls:
                if BALL1.rect.centery > 800 and len(BLOCKS) > 0 and\
                        ((BALL.act != 0 and BALL.rect.centery > 800) or (BALL.act == 0 and BALL.rect.centery < 800)):
                    SURFACE.blit(mess_over, (150, 400))

        pygame.display.update()
        FPSCLOCK.tick(40)


if __name__ == '__main__':
    main()
