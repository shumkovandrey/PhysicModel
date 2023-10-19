from locale import normalize
import config
import pygame
import math

class shape_object:
    def __init__(self, position, vertices) -> None:
        ''' vertices are relative to given position'''
        self.vertices = vertices
        self.position = position
        self.colliding = False
        self.color = config.DEFAULT_SHAPE_COLOR
        self.world_vertices = list(map(lambda x: (x[0] + self.position[0], x[1] + self.position[1]), self.vertices))
        self.centralize_polygon_position()
        self.facing = [0, 1]
        self.velocity = 0


    def move_forwards(self):
        self.position[0] += self.facing[0] * config.MOVEMENT_MULTIPLIER
        self.position[1] += self.facing[1] * config.MOVEMENT_MULTIPLIER
        self.velocity = [self.facing[0] * config.MOVEMENT_MULTIPLIER, self.facing[1] * config.MOVEMENT_MULTIPLIER]
        self.udpdate_world_verices()


    def move_backwards(self):
        self.position[0] += self.facing[0] * config.MOVEMENT_MULTIPLIER
        self.position[1] += self.facing[1] * config.MOVEMENT_MULTIPLIER
        self.velocity = [self.facing[0] * config.MOVEMENT_MULTIPLIER, self.facing[1] * config.MOVEMENT_MULTIPLIER]
        self.udpdate_world_verices()


    def udpdate_world_verices(self):
        self.world_vertices = list(map(lambda x: (x[0] + self.position[0], x[1] + self.position[1]), self.vertices))


    def centralize_polygon_position(self):
        self.position = get_centroid(self.world_vertices)
        self.vertices = []
        for vertex in self.world_vertices:
            self.vertices.append(calc_vector(self.position, vertex))


    def rotate(self, angle):
        ''' rotates vertices cunter-clockwise by given angle in radians'''
        cos = math.cos(angle)
        sin = math.sin(angle)
        for vertex in self.vertices:
            x, y = vertex
            vertex[0] = x * cos - y * sin
            vertex[1] = x * sin + y * cos

        x, y = self.facing
        self.facing[0] = x * cos - y * sin
        self.facing[1] = x * sin + y * cos
        self.udpdate_world_verices()
        self.velocity = 1


    def handle_collisions(self, polygon):
        min_depth = math.inf
        if polygon.velocity != 0:
            move_shape = polygon
            dir_vec = calc_vector(self.position, polygon.position)
        elif self.velocity != 0:
            move_shape = self
            dir_vec = calc_vector( polygon.position, self.position)
        else:
            return False
        move_vector = None

        for i in range(len(polygon.world_vertices)):
            v0 = polygon.world_vertices[i]
            v1 = polygon.world_vertices[(i + 1) % len(polygon.world_vertices)]
            edge_vector = [v1[0] - v0[0], v1[1] - v0[1]]
            normal = [-edge_vector[1], edge_vector[0]]
            normalize(normal)
            a = span_along_line(normal, self)
            b = span_along_line(normal, polygon)
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

        for i in range(len(self.world_vertices)):
            v0 = self.world_vertices[i]
            v1 = self.world_vertices[(i + 1) % len(self.world_vertices)]
            edge_vector = [v1[0] - v0[0], v1[1] - v0[1]]
            normal = [-edge_vector[1], edge_vector[0]]
            normalize(normal)
            a = span_along_line(normal, self)
            b = span_along_line(normal, polygon)
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
            move_shape.position[0] += move_vector[0] * math.ceil(min_depth)
            move_shape.position[1] += move_vector[1] * math.ceil(min_depth)
            move_shape.udpdate_world_verices()
            return True


    def draw(self, surface):
        pygame.draw.polygon(surface, self.color, self.world_vertices, config.POLYGON_BORDER_WIDTH)
        pygame.draw.circle(surface, (255,0,0), self.position, 2)
        fill_polygon_with_alpha(surface, self.world_vertices, self.color)

    

def span_along_line(vector, shape):
    span = [math.inf, -math.inf]
    for v in shape.world_vertices:
        d_p = round(dot_product(vector, v), 1)
        span[0] = min(span[0], d_p)
        span[1] = max(span[1], d_p)
    return span
    

def fill_polygon_with_alpha(surface, polygon, color):
    x_range = [math.inf, -math.inf]
    y_range = [math.inf, -math.inf]
    for vertex in polygon:
        x_range[0] = min(x_range[0], vertex[0])
        x_range[1] = max(x_range[1], vertex[0])
        y_range[0] = min(y_range[0], vertex[1])
        y_range[1] = max(y_range[1], vertex[1])

    surface_rect = (x_range[0], y_range[0], x_range[1] - x_range[0], y_range[1] - y_range[0])
    relative_vertices = list(map(lambda x: (x[0] - surface_rect[0], x[1] - surface_rect[1]), polygon))
    polygon_surface = pygame.Surface(surface_rect[2:])
    polygon_surface.set_colorkey((0, 0, 0))
    polygon_surface.set_alpha(config.POLYGON_FILL_ALPHA)
    pygame.draw.polygon(polygon_surface, color, relative_vertices)
    surface.blit(polygon_surface, surface_rect[:2])


def calc_vector(p1, p2):
    return [p2[0] - p1[0], p2[1] - p1[1]]

def vec_length(vector):
    return math.sqrt(vector[0]**2 + vector[1]**2)

def normalize(v, length=None):
    if length == None:
        length = math.sqrt(v[0]**2 + v[1]**2)
    v[0] = round(v[0] / length, 1)
    v[1] = round(v[1] / length, 1)

def add_vectors(v1, v2):
    return (v1[0] + v2[0], v1[1] + v2[1])

def subtract_vectors(v1, v2):
    return (v1[0] - v2[0], v1[1] - v2[1])

def multiply_vector_by_scalar(s, v):
    v[0] = s * v[0]
    v[1] = s * v[1]

def cross_product_2d(v1, v2):
    return v1[0]* v2[1] - v1[1]* v2[0] 

def dot_product(v0, v1):
    return v0[0] * v1[0] + v0[1] * v1[1]

def get_centroid(vertices):
    x = y = 0
    area = 0
    n = len(vertices)
    for i in range(n):
        p1 = vertices[i]
        p2 = vertices[(i + 1) % n]
        tmp = p1[0] * p2[1] - p2[0] * p1[1]
        area += tmp
        x += (p1[0] + p2[0]) * tmp
        y += (p1[1] + p2[1]) * tmp
    
    return [x / (3*area), y / (3*area)] 