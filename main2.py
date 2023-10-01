from random import randint

import pygame as pg


def get_dist(a, b):
    return pg.math.Vector2(a[0], a[1]).distance_to((b[0], b[1]))


class NonMoleculeObject(pg.sprite.Sprite):
    def __init__(self, pos, radius, color=(100, 100, 100)):
        super().__init__()

        self.pos = list(pos)
        self.radius = radius
        self.color = color

        self.velocity_x = 0
        self.velocity_y = 0

        objects.add_internal(self)

    def check_collisions(self):
        collided = []
        for i in objects.sprites():
            if get_dist(self.pos, i.pos) < self.radius + i.radius and i != self:
                collided.append(i)

        for i in collided:
            i.pos[0] -= i.velocity_x
            i.pos[1] -= i.velocity_y

    def update_parameters(self):
        self.check_collisions()

    def update(self):
        self.update_parameters()
        pg.draw.circle(window, self.color, self.pos, self.radius)


class Molecule(pg.sprite.Sprite):
    def __init__(self, pos, radius, color=(100, 100, 100), speed=2):
        super().__init__()

        self.pos = list(pos)
        self.radius = radius
        self.color = color

        self.speed = speed
        self.velocity_x = 0
        self.velocity_y = 0

        objects.add_internal(self)

    def check_collisions(self):
        collided = []
        for i in objects.sprites():
            if get_dist(self.pos, i.pos) < self.radius + i.radius and i != self:
                collided.append(i)

        for i in collided:
            # self.pos[0] -= self.velocity_x
            # self.pos[1] -= self.velocity_y

            dist = get_dist(self.pos, i.pos)

            ratio_x = (self.pos[0] - i.pos[0]) / dist
            ratio_y = (self.pos[1] - i.pos[1]) / dist

            self.pos[0] += ratio_x * (i.radius + self.radius - dist)
            self.pos[1] += ratio_y * (i.radius + self.radius - dist)

        if self.pos[0]-self.radius < 0:
            self.pos[0] = self.radius
        elif self.pos[0]+self.radius > WIDTH:
            self.pos[0] = WIDTH - self.radius
        if self.pos[1]-self.radius < 0:
            self.pos[1] = self.radius
        elif self.pos[1]+self.radius > HEIGHT:
            self.pos[1] = HEIGHT - self.radius

    def reset(self):
        pass

    def follow(self, lst, coe):
        if len(lst) > 0:
            if self in lst:
                lst.remove(self)

            near = lst[0]
            for i in lst[1:]:
                if get_dist(self.pos, i.pos) < get_dist(self.pos, near.pos):
                    near = i
            ratio_x = (self.pos[0] - near.pos[0]) / get_dist(self.pos, near.pos)
            ratio_y = (self.pos[1] - near.pos[1]) / get_dist(self.pos, near.pos)

            self.velocity_x = self.speed * ratio_x * -coe
            self.velocity_y = self.speed * ratio_y * -coe

    def update_parameters(self):

        self.reset()

        self.check_collisions()

        self.pos[0] += self.velocity_x
        self.pos[1] += self.velocity_y


    def update(self):
        self.update_parameters()
        pg.draw.circle(window, self.color, self.pos, self.radius)


class RedMolecule(Molecule):
    def __init__(self, pos):
        super().__init__(pos, 10, (255, 0, 0), 1)
        red_mols.append(self)

    def reset(self):
        self.follow(blue_mols, -1)

class BlueMolecule(Molecule):
    def __init__(self, pos):
        super().__init__(pos, 10, (0, 0, 255), 1)
        blue_mols.append(self)

    def reset(self):
        self.follow(red_mols, 1)

WIDTH = 700
HEIGHT = 500
window = pg.display.set_mode((WIDTH, HEIGHT), pg.RESIZABLE)
pg.display.set_caption('Physic simulation')


objects = pg.sprite.Group()
red_mols = []
blue_mols = []

magnit = NonMoleculeObject((0, 0), 25)

for _ in range(10):
    RedMolecule((randint(0, WIDTH), randint(0, HEIGHT)))

for _ in range(10):
    BlueMolecule((randint(0, WIDTH), randint(0, HEIGHT)))

clock = pg.time.Clock()
FPS = 30

running = True

while running:

    for e in pg.event.get():
        if e.type == pg.QUIT:
            running = False

    magnit.pos = list(pg.mouse.get_pos())

    window.fill((255, 255, 255))

    objects.update()

    clock.tick(FPS)
    pg.display.update()
