import pygame as pg
#import random
import sys

# 色定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)


# 画面描画用のクラス
class Screen:
    # 初期化関数　タイトル、縦横幅、画像のパスを入力
    def __init__(self, title, wh):
        pg.display.set_caption(title)
        self.sfc = pg.display.set_mode(wh)
        self.rct = self.sfc.get_rect()

    # 画面の描画関数
    def blit(self):
        self.sfc.fill(BLACK)
        pg.draw.line(
                        self.sfc, WHITE, (self.rct.centerx, 0),
                        (self.rct.centerx, 900), 10
                    )


# Playerの関数
class Player:
    # キーと方向の対応付け辞書
    key_delta = [{
        pg.K_w:     [0, -1],
        pg.K_s:     [0, +1],
        pg.K_a:     [-1, 0],
        pg.K_d:     [+1, 0],
    }, {
        pg.K_UP:    [0, -1],
        pg.K_DOWN:  [0, +1],
        pg.K_LEFT:  [-1, 0],
        pg.K_RIGHT: [+1, 0],
    }]

    # Playerの初期化関数　画像のパス、拡大率、位置を入力
    def __init__(self, color, rad, xy, no):
        self.sfc = pg.Surface((2*rad, 2*rad))
        self.sfc.set_colorkey((0, 0, 0))
        pg.draw.circle(self.sfc, color, (rad, rad), rad)
        self.rct = self.sfc.get_rect()
        self.rct.center = xy
        self.pre_key = [1, 0]  # 以前の方向を記憶する変数
        self.number = no  # 0 or 1
        if self.number:
            self.bullet_direction = [-1, 0]
        else:
            self.bullet_direction = [1, 0]
        # 弾のリスト
        self.bullets = []

    # Playerの描画関数　画面のオブジェクトを入力
    def blit(self, scr: Screen):
        scr.sfc.blit(self.sfc, self.rct)

    # Playerの情報更新関数　画面のオブジェクトを入力
    def update(self, scr: Screen):
        key_dct = pg.key.get_pressed()
        for key, delta in Player.key_delta[self.number].items():
            if key_dct[key]:  # 移動処理
                self.rct.centerx += delta[0]
                self.rct.centery += delta[1]
            if check_bound(self.rct, scr.rct) != (+1, +1):  # 画面外に出ないようにする処理
                self.rct.centerx -= delta[0]
                self.rct.centery -= delta[1]
        self.blit(scr)  # 描画

    # 弾を設置する処理を行う関数
    def set_bullet(self):
        if len(self.bullets) < 10:  # 画面内に10発以上無ければ弾を撃てる
            self.bullets.append(
                Projectile(BLUE, 20, self.bullet_direction, self))  # 弾追加


# 弾用のクラス
class Projectile:
    # 初期化関数　色、半径、移動方向、Playerのオブジェクトを入力
    def __init__(self, color, rad, vxy, player: Player):
        self.sfc = pg.Surface((2*rad, 2*rad))
        self.sfc.set_colorkey((0, 0, 0))
        pg.draw.circle(self.sfc, color, (rad, rad), rad)
        self.rct = self.sfc.get_rect()
        self.rct.centerx = player.rct.centerx
        self.rct.centery = player.rct.centery
        self.vx, self.vy = vxy

    # 弾の描画関数　画面のオブジェクトを入力
    def blit(self, scr: Screen):
        scr.sfc.blit(self.sfc, self.rct)

    # 弾の情報更新用関数　画面のオブジェクトを入力
    def update(self, scr: Screen):
        self.rct.move_ip(self.vx, self.vy)
        scr.sfc.blit(self.sfc, self.rct)
        yoko, tate = check_bound(self.rct, scr.rct)
        return yoko == -1 or tate == -1  # 画面外に出たらTrueを返却


# オブジェクトが重なっているか確認する関数
def check_bound(obj_rct, scr_rct):
    """
    第1引数:オブジェクトのrect
    第2引数:スクリーンrect
    範囲内：+1/範囲外:-1
    """
    yoko, tate = +1, +1
    if obj_rct.left < scr_rct.left or scr_rct.right < obj_rct.right:
        yoko = -1
    if obj_rct.top < scr_rct.top or scr_rct.bottom < obj_rct.bottom:
        tate = -1
    return yoko, tate


# メイン関数
def main():
    clock = pg.time.Clock()

    # 画面宣言
    scr = Screen("turn-shot", (1500, 900))

    # Playerを宣言
    p1 = Player(RED, 10.0, (400, 450), 0)
    p2 = Player(GREEN, 10.0, (1100, 450), 1)
    counter = 8000

    # main loop
    while True:
        for event in pg.event.get():
            # 終了判定
            if event.type == pg.QUIT:
                return
            # eを押したとき
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_e and counter >= 4000:
                    # 弾を撃つ処理
                    p1.set_bullet()
                if event.key == pg.K_m and counter >= 4000:
                    # 弾を撃つ処理
                    p2.set_bullet()

        # 画面描画
        scr.blit()

        if counter < 0:
            counter += 8000
        elif counter < 4000:
            # 弾の移動処理　画面外で消滅
            for bullet in p1.bullets:
                if bullet.update(scr):
                    p1.bullets.pop(p1.bullets.index(bullet))
                if bullet.rct.colliderect(p2.rct):
                    return
            for bullet in p2.bullets:
                if bullet.update(scr):
                    p2.bullets.pop(p2.bullets.index(bullet))
                if bullet.rct.colliderect(p1.rct):
                    return
        else:
            for bullet in p1.bullets:
                bullet.blit(scr)
            for bullet in p2.bullets:
                bullet.blit(scr)
        p1.update(scr)
        p2.update(scr)

        # 画面更新
        pg.display.update()
        eta = clock.tick(1000)
        counter -= eta


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
