import pygame as pg
import sys
import random

def main():
    pg.display.set_caption("初めてのPyGame")
    scrn_sfc = pg.display.set_mode((1500,900))
    scrn_rct = scrn_sfc.get_rect()
    clock = pg.time.Clock()

    tori_sfc = pg.image.load("fig/6.png")
    tori_sfc.set_colorkey((0, 0, 0))
    tori_sfc.convert()
    tori_sfc = pg.transform.rotozoom(tori_sfc, 0, 2.0)
    tori_rct = tori_sfc.get_rect()
    tori_rct.center = 900, 400
    bg_sfc = pg.image.load("fig/pg_bg.jpg").convert()
    bg_rct = bg_sfc.get_rect()
    bomb_sfc = pg.Surface((20, 20))
    bomb_sfc.set_colorkey((0, 0, 0))
    pg.draw.circle(bomb_sfc, (255, 0, 0), (10,10), 10)
    bomb_rct = bomb_sfc.get_rect()
    bomb_rct.center =  (random.randint(0, scrn_rct.width),
                        random.randint(0, scrn_rct.height))

    while True:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        key_lst = pg.key.get_pressed()
        if key_lst[pg.K_UP]:
            tori_rct.move_ip(0, -1)
        if key_lst[pg.K_DOWN]:
            tori_rct.move_ip(0, 1)
        if key_lst[pg.K_LEFT]:
            tori_rct.move_ip(-1, 0)
        if key_lst[pg.K_RIGHT]:
            tori_rct.move_ip(1, 0)


        bomb_rct.move_ip(1,1)
        scrn_sfc.blit(bg_sfc, (0, 0))
        scrn_sfc.blit(tori_sfc, tori_rct)
        scrn_sfc.blit(bomb_sfc, bomb_rct)
        
        
        pg.display.update()
        clock.tick(1000)


if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()
    sys.exit()

