from string import ascii_uppercase
from random import sample
from time import time


TEXTNUM = 10    # 生成するアルファベットの個数
ERRCHARNUM = 2  # 欠損するアルファベットの個数
MAXREPEAT = 5   # クイズに回答できる最大回数


# ランダムに問題を出題する関数(引数：無し　戻り値：選択されたクイズの番号)
def shutsudai():
    quiz = sample(ascii_uppercase, TEXTNUM)
    print("対象文字：")
    print(*quiz)

    defect = sample(quiz, ERRCHARNUM)
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
        return False


# 欠損文字を受け付け評価する関数(引数：欠損文字のリスト　戻り値：bool)
def katou_char(kesson):
    user_answers = []
    for i in range(ERRCHARNUM):
        if not (user_input := input(f"{i+1}つ目の文字を入力してください:")) in user_answers:
            user_answers.append(user_input)
    if (set(user_answers) == set(kesson)):
        print("正解です！")
        return True
    else:
        return False


if __name__ == '__main__':
    st = time()
    for i in range(MAXREPEAT):
        kesson = shutsudai()
        if kaitou_num(kesson) and katou_char(kesson):
            break
        else:
            print("不正解です。またチャレンジしてください")
            print("-"*20)
    else:
        print("解答権がなくなりました")
    ed = time()
    print(f"所要時間は{(ed - st):.2f}秒です。")

# (55行目)短絡評価によって、前方がTrueにならないと後方が実行されないため正しく動作する。
