import sys
from math import radians, sin, cos
from random import randint
import pygame
from pygame.locals import Rect, QUIT, KEYDOWN, KEYUP, K_SPACE, K_LEFT, K_RIGHT, K_UP, K_DOWN

pygame.init()
pygame.key.set_repeat(5, 5)
SURFACE = pygame.display.set_mode((800, 800))
FPSCLOCK = pygame.time.Clock()
X = 0
Y = 1


class Drawable:
    def __init__(self, rect):
        self.rect = rect
        self.step = [0, 0]

    def move(self):
        rect = self.rect.center
        xpos = (rect[X] + self.step[X]) % 800
        ypos = (rect[Y] + self.step[Y]) % 800
        self.rect.center = (xpos, ypos)


class Rock(Drawable):
    def __init__(self, pos, size):
        super(Rock, self).__init__(Rect(0, 0, size, size))
        self.rect.center = pos
        self.image = pygame.image.load("./image/rock.png")
        self.theta = randint(0, 360)
        self.size = size
        self.power = 128 / size
        self.step[X] = cos(radians(self.theta)) * self.power
        self.step[Y] = sin(radians(self.theta)) * -self.power

    def draw(self):
        rotated = pygame.transform.rotozoom(self.image, self.theta, self.size / 64)
        rect = rotated.get_rect()
        rect.center = self.rect.center
        SURFACE.blit(rotated, rect)

    def tick(self):
        # 운석 이동
        self.theta += 3
        self.move()


class Shot(Drawable):
    """ 총알 오브젝트 """
    def __init__(self):
        super(Shot, self).__init__(Rect(0, 0, 6, 6))
        self.count = 40
        self.power = 10
        self.max_count = 40

    def draw(self):
        """ 총알을 그린다 """
        if self.count < self.max_count:
            pygame.draw.rect(SURFACE, (225, 225, 0), self.rect)

    def tick(self):
        """ 총알을 이동한다 """
        self.count += 1
        self.move()


class Ship(Drawable):
    def __init__(self):
        super(Ship, self).__init__(Rect(355, 370, 90, 60))
        self.theta = 0
        self.power = 0
        self.accel = 0
        self.explode = False
        self.image = pygame.image.load("./image/ship.png")
        self.bang = pygame.image.load("./image/bang.png")

    def draw(self):
        rotated = pygame.transform.rotate(self.image, self.theta)
        rect = rotated.get_rect()
        rect.center = self.rect.center
        SURFACE.blit(rotated, rect)
        if self.explode:
            SURFACE.blit(self.bang, rect)

    def tick(self):
        self.power += self.accel
        self.power *= 0.94
        self.accel *= 0.94
        self.step[X] = cos(radians(self.theta)) * self.power
        self.step[Y] = sin(radians(self.theta)) * -self.power
        self.move()


class Item(Drawable):
    def __init__(self, pos, size):
        super(Item, self).__init__(Rect(0, 0, size, size))
        self.rect.center = pos
        self.size = size
        self.image = pygame.image.load("./image/Item.png")
        self.theta = randint(0, 360)
        self.power = 10
        self.step[X] = cos(radians(self.theta)) * self.power
        self.step[Y] = sin(radians(self.theta)) * -self.power

    def draw(self):
        rotated = pygame.transform.rotozoom(self.image, self.theta, self.size / 64)
        rect = rotated.get_rect()
        rect.center = self.rect.center
        SURFACE.blit(rotated, rect)

    def tick(self):
        self.theta += 3
        self.move()


def key_event_handler(keymap, ship):
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if not event.key in keymap:
                keymap.append(event.key)
        elif event.type == KEYUP:
            keymap.remove(event.key)

        if K_LEFT in keymap:
            ship.theta += 5
        elif K_RIGHT in keymap:
            ship.theta -= 5
        elif K_UP in keymap:
            ship.accel = min(5, ship.accel + 0.2)
        elif K_DOWN in keymap:
            ship.accel = max(-5, ship.accel - 0.1)


def main():
    sysfont = pygame.font.SysFont(None, 72)
    scorefont = pygame.font.SysFont(None, 36)
    message_clear = sysfont.render("CLEARED", True, (0, 255, 255))
    message_over = sysfont.render("GAME OVER", True, (0, 255, 255))
    message_rect = message_clear.get_rect()
    message_rect.center = (400, 400)

    keymap = []
    shots = []
    rocks = []
    items = []
    ship = Ship()
    game_over = False
    score = 0
    back_x, back_y = 0, 0
    back_image = pygame.image.load("C:/Users/User/PycharmProjects/box/image/bg.png")
    back_image = pygame.transform.scale2x(back_image)
    bullet = 5

    while len(rocks) < 4:
        pos = randint(0, 800), randint(0, 800)
        rock = Rock(pos, 64)
        if not rock.rect.colliderect(ship.rect):
            rocks.append(rock)

    while len(items) < 4:
        pos = randint(0, 800), randint(0, 800)
        item = Item(pos, 6)
        if not item.rect.colliderect(ship.rect):
            items.append(item)

    while True:
        key_event_handler(keymap, ship)

        while len(shots) < bullet:
            shots.append(Shot())

        if not game_over:
            ship.tick()

            for item in items:
                item.tick()
                if item.rect.colliderect(ship.rect):
                    bullet += 2
                    items.remove(item)

            for rock in rocks:
                rock.tick()
                if rock.rect.colliderect(ship.rect):
                    ship.explode = True
                    game_over = True
            # 총알 이동
            fire = False
            for shot in shots:
                if shot.count < shot.max_count:
                    shot.tick()
                    hit2 = None

                    for item in items:
                        if item.rect.colliderect(shot.rect):
                            hit2 = item
                    if hit2 is not None:
                        bullet += 2
                        items.remove(hit2)
                        hit2 = None

                    hit = None
                    for rock in rocks:
                        if rock.rect.colliderect(shot.rect):
                            hit = rock
                    if hit != None:
                        score += hit.rect.width * 10
                        shot.count = shot.max_count
                        rocks.remove(hit)
                        if hit.rect.width > 16:
                            rocks.append(Rock(hit.rect.center, hit.rect.width / 2))
                            rocks.append(Rock(hit.rect.center, hit.rect.width / 2))
                        if len(rocks) == 0:
                            game_over = True


                elif not fire and K_SPACE in keymap:
                    shot.count = 0
                    shot.rect.center = ship.rect.center
                    shot_x = shot.power * cos(radians(ship.theta))
                    shot_y = shot.power * -sin(radians(ship.theta))
                    shot.step = (shot_x, shot_y)
                    fire = True

        back_x = (back_x + ship.step[X] / 2) % 1600
        back_y = (back_y + ship.step[Y] / 2) % 1600
        SURFACE.fill((0, 0, 0))
        SURFACE.blit(back_image, (-back_x, -back_y), (0, 0, 3200, 3200))

        ship.draw()
        for shot in shots:
            shot.draw()
        for rock in rocks:
            rock.draw()
        for item in items:
            item.draw()

        score_str = str(score).zfill(6)
        score_image = scorefont.render(score_str, True, (0, 255, 0))
        bullet_str = str("BULLET = "f'{bullet}').zfill(1)
        bullet_image = scorefont.render(bullet_str, True, (0, 255, 0))
        SURFACE.blit(score_image, (600, 10))
        SURFACE.blit(bullet_image, (400, 10))

        if game_over:
            if len(rocks) == 0:
                SURFACE.blit(message_clear, message_rect.topleft)
            else:
                SURFACE.blit(message_over, message_rect.topleft)

        pygame.display.update()
        FPSCLOCK.tick(20)


if __name__ == '__main__':
    main()
