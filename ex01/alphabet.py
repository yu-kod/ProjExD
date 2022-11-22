from string import ascii_uppercase
from random import sample
from datetime import datetime


TEXTNUM = 10    # 生成するアルファベットの個数
ERRCHARNUM = 2  # 欠損するアルファベットの個数
MAXREPEAT = 5   # クイズに回答できる最大回数


# ランダムに問題を出題する関数(引数：無し　戻り値：選択されたクイズの番号)
def shutsudai():
    quiz = sample(ascii_uppercase, TEXTNUM)
    print("対象文字：")
    print(*quiz)

    kesson = sample(quiz, ERRCHARNUM)
    print("欠損文字：")
    print(*kesson)

    hyouji = set(quiz) - set(kesson)
    print("表示文字：")
    print(*hyouji)
    print()
    return kesson


# 欠損文字数を受け付け評価する関数(引数：欠損文字のリスト　戻り値：bool)
def kaitou_num(kesson):
    user_input1 = input("欠損文字はいくつあるでしょうか？：")
    if int(user_input1) == ERRCHARNUM:
        print("正解です。それでは具体的に欠損文字を1つずつ入力してください")
        return True
    else:
        print("不正解です。またチャレンジしてください")
        print("--------------------------------------------------------")
        return False


# 欠損文字を受け付け評価する関数(引数：欠損文字のリスト　戻り値：bool)
def katou_char(kesson):
    user_input2 = input("1つ目の文字を入力してください:")
    user_input3 = input("2つ目の文字を入力してください:")
    if user_input2.upper() in kesson and user_input3.upper() in kesson:
        print("正解です！")
        return True
    else:
        print("不正解です。またチャレンジしてください")
        print("--------------------------------------------------------")
        return False


if __name__ == '__main__':
    st = datetime.now()
    for i in range(5):
        kesson = shutsudai()
        if kaitou_num(kesson) and katou_char(kesson):
            ed = datetime.now()
            print(f"正解までの時間は{(ed - st).seconds}秒です。")
            break
    else:
        print("解答権がなくなりました")

# (57行目)短絡評価によって、前方がTrueにならないと後方が実行されないため正しく動作する。
