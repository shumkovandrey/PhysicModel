from random import randint

import pygame as pg


class Molecule(pg.sprite.Sprite):
    def __init__(self, pos, radius, color=(255, 0, 0), speed=4):
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
            print(self.rect.right, m.rect.left)
            if self.rect.right-1 - m.rect.left <= 5:
                self.rect.x = m.rect.left - m.rect.width

            """elif self.rect.left < m.rect.right:
                self.rect.x = m.rect.right + m.rect.width
                self.velocity_x = 0
            if self.rect.bottom > m.rect.top:
                self.rect.bottom = m.rect.top
                self.velocity_y = 0
            elif self.rect.top < m.rect.bottom:
                self.rect.top = m.rect.bottom
                self.velocity_y = 0"""
            """self.velocity_x = -self.velocity_x
            self.velocity_y = -self.velocity_y"""
        return len(mol_hits) > 0


    def update_parameters(self):
        self.velocity_x = randint(-2, 2)
        self.velocity_y = randint(-2, 2)

        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

        self.check_collisions()

        self.pos = (self.rect.x + self.radius, self.rect.y + self.radius)

    def update(self):
        self.update_parameters()
        pg.draw.circle(window, self.color, self.pos, self.radius)
        pg.draw.rect(window, (0, 255, 0), self.rect, width=2)


WIDTH = 700
HEIGHT = 500
window = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Physic simulation')


molecules = pg.sprite.Group()

mol1 = Molecule((100, 100), 50)
mol2 = Molecule((300, 300), 50)

clock = pg.time.Clock()
FPS = 60

running = True

while running:

    for e in pg.event.get():
        if e.type == pg.QUIT:
            running = False

    key_pressed = pg.key.get_pressed()
    if key_pressed[pg.K_a]:
        mol1.velocity_x = -5
    elif key_pressed[pg.K_d]:
        mol1.velocity_x = 5
    else:
        mol1.velocity_x = 0
    if key_pressed[pg.K_w]:
        mol1.velocity_y = -5
    elif key_pressed[pg.K_s]:
        mol1.velocity_y = 5
    else:
        mol1.velocity_y = 0

    window.fill((255, 255, 255))

    molecules.update()

    clock.tick(FPS)
    pg.display.update()
