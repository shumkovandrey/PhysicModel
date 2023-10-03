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
            if get_dist(self.pos, i.pos) < self.radius+0.5*self.radius + i.radius+0.5*i.radius and i != self:
                collided.append(i)

        for i in collided:
            # i.pos[0] -= i.velocity_x
            # i.pos[1] -= i.velocity_y
            dist = get_dist(self.pos, i.pos)

            ratio_x = (i.pos[0] - self.pos[0]) / dist if dist != 0 else 1
            ratio_y = (i.pos[1] - self.pos[1]) / dist if dist != 0 else 1

            i.pos[0] += ratio_x * (self.radius + 0.5 * self.radius + i.radius + 0.5 * i.radius - dist)
            i.pos[1] += ratio_y * (self.radius + 0.5 * self.radius + i.radius + 0.5 * i.radius - dist)

    def update_parameters(self):
        self.check_collisions()

    def update(self):
        self.update_parameters()
        pg.draw.circle(window, self.color, (self.pos[0]+offset_x, self.pos[1]+offset_y), self.radius)


class Molecule(pg.sprite.Sprite):
    def __init__(self, pos, color=(100, 100, 100), speed=2, power=120, radius=6):
        super().__init__()

        self.pos = list(pos)
        self.radius = radius
        self.color = color

        self.speed = speed
        self.velocity_x = 0
        self.velocity_y = 0
        self.power = power

        self.collided = []

        objects.add_internal(self)

    def check_collisions(self):
        collided = []
        for i in objects.sprites():
            if get_dist(self.pos, i.pos) < self.radius+0.5*self.radius + i.radius+0.5*i.radius and i != self:
                collided.append(i)

        self.collided = collided

        for i in collided:
            # self.pos[0] -= self.velocity_x
            # self.pos[1] -= self.velocity_y

            dist = get_dist(self.pos, i.pos)

            ratio_x = (self.pos[0] - i.pos[0]) / dist if dist != 0 else 1
            ratio_y = (self.pos[1] - i.pos[1]) / dist if dist != 0 else 1

            self.pos[0] += ratio_x * (i.radius+0.5*i.radius + self.radius+0.5*self.radius - dist)
            self.pos[1] += ratio_y * (i.radius+0.5*i.radius + self.radius+0.5*self.radius - dist)

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

        lst = lst.copy()
        if self in lst:
            lst.remove(self)

        if len(lst) > 0:
            near = lst[0]
            near_mols = []
            for i in lst[1:]:
                if abs(get_dist(self.pos, i.pos) - get_dist(self.pos, near.pos)) < 3:
                    near_mols.append(i)
                if get_dist(self.pos, i.pos) < get_dist(self.pos, near.pos):
                    near = i

            if not near_mols:
                near_mols = [near]

            for i in near_mols:
                if get_dist(self.pos, i.pos) <= self.power:
                    ratio_x = (self.pos[0] - i.pos[0]) / get_dist(self.pos, i.pos)
                    ratio_y = (self.pos[1] - i.pos[1]) / get_dist(self.pos, i.pos)

                    if get_dist(self.pos, i.pos) >= (i.radius+0.5*i.radius + self.radius+0.5*self.radius + 2):
                        self.velocity_x += self.speed * ratio_x * -coe
                        self.velocity_y += self.speed * ratio_y * -coe
                        i.velocity_x += i.speed * ratio_x * coe
                        i.velocity_y += i.speed * ratio_y * coe
            # else:
            #     self.velocity_x += self.speed * randint(-2, 2)
            #     self.velocity_y += self.speed * randint(-2, 2)


    def update_parameters(self):

        if not is_pause:
            self.reset()

            self.check_collisions()

        self.pos[0] += self.velocity_x
        self.pos[1] += self.velocity_y

        self.velocity_x = 0
        self.velocity_y = 0


    def update(self):
        self.update_parameters()
        pg.draw.circle(window, self.color, (self.pos[0]+offset_x, self.pos[1]+offset_y), self.radius)


class RedMolecule(Molecule):
    def __init__(self, pos):
        super().__init__(pos, (255, 0, 0), 1)
        red_mols.append(self)

    def reset(self):
        self.follow(red_mols, 1)

class BlueMolecule(Molecule):
    def __init__(self, pos):
        super().__init__(pos, (0, 0, 255), 2)
        blue_mols.append(self)

    def reset(self):
        pass
        self.follow(red_mols, 1)

class YellowMolecule(Molecule):
    def __init__(self, pos):
        super().__init__(pos, (0,0,0), 1)
        yellow_mols.append(self)

    def reset(self):
        pass
        self.follow(red_mols, 1)
        self.follow(blue_mols, -1)


WIDTH = 700
HEIGHT = 500
window = pg.display.set_mode((WIDTH, HEIGHT), pg.RESIZABLE)
pg.display.set_caption('Physic simulation')


objects = pg.sprite.Group()
red_mols = []
blue_mols = []
yellow_mols = []

magnit = NonMoleculeObject((0, 0), 20)
objects.remove_internal(magnit)
is_visible = False

for _ in range(100):
    RedMolecule((randint(0, WIDTH), randint(0, HEIGHT)))

# for _ in range(50):
#     BlueMolecule((randint(0, WIDTH), randint(0, HEIGHT)))
#
# for _ in range(50):
#     YellowMolecule((randint(0, WIDTH), randint(0, HEIGHT)))

clock = pg.time.Clock()
FPS = 60

offset_x = 0
offset_y = 0
is_pause = False

running = True

while running:

    for e in pg.event.get():
        if e.type == pg.QUIT:
            running = False
        if e.type == pg.MOUSEBUTTONDOWN:
            RedMolecule((pg.mouse.get_pos()[0]-offset_x, pg.mouse.get_pos()[1]-offset_y))
        if e.type == pg.KEYDOWN:
            if e.key == pg.K_q:
                is_visible = not is_visible
                if not is_visible:
                    objects.remove_internal(magnit)
                else:
                    objects.add_internal(magnit)
            if e.key == pg.K_p:
                is_pause = not is_pause
    key_pressed = pg.key.get_pressed()
    if key_pressed[pg.K_a]:
        offset_x += 500 * 1/FPS
    elif key_pressed[pg.K_d]:
        offset_x -= 500 * 1/FPS
    if key_pressed[pg.K_w]:
        offset_y += 500 * 1/FPS
    elif key_pressed[pg.K_s]:
        offset_y -= 500 * 1/FPS

    magnit.pos = [pg.mouse.get_pos()[0]-offset_x, pg.mouse.get_pos()[1]-offset_y]


    window.fill((255, 255, 255))

    objects.update()

    clock.tick(FPS)
    pg.display.update()
