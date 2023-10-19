import math

import pygame as pg
import config
from world import World

from shape import *


class Property:
    def __init__(self):
        self.parent = None

    def update(self):
        pass


class GameObject(pg.sprite.Sprite):
    def __init__(self, pos, size, properties, color=(0, 255, 0), speed=2):
        super().__init__()

        self.pos = list(pos)
        self.size = size
        self.color = color
        self.properties = {}
        for i in properties:
            i.parent = self
            self.properties[type(i)] = i

        self.speed = speed
        self.velocity = [0, 0]
        self.last_velocity = [0, 0]

        world.objects.append(self)

    def reset(self):
        pass

    def update_parameters(self):

        self.reset()

        for prop in self.properties.values():
            prop.update()

        # if self.velocity[0] != 0:
        #     self.last_velocity[0] = self.velocity[0]
        # if self.velocity[1] != 0:
        #     self.last_velocity[1] = self.velocity[1]
        #
        # self.last_pos = self.pos.copy()

    def update(self):
        self.update_parameters()

    def draw(self, surf):
        if PhysicBody in self.properties:
            pg.draw.polygon(surf, (255, 0, 0), self.properties[PhysicBody].world_vertices, config.POLYGON_BORDER_WIDTH)
        pg.draw.circle(surf, (255, 0, 0), (self.pos[0] - camera_x, self.pos[1] - camera_y), 2)


class PhysicBody(Property):
    def __init__(self, par_pos, vertices, mass=1000, is_kinematic=False, gravity=0.09):
        super().__init__()
        self.is_kinematic = is_kinematic
        self.is_falling = True
        self.gravity = gravity
        self.mass = mass
        self.vertices = vertices
        self.world_vertices = list(map(lambda x: (x[0] + par_pos[0], x[1] + par_pos[1]), self.vertices))
        world.collision_objects.append(self)

    def udpdate_world_verices(self):
        self.world_vertices = list(map(lambda x: (x[0] + self.parent.pos[0], x[1] + self.parent.pos[1]), self.vertices))

    def move_forwards(self):
        self.parent.pos[0] += 1 * config.MOVEMENT_MULTIPLIER
        self.parent.pos[1] += 1 * config.MOVEMENT_MULTIPLIER
        self.parent.velocity = [1 * config.MOVEMENT_MULTIPLIER, 1 * config.MOVEMENT_MULTIPLIER]
        self.udpdate_world_verices()

    def update(self):
        s_par = self.parent
        for i in world.collision_objects:
            if i == self:
                continue
            i_par = i.parent
            min_depth = math.inf
            if not (i_par.velocity[1] == 0 and i_par.velocity[0] == 0):
                move_shape = i
                dir_vec = calc_vector(s_par.pos, i_par.pos)
            elif not (s_par.velocity[1] == 0 and s_par.velocity[0] == 0):
                move_shape = self
                dir_vec = calc_vector(i_par.pos, s_par.pos)
            else:
                return False
            move_vector = None

            for j in range(len(i.world_vertices)):
                v0 = i.world_vertices[j]
                v1 = i.world_vertices[(j + 1) % len(i.world_vertices)]
                edge_vector = [v1[0] - v0[0], v1[1] - v0[1]]
                normal = [-edge_vector[1], edge_vector[0]]
                normalize(normal)
                a = span_along_line(normal, self)
                b = span_along_line(normal, i)
                if a[0] >= b[1] or a[1] <= b[0]:
                    return False
                else:
                    # we can assume that this collision would not occur in game
                    # since we check for collisions very frequently
                    if not ((a[0] > b[0] and a[1] < b[1]) or (b[0] > a[0] and b[1] < a[1])):
                        depth = min(a[1] - b[0], b[1] - a[0])
                        if (not min_depth) or min_depth > depth:
                            min_depth = depth
                            if dot_product(dir_vec, normal) < 0:
                                multiply_vector_by_scalar(-1, normal)
                            move_vector = normal

            for j in range(len(self.world_vertices)):
                v0 = self.world_vertices[j]
                v1 = self.world_vertices[(j + 1) % len(self.world_vertices)]
                edge_vector = [v1[0] - v0[0], v1[1] - v0[1]]
                normal = [-edge_vector[1], edge_vector[0]]
                normalize(normal)
                a = span_along_line(normal, self)
                b = span_along_line(normal, i)
                if a[0] >= b[1] or a[1] <= b[0]:
                    return False
                else:
                    # we can assume that this collision would not occur in game
                    # since we check for collisions very frequently
                    if not ((a[0] > b[0] and a[1] < b[1]) or (b[0] > a[0] and b[1] < a[1])):
                        depth = min(a[1] - b[0], b[1] - a[0])
                        if (not min_depth) or min_depth > depth:
                            min_depth = depth
                            if dot_product(dir_vec, normal) < 0:
                                multiply_vector_by_scalar(-1, normal)
                            move_vector = normal

            if move_vector:
                move_shape.parent.pos[0] += move_vector[0] * math.ceil(min_depth)
                move_shape.parent.pos[1] += move_vector[1] * math.ceil(min_depth)
                move_shape.udpdate_world_verices()
                return True




pg.init()
clock = pg.time.Clock()
window = pg.display.set_mode(config.SURFACE_SIZE)
world = World()

camera_x, camera_y = 0, 0

main_shape = GameObject((100, 100), (100, 100), [PhysicBody((100, 100), [[-40, -40], [40, -40], [40, 40], [-40, 40]], gravity=0)])
GameObject((100, 100), (500, 500), [PhysicBody((500, 500), [[0, -80], [-50, -20], [-50, 90], [200, 90]], gravity=0)])

# main_shape = world.add_shape([100, 100], [[-40, -40], [40, -40], [40, 40], [-40, 40]])
# #world.add_shape([300, 500], [[0, -40], [-40, 0], [0, 120], [40, 0]])
# world.add_shape([300, 500], [[0, -40], [-40, 0], [0, 120], [40, 0]])
# world.add_shape([500, 650], [[0, -80], [-50, -20], [-50, 90], [200, 90]])
# world.add_shape([650, 500], [[-100, -100], [-100, 100], [100, 100], [100, -100]])
# world.add_shape([500, 300], [[-200, -100], [-100, 20], [20, -50]])
# world.add_shape([0, 0], [[0, 0], [0, 20], [config.SURFACE_SIZE[0], 20], [config.SURFACE_SIZE[0], 0]])
# world.add_shape([0, config.SURFACE_SIZE[1]-20], [[0, 0], [0, 20], [config.SURFACE_SIZE[0], 20], [config.SURFACE_SIZE[0], 0]])
# world.add_shape([0, 0], [[20, 0], [0, 0], [0, config.SURFACE_SIZE[1]], [20, config.SURFACE_SIZE[1]]])
# world.add_shape([config.SURFACE_SIZE[0]-20, 0], [[20, 0], [0, 0], [0, config.SURFACE_SIZE[1]], [20, config.SURFACE_SIZE[1]]])



flag = True
pressed = {'down':False, 'up':False, 'left':False, 'right':False}

while flag:

    window.fill(config.FILL_COLOR)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            flag = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                pressed['left'] = True
            elif event.key == pg.K_RIGHT:
                pressed['right'] = True
            elif event.key == pg.K_UP:
                pressed['up'] = True
            elif event.key == pg.K_DOWN:
                pressed['down'] = True

        elif event.type == pg.KEYUP:
            if event.key == pg.K_LEFT:
                pressed['left'] = False
            elif event.key == pg.K_RIGHT:
                pressed['right'] = False
            elif event.key == pg.K_UP:
                pressed['up'] = False
            elif event.key == pg.K_DOWN:
                pressed['down'] = False

    if pressed['left']:
        main_shape.rotate(config.ROTATION_MULTIER)
    if pressed['right']:
        main_shape.rotate(-config.ROTATION_MULTIER)
    if pressed['up']:
        main_shape.properties[PhysicBody].move_forwards()
    if pressed['down']:
        main_shape.move_backwards()

    window.fill((255, 255, 255))

    world.update()
    world.draw(window)

    clock.tick(config.FPS)

    pg.display.update()

