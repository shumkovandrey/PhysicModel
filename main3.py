from random import randint

import pygame as pg


def get_dist(a, b):
    return pg.math.Vector2(a[0], a[1]).distance_to((b[0], b[1]))

class GameObject(pg.sprite.Sprite):
    def __init__(self, pos, size, is_kinematic=True, color=(0, 255, 0), speed=2):
        super().__init__()

        self.pos = list(pos)
        self.size = size
        self.color = color
        self.last_pos = list(pos)
        self.is_kinematic = is_kinematic


        self.rect = pg.Rect(pos[0]-size[0]//2, pos[1]-size[1]//2, *size)
        self.speed = speed
        self.velocity_x = 0
        self.velocity_y = 0
        self.last_velocity = [0, 0]
        self.is_falling = True

        objects.add_internal(self)

    def check_collisions(self):
        hits = pg.sprite.spritecollide(self, objects.sprites(), False)
        hits.remove(self)
        if len(hits) == 0 and not self.is_kinematic:
            self.is_falling = True
        for i in hits:
            x = i.pos[0] - self.pos[0]
            y = i.pos[1] - self.pos[1]
            inside_rect = pg.rect.Rect(i.pos[0] - i.size[0]//2 + 10, i.pos[1] - i.size[1]//2 + 10, i.size[0]-20, i.size[1]-20)
            pg.draw.rect(window, (0, 0, 0), inside_rect)
            if (x > 0 and self.velocity_x > 0 or x < 0 and self.velocity_x < 0) and abs(y)+1 < i.size[1]//2+self.size[1]//2 - self.speed:
                self.pos[0] -= self.velocity_x
                self.pos[0] -= (x//abs(x)) * (self.rect.clip(i.rect).width-1)
                self.velocity_x = 0
            if (y > 0 and self.velocity_y > 0 or y < 0 and self.velocity_y < 0) and abs(x)+1 < i.size[0]//2+self.size[0]//2 - self.speed:
                self.pos[1] -= self.velocity_y
                self.pos[1] -= (y//abs(y)) * (self.rect.clip(i.rect).height-1)
                self.velocity_y = 0
                if y > 0 and not self.is_kinematic:
                    self.is_falling = False
            if self.rect.colliderect(inside_rect) and not self.is_kinematic:
                if (x > 0 or x < 0) and abs(y)+1 < i.size[1] // 2 + self.size[1] // 2:
                    self.pos[0] -= self.last_velocity[0]
                    x = i.pos[0] - self.pos[0]
                    self.pos[0] -= (x // abs(x)) * (self.rect.clip(i.rect).width - 1)
                    print("x", self.velocity_x, x//abs(x), self.rect.clip(i.rect).width - 1)
                if (y > 0 or y < 0) and abs(x)+1 < i.size[0] // 2 + self.size[0] // 2:
                    self.pos[1] -= self.last_velocity[1]
                    y = i.pos[1] - self.pos[1]
                    self.pos[1] -= (y // abs(y)) * (self.rect.clip(i.rect).height - 1)
                    print("y", self.velocity_y, y//abs(y), self.rect.clip(i.rect).height - 1)

    def reset(self):
        pass

    def update_parameters(self):
        # self.velocity_x = randint(-2, 2) * self.speed
        # self.velocity_y = randint(-2, 2) * self.speed
        self.reset()

        self.pos[0] += self.velocity_x
        self.pos[1] += self.velocity_y

        if self.velocity_x != 0:
            self.last_velocity[0] = self.velocity_x
        if self.velocity_y != 0:
            self.last_velocity[1] = self.velocity_y

        self.check_collisions()


        self.last_pos = self.pos.copy()
        self.rect.x, self.rect.y = (self.pos[0]-self.size[0]//2, self.pos[1]-self.size[1]//2)

    def update(self):
        self.update_parameters()
        pg.draw.rect(window, self.color, self.rect, width=1)
        pg.draw.circle(window, (255, 0, 0), self.pos, 2)


class Player(GameObject):
    def reset(self):
        if self.is_falling:
            self.velocity_y += 0.09
        pass


WIDTH = 700
HEIGHT = 500
window = pg.display.set_mode((WIDTH, HEIGHT), pg.RESIZABLE)
pg.display.set_caption('Physic simulation')


objects = pg.sprite.Group()


mol1 = Player((300, 100), (25, 25), is_kinematic=False)
mol2 = GameObject((300, 300), (50, 100))
mol3 = GameObject((375, 300), (50, 100))
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
    if key_pressed[pg.K_w] and not mol1.is_falling:
        mol1.velocity_y = -mol1.speed
    elif key_pressed[pg.K_q]:
        mol1.velocity_y = -mol1.speed
    elif key_pressed[pg.K_s]:
        mol1.velocity_y = mol1.speed

    window.fill((255, 255, 255))

    objects.update()

    clock.tick(FPS)
    pg.display.update()
