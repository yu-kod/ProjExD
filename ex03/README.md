# 第3回
## 迷路ゲーム:迷えるこうかとん(ex03/maze.py)
### ゲーム概要
- ex03/maze.pyを実行すると1500x900のcanvasに迷路が描画され、迷路に沿ってこうかとんを移動させるゲーム
### 操作方法
- 矢印キーでこうかとんを上下左右に移動する
### 追加機能
- マスが市松模様に赤く点滅するようになりました。壁も市松模様の一部として変化し壁として認識出来なくなることで、視認性が下がり難易度が上がっています。]
- 赤いマスにこうかとんが乗るとダメージを受けます。
- HPは画面上部に緑のバーで示されています。
- HPがゼロになるとスタート地点に戻ります。
- 動作が重くならないようにするために、マップを表示するごとに毎回削除するようにしました。
### ToDo
- どこかの処理が悪さをして、実行が長引くと動作が重くなります。(修正しました↑)
- local変数で十分な部分を確認していません。
- ゴール判定
### メモ

