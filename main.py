import pygame as pg


SIZE = WIDTH, HEIGHT = 1200, 1000
FPS = 60

pg.init()
window = pg.display.set_mode(SIZE)
clock = pg.time.Clock()

while True:
    window.fill(pg.Color('black'))

    for i in pg.event.get():
        if i.type == pg. QUIT:
            exit()

    pg.display.flip()
    clock.tick(FPS)
