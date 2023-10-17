from random import randint

import pygame as pg


def get_dist(a, b):
    return pg.math.Vector2(a[0], a[1]).distance_to((b[0], b[1]))

class Property:
    def __init__(self):
        self.parent = None

    def update(self):
        pass


class GameObject(pg.sprite.Sprite):
    def __init__(self, pos, size, properties, color=(0, 255, 0), speed=2):
        super().__init__()

        self.pos = list(pos)
        self.last_pos = self.pos.copy()
        self.size = size
        self.color = color
        self.properties = {}
        for i in properties:
            i.parent = self
            self.properties[type(i)] = i

        self.rect = pg.Rect(pos[0]-size[0]//2, pos[1]-size[1]//2, *size)
        self.speed = speed
        self.velocity_x = 0
        self.velocity_y = 0
        self.last_velocity = [0, 0]
        self.collided = []

        objects.add_internal(self)

    def reset(self):
        pass

    def update_parameters(self):
        # self.velocity_x = randint(-2, 2) * self.speed
        # self.velocity_y = randint(-2, 2) * self.speed
        self.collided = pg.sprite.spritecollide(self, objects.sprites(), False)
        self.collided.remove(self)

        self.reset()

        self.last_pos = self.pos.copy()
        self.pos[0] += self.velocity_x
        self.pos[1] += self.velocity_y

        for prop in self.properties.values():
            prop.update()

        if self.velocity_x != 0:
            self.last_velocity[0] = self.velocity_x
        if self.velocity_y != 0:
            self.last_velocity[1] = self.velocity_y

        self.rect.x, self.rect.y = (self.pos[0]-self.size[0]//2, self.pos[1]-self.size[1]//2)

    def update(self):
        self.update_parameters()
        pg.draw.rect(window, self.color, pg.rect.Rect(self.rect.x-camera_x, self.rect.y-camera_y, self.size[0], self.size[1]), width=1)
        pg.draw.rect(window, (0, 0, 255), pg.rect.Rect(self.last_pos[0]-self.size[0]//2-camera_x, self.last_pos[1]-self.size[1]//2-camera_y, self.size[0], self.size[1]), width=1)
        pg.draw.circle(window, (255, 0, 0) if self.properties[PhysicBody].is_falling else (0, 255, 0), (self.pos[0]-camera_x, self.pos[1]-camera_y), 2)


class PhysicBody(Property):
    def __init__(self, mass=1000, is_kinematic=False, gravity=0.09):
        super().__init__()
        self.is_kinematic = is_kinematic
        self.is_falling = True
        self.gravity = gravity
        self.mass = mass

    def update(self):
        par = self.parent

        hits = pg.sprite.spritecollide(par, objects.sprites(), False)
        hits.remove(par)
        if len(hits) == 0 and not self.is_kinematic:
            self.is_falling = True

        for i in hits:
            if PhysicBody not in i.properties:
                continue

            x = i.pos[0] - par.pos[0]
            y = i.pos[0] - par.pos[0]
            koef_x = x // abs(x) if x != 0 else 0
            koef_y = y // abs(y) if y != 0 else 0


            if i.properties[PhysicBody].mass < self.mass:
                i.pos[0] += par.velocity_x * min(1, self.mass/i.properties[PhysicBody].mass)
                i.pos[1] += par.velocity_y * min(1, self.mass/i.properties[PhysicBody].mass)
                i_hits = i.collided.copy()
                if par in i_hits:
                    i_hits.remove(par)
                if len(i_hits) > 0:
                    i.pos[0] -= par.velocity_x * min(1, self.mass / i.properties[PhysicBody].mass) + koef_x
                    i.pos[1] -= par.velocity_y * min(1, self.mass / i.properties[PhysicBody].mass) + koef_y
            if i.properties[PhysicBody].mass > self.mass:
                par.pos[0] += i.velocity_x * min(1, i.properties[PhysicBody].mass/self.mass)
                par.pos[1] += i.velocity_y * min(1, i.properties[PhysicBody].mass/self.mass)
                par_hits = par.collided.copy()
                if i in par_hits:
                    par_hits.remove(i)
                if len(par_hits) > 0:
                    par.pos[0] -= i.velocity_x * min(1, i.properties[PhysicBody].mass / self.mass) + koef_x
                    par.pos[1] -= i.velocity_y * min(1, i.properties[PhysicBody].mass / self.mass) + koef_y

        for i in hits:
            global a
            if PhysicBody not in i.properties:
                continue
            x = i.pos[0] - par.pos[0]
            y = i.pos[0] - par.pos[0]
            koef_x = x//abs(x) if x != 0 else 0
            koef_y = y//abs(y) if y != 0 else 0

            if not (par.velocity_x == 0 and par.velocity_y == 0):
                if abs(par.velocity_x) >= abs(par.velocity_y):
                    vel_x = par.velocity_x//abs(par.velocity_x) if par.velocity_x != 0 else 0
                    ratio_vel = par.velocity_y/par.velocity_x if par.velocity_x != 0 else 0
                    vel_y = vel_x * ratio_vel
                    vel_rect = pg.rect.Rect(par.pos[0]-par.size[0]//2, par.pos[1]-par.size[1]//2, par.size[0], par.size[1])
                    while vel_rect.colliderect(i.rect):
                        vel_rect.x -= vel_x
                        vel_rect.y -= vel_y
                        pg.draw.rect(window, (0, 0, 0), vel_rect)
                    par.pos[0] = vel_rect.x+par.size[0]//2
                    par.pos[1] = vel_rect.y+par.size[1]//2
                else:
                    vel_y = par.velocity_y // abs(par.velocity_y) if par.velocity_y != 0 else 0
                    ratio_vel = par.velocity_x / par.velocity_y if par.velocity_y != 0 else 0
                    vel_x = vel_y * ratio_vel
                    vel_rect = pg.rect.Rect(par.pos[0]-par.size[0]//2, par.pos[1]-par.size[1]//2, par.size[0], par.size[1])
                    while vel_rect.colliderect(i.rect):
                        vel_rect.x -= vel_x
                        vel_rect.y -= vel_y
                        pg.draw.rect(window, (0, 0, 0), vel_rect)
                    par.pos[0] = vel_rect.x+par.size[0]//2
                    par.pos[1] = vel_rect.y+par.size[1]//2
                if y < 0:
                    i.properties[PhysicBody].is_falling = False
                else:
                    i.properties[PhysicBody].is_falling = True
            elif not (i.velocity_x == 0 and i.velocity_y == 0):
                if abs(i.velocity_x) >= abs(i.velocity_y):
                    vel_x = i.velocity_x//abs(i.velocity_x) if i.velocity_x != 0 else 0
                    ratio_vel = i.velocity_y/i.velocity_x if i.velocity_x != 0 else 0
                    vel_y = vel_x * ratio_vel
                    vel_rect = pg.rect.Rect(i.pos[0]-i.size[0]//2, i.pos[1]-i.size[1]//2, i.size[0], i.size[1])
                    while vel_rect.colliderect(par.rect):
                        vel_rect.x -= vel_x
                        vel_rect.y -= vel_y
                        pg.draw.rect(window, (0, 0, 0), vel_rect)
                    i.pos[0] = vel_rect.x+i.size[0]//2
                    i.pos[1] = vel_rect.y+i.size[1]//2
                else:
                    vel_y = i.velocity_y // abs(i.velocity_y) if i.velocity_y != 0 else 0
                    ratio_vel = i.velocity_x / i.velocity_y if i.velocity_y != 0 else 0
                    vel_x = vel_y * ratio_vel
                    vel_rect = pg.rect.Rect(i.pos[0]-i.size[0]//2, i.pos[1]-i.size[1]//2, i.size[0], i.size[1])
                    while vel_rect.colliderect(par.rect):
                        vel_rect.x -= vel_x
                        vel_rect.y -= vel_y
                        pg.draw.rect(window, (0, 0, 0), vel_rect)
                    i.pos[0] = vel_rect.x+i.size[0]//2
                    i.pos[1] = vel_rect.y+i.size[1]//2
                if y < 0:
                    i.properties[PhysicBody].is_falling = False
                else:
                    i.properties[PhysicBody].is_falling = True



        if self.is_falling and not self.is_kinematic:
            par.velocity_y += self.gravity
        if par.velocity_x > 0:
            par.velocity_x -= 0.1
        elif par.velocity_x < 0:
            par.velocity_x += 0.1
        if abs(par.velocity_x) < 0.1:
            par.velocity_x = 0
        if self.gravity == 0:
            if par.velocity_y > 0:
                par.velocity_y -= 0.1
            elif par.velocity_y < 0:
                par.velocity_y += 0.1
            if abs(par.velocity_y) < 0.1:
                par.velocity_y = 0


class SpriteRenderer(Property):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        self.image = pg.image.load(filename)
        self.first = 1

    def update(self):
        par = self.parent
        if self.first:
            self.image = pg.transform.scale(pg.image.load(self.filename), (par.size[0], par.size[1]))
            self.first = 0
        window.blit(self.image, (par.pos[0]-par.size[0]//2-camera_x, par.pos[1]-par.size[1]//2-camera_y))


class Player(GameObject):
    def __init__(self, pos, size, properties, color, speed, jump_force):
        super().__init__(pos, size, properties, color, speed)
        self.jump_force = jump_force

    def reset(self):
        key_pressed = pg.key.get_pressed()
        if key_pressed[pg.K_e]:
            ex.explode()
        if key_pressed[pg.K_a]:
            self.velocity_x = -self.speed
        elif key_pressed[pg.K_d]:
            self.velocity_x = self.speed
        else:
            self.velocity_x = 0
        if key_pressed[pg.K_q] and not self.properties[PhysicBody].is_falling:
            self.velocity_y = -self.jump_force
        elif key_pressed[pg.K_w]:
            self.velocity_y = -self.speed
        elif key_pressed[pg.K_s]:
            self.velocity_y = self.speed
        else:
            self.velocity_y = 0
        # if key_pressed[pg.K_w]:
        #     self.velocity_y = -self.speed
        # elif key_pressed[pg.K_s]:
        #     self.velocity_y = self.speed
        # else:
        #     self.velocity_y = 0


class Player2(GameObject):
    def __init__(self, pos, size, properties, color, speed, jump_force):
        super().__init__(pos, size, properties, color, speed)
        self.jump_force = jump_force

    def reset(self):
        key_pressed = pg.key.get_pressed()
        if key_pressed[pg.K_e]:
            ex.explode()
        if key_pressed[pg.K_LEFT]:
            self.velocity_x = -self.speed
        elif key_pressed[pg.K_RIGHT]:
            self.velocity_x = self.speed
        else:
            self.velocity_x = 0
        if key_pressed[pg.K_q] and not self.properties[PhysicBody].is_falling:
            self.velocity_y = -self.jump_force
        elif key_pressed[pg.K_UP]:
            self.velocity_y = -self.speed
        elif key_pressed[pg.K_DOWN]:
            self.velocity_y = self.speed
        else:
            self.velocity_y = 0
        # if key_pressed[pg.K_w]:
        #     self.velocity_y = -self.speed
        # elif key_pressed[pg.K_s]:
        #     self.velocity_y = self.speed
        # else:
        #     self.velocity_y = 0


class Explosion:
    def __init__(self, pos, objs, power):
        self.pos = pos
        self.objs = objs
        self.power = power


    def explode(self):
        for obj in self.objs:
            obj.properties[PhysicBody].is_kinematic = False
            x, y = (obj.pos[0] - self.pos[0]), (obj.pos[1] - self.pos[1])
            dist = (x**2 + y**2) ** 0.5
            ratio_x, ratio_y = x/dist if x != 0 else 0, y/dist if y != 0 else 0
            obj.velocity_x, obj.velocity_y = self.power*ratio_x, self.power*ratio_y
        #GameObject(self.pos, (100, 100), [SpriteRenderer("explosion.png")])

WIDTH = 700
HEIGHT = 500
window = pg.display.set_mode((WIDTH, HEIGHT), pg.RESIZABLE)
pg.display.set_caption('Physic simulation')

camera_x = 0
camera_y = 0
a = True

objects = pg.sprite.Group()


mol1 = Player((300, 100), (50, 50), [PhysicBody(1000, gravity=0.0)], (255, 0, 0), 3, 4)
mol1_2 = Player2((300, 100), (50, 50), [PhysicBody(100, gravity=0.0)], (255, 0, 0), 3, 4)
mol2 = GameObject((300, 300), (100, 100), [PhysicBody(100, gravity=0)])
mol3 = GameObject((375, 300), (10, 10), [PhysicBody(100, gravity=0)])
floor = GameObject((350, 475), (700, 100), [PhysicBody(is_kinematic=True)])
ex = Explosion((200, 200), [], 5)
ex.objs.append(GameObject((190, 200), (10, 10), [PhysicBody(is_kinematic=True)]))
ex.objs.append(GameObject((190, 190), (10, 10), [PhysicBody(is_kinematic=True)]))
ex.objs.append(GameObject((190, 210), (10, 10), [PhysicBody(is_kinematic=True)]))
ex.objs.append(GameObject((210, 200), (10, 10), [PhysicBody(is_kinematic=True)]))
ex.objs.append(GameObject((210, 190), (10, 10), [PhysicBody(is_kinematic=True)]))
ex.objs.append(GameObject((200, 210), (10, 10), [PhysicBody(is_kinematic=True)]))
ex.objs.append(GameObject((210, 210), (10, 10), [PhysicBody(is_kinematic=True)]))
ex.objs.append(GameObject((200, 190), (10, 10), [PhysicBody(is_kinematic=True)]))
clock = pg.time.Clock()
FPS = 60

running = True

while running:

    for e in pg.event.get():
        if e.type == pg.QUIT:
            running = False


    if a:
        camera_x = mol1.pos[0] - WIDTH // 2
        camera_y = mol1.pos[1] - HEIGHT // 2

        window.fill((255, 255, 255))

        objects.update()
        clock.tick(FPS)
        pg.display.update()

