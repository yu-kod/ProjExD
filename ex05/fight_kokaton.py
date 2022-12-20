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

    # Playerの初期化関数　画像のパス、拡大率、位置を入力
    def __init__(self, img_path, ratio, xy):
        self.sfc = pg.image.load(img_path)
        self.sfc = pg.transform.rotozoom(self.sfc, 0, ratio)
        self.rct = self.sfc.get_rect()
        self.rct.center = xy
        self.pre_key = [1, 0]  # 以前の方向を記憶する変数

    # Playerの描画関数　画面のオブジェクトを入力
    def blit(self, scr: Screen):
        scr.sfc.blit(self.sfc, self.rct)

    # Playerの情報更新関数　画面のオブジェクトを入力
    def update(self, scr: Screen):
        key_dct = pg.key.get_pressed()
        for key, delta in Bird.key_delta.items():
            if key_dct[key]:  # 移動処理
                self.rct.centerx += delta[0]
                self.rct.centery += delta[1]
                self.pre_key = delta  # 前回の移動方向を記憶
            if check_bound(self.rct, scr.rct) != (+1, +1):  # 画面外に出ないようにする処理
                self.rct.centerx -= delta[0]
                self.rct.centery -= delta[1]
        self.blit(scr)  # 描画

    # 弾を撃つ処理を行う関数　弾のリストを入力
    def shoot(self, bullets):
        if len(bullets) < 5:  # 画面内に5発以上無ければ弾を撃てる
            bullets.append(
                Projectile((0, 0, 255), 20, self.pre_key, self))  # 弾追加


# 弾用のクラス
class Projectile:
    # 初期化関数　色、半径、移動方向、Playerのオブジェクトを入力
    def __init__(self, color, rad, vxy, bird: Bird):
        self.sfc = pg.Surface((2*rad, 2*rad))
        self.sfc.set_colorkey((0, 0, 0))
        pg.draw.circle(self.sfc, color, (rad, rad), rad)
        self.rct = self.sfc.get_rect()
        self.rct.centerx = bird.rct.centerx
        self.rct.centery = bird.rct.centery
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


# 爆弾用の関数
class Bomb:
    # 初期化関数　色、半径、移動方向、画面オブジェクトを入力
    def __init__(self, color, rad, vxy, scr):
        self.sfc = pg.Surface((2*rad, 2*rad))
        self.sfc.set_colorkey((0, 0, 0))
        pg.draw.circle(self.sfc, color, (rad, rad), rad)
        self.rct = self.sfc.get_rect()
        self.rct.centerx = random.randint(0, scr.rct.width)  # 爆弾の初期配置位置はランダム
        self.rct.centery = random.randint(0, scr.rct.height)
        self.vx, self.vy = vxy

    # 爆弾を描画する関数　画面のオブジェクトを入力
    def blit(self, scr: Screen):
        scr.sfc.blit(self.sfc, self.rct)

    # 爆弾の情報を更新するための関数
    def update(self, scr: Screen):
        # 移動処理
        self.rct.move_ip(self.vx, self.vy)
        # 画面外に出たら反射
        yoko, tate = check_bound(self.rct, scr.rct)
        self.vx *= yoko
        self.vy *= tate
        # 描画処理
        self.blit(scr)


# 文字のクラス
class text:
    # 初期化関数　文字列、x座標、y座標、フォントサイズを入力
    def __init__(self, string, coordx, coordy, fontSize):
        font = pg.font.Font('freesansbold.ttf', fontSize)
        self.text = font.render(string, True, (0, 0, 0))
        self.textRect = self.text.get_rect()
        self.textRect.left, self.textRect.top = (coordx, coordy)

    # 描画用の関数
    def blit(self, scr: Screen):
        scr.sfc.blit(self.text, self.textRect)


# アイテムのクラス
class Item:
    # 初期化関数　色、半径、画面のオブジェクトを入力
    def __init__(self, color, rad, scr):
        self.sfc = pg.Surface((2*rad, 2*rad))
        self.sfc.set_colorkey((0, 0, 0))
        pg.draw.circle(self.sfc, color, (rad, rad), rad)
        self.rct = self.sfc.get_rect()
        self.rct.centerx = random.randint(0, scr.rct.width)  # 場所はランダム
        self.rct.centery = random.randint(0, scr.rct.height)

    # アイテムの描画用関数
    def blit(self, scr: Screen):
        scr.sfc.blit(self.sfc, self.rct)


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
    scr = Screen("逃げろこうかとん", (1500, 900), "fig/pg_bg.jpg")

    # Playerを宣言
    kkt = Bird("fig/6.png", 2.0, (900, 400))

    # 爆弾のリストを宣言
    bkd_list = []
    bkd = Bomb((255, 0, 0), 10, (1, 1), scr)
    bkd_list.append(bkd)

    # 弾のリスト
    bullets = []

    # アイテムのリスト
    items = []
    # 時間を管理する変数
    time = 0
    # スコアを管理する変数
    score = 0
    # 爆弾の発生間隔を管理する変数
    pre_bomb_score = 0
    # アイテムの発生間隔を管理する変数
    pre_item_score = 0

    # main loop
    while True:
        # 時間処理　一定時間ごとにスコア+1
        time += 1
        if time >= 300:
            score += 1
            time = 0

        # 以前出現させたスコアと比較して、3スコアごとに出現(%で管理するとtick更新ごとにしゅつげんしてしまうため)
        if score - pre_bomb_score == 3:
            bkd = Bomb((255, 0, 0), 10, (1, 1), scr)
            bkd_list.append(bkd)
            pre_bomb_score = score

        # 5スコアごとに出現
        if score - pre_item_score == 6:
            item = Item((0, 255, 0), 10, scr)
            items.append(item)
            pre_item_score = score

        # 画面描画
        scr.blit()

        for event in pg.event.get():
            # 終了判定
            if event.type == pg.QUIT:
                return
            # スペースキーを押したとき
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    # 弾を撃つ処理
                    kkt.shoot(bullets)

        # Player 更新処理
        kkt.update(scr)

        # 爆弾更新処理
        for bkd in (bkd_list):
            bkd.update(scr)
            # Playerと衝突で終了
            if kkt.rct.colliderect(bkd.rct):
                return
            # 弾と衝突でお互い消滅
            for bullet in bullets:
                if bullet.rct.colliderect(bkd.rct):
                    bullets.pop(bullets.index(bullet))
                    bkd_list.pop(bkd_list.index(bkd))

        # 弾の移動処理　画面外で消滅
        for bullet in bullets:
            if bullet.update(scr):
                bullets.pop(bullets.index(bullet))

        # アイテムの取得処理
        for item in items:
            if kkt.rct.colliderect(item.rct):
                score += 20
                # 急激にスコアが増えるので、Pre変数をリセット
                pre_item_score = score
                pre_bomb_score = score
                # アイテム削除
                items.pop(items.index(item))
            # アイテム描画
            item.blit(scr)

        # 点数を宣言
        totalText = text("Score: " + str(score), 40, 20, 60)
        # 点数を描画
        totalText.blit(scr)

        # 画面更新
        pg.display.update()
        clock.tick(1000)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
