import pygame as pg
import sys
import random

# 定数
WIDTH = 1500
HEIGHT = 900
TICK = 30

# 色定義
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
    pg.display.set_caption("逃げろこうかとん")

    # 移動してないときのキャラクター画像読み込み
    char = pg.image.load("fig/4.png")
    char.set_colorkey(BLACK)
    char.convert()
    char = pg.transform.rotozoom(char, 0, 2.0)

    # 左に移動しているときのキャラクター画像
    char_left = pg.image.load("fig/5.png")
    char_left.set_colorkey(BLACK)
    char_left.convert()
    char_left = pg.transform.rotozoom(char_left, 0, 2.0)

    #右に移動しているときのキャラクター画像
    char_right = pg.image.load("fig/2.png")
    char_right.set_colorkey(BLACK)
    char_right.convert()
    char_right = pg.transform.rotozoom(char_right, 0, 2.0)
    
    # 背景画像
    bg = pg.image.load("fig/pg_bg.jpg")

    # 爆弾の見た目
    bom = pg.Surface((20, 20))
    pg.draw.circle(bom, RED, (10, 10), 10)
    bom.set_colorkey(BLACK)
    bom.convert()

    # フレームを管理する時計をclockに格納
    clock = pg.time.Clock()

    #プレイヤーのクラス
    class Player(object):
        # 初期化
        def __init__(self, x, y, width, height):
            # 座標
            self.x = x
            self.y = y
            # 幅と高さ
            self.width = width
            self.height = height
            # 動作の倍率
            self.vel = 15
            # ジャンプしているかどうか
            self.isJump = False
            # 向いている方向
            self.left = False
            self.right = False
            # 重力処理用
            self.jumpCount = 10
            # 前回向いていた方向
            self.pre_char = char_right
            # 衝突判定
            self.hitBox = (self.x + 17, self.y + 11, 50, 100)

        # プレイヤー描画用関数
        def draw(self, win):
            #左向き、右向き、立ち止まっている時を描画
            if self.left:
                win.blit(char_left, (self.x, self.y))
                self.pre_char = char_left
            elif self.right:
                win.blit(char_right, (self.x, self.y))
                self.pre_char = char_right
            else:
                win.blit(self.pre_char, (self.x, self.y))
            # hitBoxの上書き対策
            self.hitBox = (self.x + 17, self.y + 11, 50, 100)
            #hitBoxの範囲の確認
            #pg.draw.rect(win, (255,0,0),self.hitBox,2)
        
        #衝突したときに動作する関数
        def hit(self):
            print('hit')

    # 敵のクラス
    class Enemy(object):
        # 初期化
        def __init__(self, x, y, width, height,vel, end):
            # 座標
            self.x = x
            self.y = y
            # 幅と高さ
            self.width = width
            self.height = height
            # 移動の終了位置
            self.end = end
            # 移動の両端
            self.path = [self.x, self.end]
            # 動作の倍率
            self.vel = vel
            # 当たり判定
            self.hitBox = (self.x, self.y, 20, 20)

        # 敵の描画用関数
        def draw(self, win):
            # 移動処理実行
            self.move()
            # 描画
            win.blit(bom, (self.x, self.y))
            # hitboxの上書き対策
            self.hitBox = (self.x, self.y, 20, 20)
            #hitbox確認用
            #pg.draw.rect(win, RED, self.hitBox,2)

        # 敵の移動用関数
        def move(self):
            #左移動
            if self.vel > 0:
                #移動する
                if self.x + self.vel < self.path[0]:
                    self.x += self.vel
                # 反転する
                else:
                    self.vel = self.vel * -1
                    self.x += self.vel
            # 右移動
            else:
                # 移動する
                if self.x - self.vel > self.path[1]:
                    self.x += self.vel
                # 反転する
                else:
                    self.vel = self.vel * -1
                    self.x += self.vel
        
        #衝突時に実行される関数
        def hit(self):
            print('hit')

    #画面描画用関数
    def redrawGameWindow():
        # 背景描画
        win.blit(bg, (0, 0))
        # プレイヤー描画
        player.draw(win)
        # 敵描画
        enemy1.draw(win)
        enemy2.draw(win)
        # 画面更新
        pg.display.update()

    # プレイヤー生成
    player = Player(200, 610, 64, 64)
    #敵生成
    enemy1 = Enemy(1500, 610, 64, 64,5, 0)
    enemy2 = Enemy(1400, 610, 64, 64,15, 100)
    #実行を管理する変数
    running = True
    # main loop
    while running:
        # フレームを空ける
        clock.tick(TICK)

        # 衝突判定
        def collision(object1, object2):
            return  object1.hitBox[1] < object2.hitBox[1] + object2.hitBox[3] and \
                    object1.hitBox[1] + object1.hitBox[3] > object2.hitBox[1] and \
                    object1.hitBox[0] + object1.hitBox[2] > object2.hitBox[0] and \
                    object1.hitBox[0] < object2.hitBox[0] + object2.hitBox[2]

        if collision(player, enemy1):
            player.hit()
            break
        if collision(player, enemy2):
            player.hit()
            break

        # ×ボタンでの終了
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        
        # キー入力取得
        keys = pg.key.get_pressed()

        # 左移動
        if keys[pg.K_LEFT] and player.x > player.vel:
            player.x -= player.vel
            player.left = True
            player.right = False
        # 右移動
        elif keys[pg.K_RIGHT] and player.x < WIDTH - player.width - player.vel:
            player.x += player.vel
            player.right = True
            player.left = False
        # 静止
        else:
            player.right = False
            player.left = False
        
        # ジャンプしていないならジャンプができる
        if not (player.isJump):
            if keys[pg.K_UP]:
                player.isJump = True
                player.right = False
                player.left = False
        # ジャンプ中は重力処理
        else:
            if player.jumpCount >= -10:
                neg = 1
                if player.jumpCount < 0:
                    neg = -1
                player.y -= (player.jumpCount ** 2) * 0.5 * neg
                player.jumpCount -= 1
            else:
                player.isJump = False
                player.jumpCount = 10
        
        # 画面更新
        redrawGameWindow()


# ゲーム実行
if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()
    sys.exit()

