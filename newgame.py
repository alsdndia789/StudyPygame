import sys
import pygame
import math
from math import radians, sin, cos
from random import randint
from pygame.locals import QUIT, Rect, KEYDOWN, KEYUP, K_ESCAPE, K_DOWN, \
    K_RIGHT, K_LEFT, K_UP

WIDTH = 1000
HEIGHT = 800
GREEN = (0, 255, 0)
RED = (255, 0, 0)
pygame.init()
pygame.key.set_repeat(5, 5)
SURFACE = pygame.display.set_mode((WIDTH, HEIGHT))
FPSCLOCK = pygame.time.Clock()

moveUp = False
moveDown = False
moveLeft = False
moveRight = False


class item:
    def __init__(self, xpos, ypos, speed= 10, dir =0):
        self.xpos = xpos
        self.ypos = ypos
        self.speed = speed
        self.dir = dir
        self.rect = (self.xpos, self.ypos, 30, 30)

    def move_item(self):
        if self.dir == 1 and self.ypos < HEIGHT:
            self.ypos += self.speed
        if self.dir == 2 and self.ypos > 0:
            self.ypos -= self.speed
        if self.dir == 3 and self.xpos > 0:
            self.xpos -= self.speed
        if self.dir == 4 and self.xpos < WIDTH:
            self.xpos += self.speed

    def draw_item(self):
        pygame.draw.ellipse(SURFACE, GREEN,
                            Rect(self.xpos, self.ypos, 30, 30))

    def is_collide(self, xpos, ypos):
        return pygame.Rect(self.xpos, self.ypos, 30, 30).collidepoint(xpos, ypos)


def main():
    items = []
    moveUp = False
    moveDown = False
    moveLeft = False
    moveRight = False
    size = 50
    score = 0
    scorefont = pygame.font.SysFont(None, 36)
    xpos = 500
    ypos = 500
    speed = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                speed += 2
                if event.key == K_LEFT:
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT:
                    moveRight = True
                    moveLeft = False
                if event.key == K_UP:
                    moveUp = True
                    moveDown = False
                if event.key == K_DOWN:
                    moveUp = False
                    moveDown = True
            if event.type == KEYUP:
                speed = 0
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == K_LEFT:
                    moveLeft = False
                if event.key == K_RIGHT:
                    moveRight = False
                if event.key == K_UP:
                    moveUp = False
                if event.key == K_DOWN:
                    moveDown = False

        user = pygame.Rect(xpos, ypos, size, size)
        SURFACE.fill((0, 0, 0))
        while len(items) < 10:
            items.append(item(randint(0, WIDTH), randint(0, HEIGHT)))
        for ITEM in items:
            ITEM.dir = randint(1, 4)
            ITEM.draw_item()
            ITEM.move_item()

        vel = 15
        if moveDown and user.bottom < HEIGHT:
            vel += speed
            ypos += vel
        if moveUp and user.top > 0:
            vel += speed
            ypos -= vel
        if moveLeft and user.left > 0:
            vel += speed
            xpos -= vel
        if moveRight and user.right < WIDTH:
            vel += speed
            xpos += vel

        for ITEM in items:
            if user.colliderect(ITEM):
                items.remove(ITEM)
                score += 10
                size += 1

        score_str = str(score)
        score_image = scorefont.render(score_str, True, (0, 255, 0))
        SURFACE.blit(score_image, (600, 10))
        pygame.draw.rect(SURFACE, RED, user)
        pygame.display.update()
        FPSCLOCK.tick(20)


if __name__ == '__main__':
    main()