from random import randint

import pygame as pg


def get_dist(a, b):
    return pg.math.Vector2(a[0], a[1]).distance_to((b[0], b[1]))


class Object(pg.sprite.Sprite):
    def __init__(self, pos, size, color=(0, 255, 0), speed=2):
        super().__init__()

        self.pos = list(pos)
        self.size = size
        self.color = color
        self.last_pos = list(pos)

        self.rect = pg.Rect(pos[0]-size[0]//2, pos[1]-size[1]//2, *size)
        self.speed = speed
        self.velocity_x = 0
        self.velocity_y = 0

        objects.add_internal(self)

    def check_collisions(self):
        hits = pg.sprite.spritecollide(self, objects.sprites(), False)
        hits.remove(self)
        for i in hits:
            x = i.pos[0] - self.pos[0]
            y = i.pos[1] - self.pos[1]
            inside_rect = pg.rect.Rect(i.pos[0] - i.size[0]//2 + 10, i.pos[1] - i.size[1]//2 + 10, i.size[0]-20, i.size[1]-20)
            pg.draw.rect(window, (0, 0, 0), inside_rect)
            if (x > 0 and self.velocity_x > 0 or x < 0 and self.velocity_x < 0) and abs(y) < i.size[1]//2+self.size[1]//2 - self.speed:
                self.pos[0] -= self.velocity_x
                self.velocity_x = 0
            if (y > 0 and self.velocity_y > 0 or y < 0 and self.velocity_y < 0) and abs(x) < i.size[0]//2+self.size[0]//2 - self.speed:
                self.pos[1] -= self.velocity_y
                self.velocity_y = 0

            if self.rect.colliderect(inside_rect):
                if (x > 0 and self.velocity_x > 0 or x < 0 and self.velocity_x < 0) and abs(y) < i.size[1] // 2 + self.size[1] // 2:
                    self.pos[0] -= self.velocity_x
                    self.velocity_x = 0
                if (y > 0 and self.velocity_y > 0 or y < 0 and self.velocity_y < 0) and abs(x) < i.size[0] // 2 + self.size[0] // 2:
                    self.pos[1] -= self.velocity_y
                    self.velocity_y = 0

            # x = i.pos[0] - self.pos[0]
            # y = i.pos[1] - self.pos[1]
            # if x != 0 and y != 0:
            #     last_x = i.pos[0] - self.last_pos[0]
            #     last_y = i.pos[1] - self.last_pos[1]
            #     r_x, r_y = self.rect.clip(i.rect).width, self.rect.clip(i.rect).height
            #     pg.draw.circle(window, (0, 0, 0), (self.pos[0] - (x//abs(x)) * r_x, self.pos[1]), 2)
            #     a = (self.pos[0] - self.size[0]//2 - (x//abs(x)) * r_x, self.pos[1] - self.size[1]//2)
            #     b = (self.pos[0] - self.size[0]//2, self.pos[1] - self.size[1]//2 - (y//abs(y)) * r_y)
            #
            #
            #     if get_dist(a, self.last_pos) < get_dist(b, self.last_pos):
            #         relation = (self.pos[0] - self.last_pos[0]) / (self.pos[1] - self.last_pos[1]) if (self.pos[1] - self.last_pos[1]) != 0 else 0
            #         self.pos[0] -= (x // abs(x)) * r_x
            #         self.pos[1] -= (x // abs(x)) * r_x * relation
            #     else:
            #         relation = (self.pos[1] - self.last_pos[1]) / (self.pos[0] - self.last_pos[0]) if (self.pos[0] - self.last_pos[0]) != 0 else 0
            #         self.pos[1] -= (y // abs(y)) * r_y
            #         self.pos[0] -= (y // abs(y)) * r_y * relation


        if self.rect.x <= 0:
            self.rect.x = 0
        elif self.rect.right >= WIDTH:
            self.rect.x = WIDTH - self.rect.width
        if self.rect.y <= 0:
            self.rect.y = 0
        elif self.rect.bottom >= HEIGHT:
            self.rect.y = HEIGHT - self.rect.height
        return len(hits) > 0


    def update_parameters(self):
        # self.velocity_x = randint(-2, 2) * self.speed
        # self.velocity_y = randint(-2, 2) * self.speed

        self.pos[0] += self.velocity_x
        self.pos[1] += self.velocity_y

        self.check_collisions()

        self.last_pos = self.pos.copy()
        self.rect.x, self.rect.y = (self.pos[0]-self.size[0]//2, self.pos[1]-self.size[1]//2)

    def update(self):
        self.update_parameters()
        pg.draw.rect(window, self.color, self.rect, width=1)
        pg.draw.circle(window, (255, 0, 0), self.pos, 2)


WIDTH = 700
HEIGHT = 500
window = pg.display.set_mode((WIDTH, HEIGHT), pg.RESIZABLE)
pg.display.set_caption('Physic simulation')


objects = pg.sprite.Group()


mol1 = Object((100, 100), (25, 25))
mol2 = Object((300, 300), (50, 100))
mol3 = Object((375, 300), (50, 100))
clock = pg.time.Clock()
FPS = 60

running = True

while running:

    for e in pg.event.get():
        if e.type == pg.QUIT:
            running = False

    key_pressed = pg.key.get_pressed()
    if key_pressed[pg.K_a]:
        mol1.velocity_x = -mol1.speed
    elif key_pressed[pg.K_d]:
        mol1.velocity_x = mol1.speed
    else:
        mol1.velocity_x = 0
    if key_pressed[pg.K_w]:
        mol1.velocity_y = -mol1.speed
    elif key_pressed[pg.K_s]:
        mol1.velocity_y = mol1.speed
    else:
        mol1.velocity_y = 0

    window.fill((255, 255, 255))

    objects.update()

    clock.tick(FPS)
    pg.display.update()
