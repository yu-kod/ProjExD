import random


quiz_data = [
    {"question": "サザエさんの旦那の名前は?", "answer": ["マスオ", "ますお"]},
    {"question": "カツオの妹の名前は?", "answer": ["ワカメ", "わかめ"]},
    {"question": "タラオはカツオから見てどんな関係?", "answer": ["甥", "おい", "甥っ子", "おいっこ"]}
]


# ランダムに問題を出題する関数
def shutudai():
    quiz_no = random.randint(0, len(quiz_data))
    print(quiz_data[quiz_no]["question"])
    return quiz_no


# 解答を受け付け評価する関数
def kaitou(quiz_no):
    user_input = input("解答:")
    if user_input in quiz_data[quiz_no]["answer"]:
        print("正解!")
    else:
        print("不正解")


if __name__ == "__main__":
    quiz_no = shutudai()
    kaitou(quiz_no)
