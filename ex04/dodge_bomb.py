import pygame as pg
import sys
import random

WIDTH = 1500
HEIGHT = 900
TICK = 27

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)




def main():
    # ゲーム画面のSurfaceであるscreen を設定
    win = pg.display.set_mode((WIDTH,HEIGHT))
    # ウィンドウ上部のタイトルを設定
    pg.display.set_caption("初めてのPyGame")

    char = pg.image.load("fig/1.png")
    char.set_colorkey((0, 0, 0))
    char.convert()
    char = pg.transform.rotozoom(char, 0, 2.0)

    bg = pg.image.load("fig/pg_bg.jpg")

    # フレームを管理する時計をclockに格納
    clock = pg.time.Clock()

    class Player(object):
        #Player sprite
        def __init__(self, x, y, width, height):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.vel = 20
            self.isJump = False
            self.left = False
            self.right = False
            self.walkCount = 0
            self.jumpCount = 10

        def draw(self, win):
            if self.walkCount + 1 >= 27:
                self.walkCOunt = 0

            if self.left:
                win.blit(char, (self.x, self.y))
            elif self.right:
                win.blit(char, (self.x, self.y))
            else:
                win.blit(char, (self.x, self.y))

    class Enemy(object):
        def __init__(self, x, y, width, height)

    def redrawGameWindow():
        win.blit(bg, (0, 0))
        player.draw(win)
        pg.display.update()

    player = Player(200, 610, 64, 64)
    running = True
    while running:
        # ---- フレームを空ける ----
        clock.tick(TICK)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        
        keys = pg.key.get_pressed()

        if keys[pg.K_LEFT] and player.x > player.vel:
            player.x -= player.vel
            player.left = True
            player.right = False
        elif keys[pg.K_RIGHT] and player.x < WIDTH - player.width - player.vel:
            player.x += player.vel
            player.right = True
            player.left = False
        else:
            player.right = False
            player.left = False
            player.walkCount = 0
        
        if not (player.isJump):
            if keys[pg.K_UP]:
                player.isJump = True
                player.right = False
                player.left = False
                player.walkCount = 0
        else:
            if player.jumpCount >= -10:
                neg = 1
                if player.jumpCount < 0:
                    neg = -1
                player.y -= (player.jumpCount ** 2) * 0.9 * neg
                player.jumpCount -= 1
            else:
                player.isJump = False
                player.jumpCount = 10
        
        redrawGameWindow()


if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()
    sys.exit()

