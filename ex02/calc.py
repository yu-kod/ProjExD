import tkinter as tk

class App:
    num_flag = False         # 記号入力後に数値を入力したか管理する変数(Falseで未入力)
    def __init__(self, root):
        self.root = root
        root.title("calc")
        root.geometry("300x500")
        root.resizable(width=False, height=False)
        root.configure(bg="#CCCCCC")


        #計算式を表示するlabel
        self.label = tk.Label(bg="#CCCCCC", width=12, text="", font=("", 20))
        self.label.grid(row=0, column=0, columnspan=4)


        # テキスト入力欄追加
        self.entry = tk.Entry(
            justify="right", bg="#CCCCCC", bd=1, relief=tk.GROOVE, width=11, font=("", 40))
        self.entry.grid(row=1, column=0, columnspan=4)

        # 数字ボタン配置
        for i in range(10):
            button = tk.Button(root, text=i, bd=1, bg="#CCCCCC", width=5, height=2, relief=tk.GROOVE, font=("", 18))
            button.bind("<1>", self.button_click)
            button.grid(row=(3*7-i) // 3, column=(i-1) % 3)

        
        # 数字以外のボタン追加
        other_button = ["<-", "/", "*", "-", "+", "="]
        for i in range(len(other_button)):
            button = tk.Button(root, text=other_button[i], bd=1, bg="#BBBBBB", width=5, height=2, relief=tk.GROOVE, font=("", 18))
            button.bind("<1>", self.other_click)
            button.grid(row=2+i, column=3)
    

    # 数字ボタンがクリックされたときの動作(メッセージボックス表示)
    def button_click(self, e):
        btn = e.widget
        txt = btn["text"]
        if App.num_flag == False:
            self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, txt)
        App.num_flag = True


    # 数字以外のボタンを押したときの動作
    def other_click(self, e):
        btn = e.widget
        txt = btn["text"]
        if txt == "=":         # 計算が発生しない処理
            self.equal_click() # 答えを出力
        elif txt == "<-":       # 1文字消す
            self.delete_one()
        else:                   #計算が発声する処理
            if App.num_flag == True:  # 新しく数値を入力したなら
                if self.label["text"] == "":
                    self.label["text"] = self.entry.get() + txt     #初期化
                else:
                    if txt in ["+", "-", "*", "/"]:
                        self.label["text"] = self.calc() + txt      #計算
                App.num_flag = False                                #文字入力をFalseに戻す
            else:
                if txt in ["+", "-", "*", "/"]:
                    self.label["text"] = self.label["text"][:-1] + txt # 記号を更新する


    # 計算を行う関数
    def calc(self):
        return str(eval(self.label["text"] + self.entry.get()))


    # 1文字削除する関数
    def delete_one(self):
        self.entry.delete(len(self.entry.get())-1, tk.END)


    # イコールボタンがクリックされたときの動作
    def equal_click(self):
        ans = self.calc()
        self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, ans)
        self.label["text"] = ""
        App.num_flag = True


# メイン関数
def main():
    root = tk.Tk()
    app = App(root)
    app.root.mainloop()


if __name__ == "__main__":
    main()
