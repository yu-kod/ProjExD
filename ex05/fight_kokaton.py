import pygame as pg
import random
import sys


# 画面描画用のクラス
class Screen:

    # 初期化関数　タイトル、縦横幅、画像のパスを入力
    def __init__(self, title, wh, img_path):
        pg.display.set_caption(title)
        self.sfc = pg.display.set_mode(wh)
        self.rct = self.sfc.get_rect()
        self.bgi_sfc = pg.image.load(img_path)
        self.bgi_rct = self.bgi_sfc.get_rect()

    # 画面の描画関数
    def blit(self):
        self.sfc.blit(self.bgi_sfc, self.bgi_rct)


# Playerの関数
class Bird:
    # キーと方向の対応付け辞書
    key_delta = {
        pg.K_UP:    [0, -1],
        pg.K_DOWN:  [0, +1],
        pg.K_LEFT:  [-1, 0],
        pg.K_RIGHT: [+1, 0],
    }

    #Playerの初期化関数　画像のパス、拡大率、位置を入力
    def __init__(self, img_path, ratio, xy):
        self.sfc = pg.image.load(img_path)
        self.sfc = pg.transform.rotozoom(self.sfc, 0, ratio)
        self.rct = self.sfc.get_rect()
        self.rct.center = xy
        self.shoot_flag = True
        self.pre_key = [1, 0]

    def blit(self, scr: Screen):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self, scr: Screen):
        key_dct = pg.key.get_pressed()
        for key, delta in Bird.key_delta.items():
            if key_dct[key]:
                self.rct.centerx += delta[0]
                self.rct.centery += delta[1]
                self.pre_key = delta
            if check_bound(self.rct, scr.rct) != (+1, +1):
                self.rct.centerx -= delta[0]
                self.rct.centery -= delta[1]
        self.blit(scr)

    def shoot(self, bullets):
        if len(bullets) < 5:
            bullets.append(
                Projectile((0, 0, 255), 20, self.pre_key, self))


class Projectile:
    def __init__(self, color, rad, vxy, bird: Bird):
        self.sfc = pg.Surface((2*rad, 2*rad))  # 正方形の空のSurface
        self.sfc.set_colorkey((0, 0, 0))
        pg.draw.circle(self.sfc, color, (rad, rad), rad)
        self.rct = self.sfc.get_rect()
        self.rct.centerx = bird.rct.centerx
        self.rct.centery = bird.rct.centery
        self.vx, self.vy = vxy

    def blit(self, scr: Screen):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self, scr: Screen):
        self.rct.move_ip(self.vx, self.vy)
        scr.sfc.blit(self.sfc, self.rct)
        yoko, tate = check_bound(self.rct, scr.rct)
        return yoko == -1 or tate == -1 


class Bomb:
    def __init__(self, color, rad, vxy, scr):
        self.sfc = pg.Surface((2*rad, 2*rad))  # 正方形の空のSurface
        self.sfc.set_colorkey((0, 0, 0))
        pg.draw.circle(self.sfc, color, (rad, rad), rad)
        self.rct = self.sfc.get_rect()
        self.rct.centerx = random.randint(0, scr.rct.width)
        self.rct.centery = random.randint(0, scr.rct.height)
        self.vx, self.vy = vxy

    def blit(self, scr: Screen):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self, scr: Screen):
        self.rct.move_ip(self.vx, self.vy)
        scr.sfc.blit(self.sfc, self.rct)
        yoko, tate = check_bound(self.rct, scr.rct)
        self.vx *= yoko
        self.vy *= tate
        self.blit(scr)


class text:
    def __init__(self, string, coordx, coordy, fontSize):
        font = pg.font.Font('freesansbold.ttf', fontSize)
        self.text = font.render(string, True, (0, 0, 0))
        self.textRect = self.text.get_rect()
        self.textRect.left, self.textRect.top = (coordx, coordy)
    
    def blit(self, scr: Screen):
        scr.sfc.blit(self.text, self.textRect)


class Item:
    def __init__(self, color, rad, scr):
        self.sfc = pg.Surface((2*rad, 2*rad))  # 正方形の空のSurface
        self.sfc.set_colorkey((0, 0, 0))
        pg.draw.circle(self.sfc, color, (rad, rad), rad)
        self.rct = self.sfc.get_rect()
        self.rct.centerx = random.randint(0, scr.rct.width)
        self.rct.centery = random.randint(0, scr.rct.height)
    
    def blit(self, scr: Screen):
        scr.sfc.blit(self.sfc, self.rct)


def check_bound(obj_rct, scr_rct):
    """
    第1引数:こうかとんrectまたは爆弾rect
    第2引数:スクリーンrect
    範囲内：+1/範囲外:-1
    """
    yoko, tate = +1, +1
    if obj_rct.left < scr_rct.left or scr_rct.right < obj_rct.right:
        yoko = -1
    if obj_rct.top < scr_rct.top or scr_rct.bottom < obj_rct.bottom:
        tate = -1
    return yoko, tate


def main():
    clock = pg.time.Clock()

    scr = Screen("逃げろこうかとん", (1500, 900), "fig/pg_bg.jpg")

    kkt = Bird("fig/6.png", 2.0, (900, 400))

    bkd_list = []
    bkd = Bomb((255, 0, 0), 10, (1, 1), scr)
    bkd_list.append(bkd)

    bullets = []

    items = []
    time = 0
    score = 0
    pre_bomb_score = 0
    pre_item_score = 0
    while True:
        time += 1
        if time >= 300:
            score += 1
            time = 0 

        if score - pre_bomb_score == 3:
            bkd = Bomb((255, 0, 0), 10, (1, 1), scr)
            bkd_list.append(bkd)
            pre_bomb_score = score

        if score - pre_item_score == 6:
            item = Item((0, 255, 0), 10, scr)
            items.append(item)
            pre_item_score = score

        scr.blit()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    kkt.shoot(bullets)

        kkt.update(scr)
        for bkd in (bkd_list):
            bkd.update(scr)
            if kkt.rct.colliderect(bkd.rct):
                return
            for bullet in bullets:
                if bullet.rct.colliderect(bkd.rct):
                    bullets.pop(bullets.index(bullet))
                    bkd_list.pop(bkd_list.index(bkd))

        for bullet in bullets:
            if bullet.update(scr):
                bullets.pop(bullets.index(bullet))

        for item in items:
            if kkt.rct.colliderect(item.rct):
                score += 20
                pre_item_score = score
                items.pop(items.index(item))
            item.blit(scr)

        totalText = text("Score: " + str(score), 40, 20, 60)
        totalText.blit(scr)

        pg.display.update()
        clock.tick(1000)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
