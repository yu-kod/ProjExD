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
        self.bullet_num = 5
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
        if len(self.bullets) < self.bullet_num:  # 画面内に10発以上無ければ弾を撃てる
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


# 弾を強化するアイテムのクラス(近藤悠斗)
class Item:
    def __init__(self, color, rad, player: Player):
        self.sfc = pg.Surface((2*rad, 2*rad))
        self.sfc.set_colorkey((0, 0, 0))
        pg.draw.circle(self.sfc, color, (rad, rad), rad)
        self.rct = self.sfc.get_rect()
        if player.number:
            self.rct.center = (1100, 450)
        else:
            self.rct.center = (400, 450)

    # アイテムの描画関数　画面のオブジェクトを入力
    def blit(self, scr: Screen):
        scr.sfc.blit(self.sfc, self.rct)
# (近藤ここまで)


# 追加機能　ライフ表示用のクラス(鈴木友也)
class Life:
    def __init__(self, hp, color, xy):
        self.hp = hp
        self.color = color
        self.xy = xy
        self.font = pg.font.Font(None, 55)
        self.text = self.font.render(f"HP:{self.hp}", True, self.color)

    # 描画
    def blit(self, scr):
        scr.sfc.blit(self.text, self.xy)

    # HPの更新
    def update(self, scr):
        self.hp -= 1
        self.text = self.font.render(f"HP:{self.hp}", True, self.color)
        self.blit(scr)


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


# ゲームオーバー時に呼び出される関数(中村隼人)
def gameover(clock, player, scr:Screen):
    font = pg.font.Font(None, 300) #ゲームオーバーの文字の大きさを設定
    txt = f"{player} WIN!" #表示する文字列
    txt_rend = font.render(txt, True, (128,   0, 128)) #文字を紫色でrenderする。
    txt_rect = txt_rend.get_rect(center=(scr.rct.right//2, scr.rct.bottom//2)) #真ん中に文字を配置する
    scr.sfc.blit(txt_rend, txt_rect) #文字を貼り付け
    pg.display.update() #ディスプレイ全体を更新。これをしないと文字が表示されない。
    clock.tick(0.33) #3秒間表示する
# (中村ここまで)

# メイン関数
def main():
    clock = pg.time.Clock()

    # 画面宣言
    scr = Screen("turn-shot", (1500, 900))

    # Playerを宣言
    p1 = Player(RED, 10.0, (400, 450), 0)
    p2 = Player(GREEN, 10.0, (1100, 450), 1)
    # ライフの宣言（鈴木友也）
    p1hp = Life(3, RED, (0, 0))
    p2hp = Life(3, GREEN, (1415, 0))
    # アイテムを宣言
    p1_item = Item(YELLOW, 10, p1)
    p2_item = Item(YELLOW, 10, p2)
    # 初回の時間を決定
    counter = 8000
    pre_count = counter
    # アイテムを表示するかどうかのフラッaグ
    p1_item_flag = 1
    p2_item_flag = 1

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
            p1_item_flag = 1
            p2_item_flag = 1
            # (counter, pre_count変数については近藤悠斗)
            counter += pre_count + 100  # 次回の時間決定
            pre_count = counter
        elif counter < 2000:
            # 弾の移動処理　画面外で消滅　（プレイヤーと衝突で消滅　衝突でHP-1（鈴木友也））
            for bullet in p1.bullets:
                if bullet.update(scr):
                    p1.bullets.pop(p1.bullets.index(bullet))
                if bullet.rct.colliderect(p2.rct):
                    p1.bullets.pop(p1.bullets.index(bullet))
                    p2hp.update(scr)
            for bullet in p2.bullets:
                if bullet.update(scr):
                    p2.bullets.pop(p2.bullets.index(bullet))
                if bullet.rct.colliderect(p1.rct):
                    p2.bullets.pop(p2.bullets.index(bullet))
                    p1hp.update(scr)


            # アイテム処理(近藤悠斗)
            if p1_item_flag == 1:
                p1_item.blit(scr)
                if p1_item.rct.colliderect(p1.rct):
                    p1.bullet_num += 3
                    p1_item_flag = 0
            if p2_item_flag == 1:
                p2_item.blit(scr)
                if p2_item.rct.colliderect(p2.rct):
                    p2.bullet_num += 3
                    p2_item_flag = 0
            # (近藤ここまで)
        else:
            for bullet in p1.bullets:
                bullet.blit(scr)
            for bullet in p2.bullets:
                bullet.blit(scr)
        p1.update(scr)
        p2.update(scr)
        # ライフ更新（鈴木友也）
        p1hp.blit(scr)
        p2hp.blit(scr)

        # HPが0になったら終了（鈴木友也）
        if p1hp.hp == 0:
            gameover(clock, "Player2", scr) #gameover関数を呼び出す(中村隼人)
            return
        if p2hp == 0:
            gameover(clock, "Player1", scr) #gameover関数を呼び出す(中村隼人)
            return

        # 画面更新
        pg.display.update()
        eta = clock.tick(1000)
        counter -= eta


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
