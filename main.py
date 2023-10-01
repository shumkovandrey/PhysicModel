from random import randint

import pygame as pg


class Molecule(pg.sprite.Sprite):
    def __init__(self, pos, radius, color=(255, 0, 0), speed=2):
        super().__init__()

        self.pos = pos
        self.radius = radius
        self.color = color

        self.rect = pg.Rect(pos[0] - radius, pos[1] - radius, 2 * radius, 2 * radius)
        self.speed = speed
        self.velocity_x = 0
        self.velocity_y = 0

        molecules.add_internal(self)

    def check_collisions(self):
        other_mols = molecules.sprites()
        other_mols.remove(self)
        mol_hits = pg.sprite.spritecollide(self, other_mols, False)
        for m in mol_hits:
            if self.rect.right - m.rect.left <= self.speed*2:
                self.rect.x = m.rect.left - m.rect.width
            if m.rect.right - self.rect.left <= self.speed*2:
                self.rect.x = m.rect.right
            if self.rect.bottom - m.rect.top <= self.speed*2:
                self.rect.y = m.rect.top - m.rect.height
            if m.rect.bottom - self.rect.top <= self.speed*2:
                self.rect.y = m.rect.bottom


        if self.rect.x <= 0:
            self.rect.x = 0
        elif self.rect.right >= WIDTH:
            self.rect.x = WIDTH - self.rect.width
        if self.rect.y <= 0:
            self.rect.y = 0
        elif self.rect.bottom >= HEIGHT:
            self.rect.y = HEIGHT - self.rect.height
        return len(mol_hits) > 0


    def update_parameters(self):
        # self.velocity_x = randint(-2, 2) * self.speed
        # self.velocity_y = randint(-2, 2) * self.speed

        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

        self.check_collisions()

        self.pos = (self.rect.x + self.radius, self.rect.y + self.radius)

    def update(self):
        self.update_parameters()
        pg.draw.circle(window, self.color, self.pos, self.radius)
        pg.draw.rect(window, (0, 255, 0), self.rect, width=1)


WIDTH = 700
HEIGHT = 500
window = pg.display.set_mode((WIDTH, HEIGHT), pg.RESIZABLE)
pg.display.set_caption('Physic simulation')


molecules = pg.sprite.Group()

cnt_x = 20
cnt_y = 24
radius = 8
dist_x = (WIDTH - (cnt_x * radius * 2)) // (cnt_x-1)
dist_y = (HEIGHT - (cnt_y * radius * 2)) // (cnt_y-1)

print(dist_x, dist_y)

# for i in range(cnt_x * cnt_y):
#     Molecule((radius + i % cnt_x * (dist_x + radius * 2), radius + i // cnt_x * (dist_y + radius * 2)), radius, (255 * (i < (cnt_y * cnt_x // 2)), 0, 255 * (i >= (cnt_y * cnt_x // 2))))

"""for i in range(cnt_x * (cnt_y//2)):
    Molecule((radius + i % cnt_x * (dist_x + radius * 2), radius + HEIGHT//2 + i // cnt_x * (dist_y + radius * 2)), radius)"""
mol1 = Molecule((100, 100), 25)
mol2 = Molecule((300, 300), 25)
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

    molecules.update()

    clock.tick(FPS)
    pg.display.update()
