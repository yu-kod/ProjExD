import tkinter as tk
# import tkinter.messagebox as tkm

class App:
    num_flag = False
    def __init__(self, root):
        self.root = root
        root.title("calc")
        root.geometry("300x500")
        root.resizable(width=False, height=False)

        #計算式を表示するlabel
        self.label = tk.Label(root, width=12, text="", font=("", 20))
        self.label.grid(row=0, column=0, columnspan=4)

        # テキスト入力欄追加
        self.entry = tk.Entry(justify="right", width=11, font=("", 40))
        self.entry.grid(row=1, column=0, columnspan=4)

        # 数字ボタン配置
        for i in range(10):
            button = tk.Button(root, text=i, width=5, height=2, font=("", 18))
            button.bind("<1>", self.button_click)
            button.grid(row=(3*7-i) // 3, column=(i-1) % 3)

        
        # 数字以外のボタン追加
        other_button = ["<-", "/", "*", "-", "+", "="]
        for i in range(len(other_button)):
            button = tk.Button(root, text=other_button[i], width=5, height=2, font=("", 18))
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
        if txt == "=":
            self.equal_click(e)
        elif txt == "<-":
            self.delete_one()
        else:
            if App.num_flag == True:
                if self.label["text"] == "":
                    self.label["text"] = self.entry.get() + txt
                else:
                    if txt in ["+", "-", "*", "/"]:
                        self.label["text"] = str(eval(self.label["text"] + self.entry.get())) + txt
                App.num_flag = False
            else:
                if txt in ["+", "-", "*", "/"]:
                    self.label["text"] = self.label["text"][:-1] + txt
    
    def delete_one(self):
        self.entry.delete(len(self.entry.get())-1, tk.END)

    # =ボタンがクリックされたときの動作
    def equal_click(self, e):
        formula = self.label["text"] + self.entry.get()
        ans = eval(formula)
        self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, ans)
        self.label["text"] = ""


def main():
    root = tk.Tk()
    app = App(root)
    app.root.mainloop()

if __name__ == "__main__":
    main()
