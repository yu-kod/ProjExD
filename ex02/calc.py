import tkinter as tk
# import tkinter.messagebox as tkm

class App:
    num_flag = False
    def __init__(self, root):
        self.root = root
        root.title("calc")
        root.geometry("300x500")

        #計算式を表示するlabel
        self.label = tk.Label(root, text="")
        self.label.grid(row=0, column=0, columnspan=4)

        # テキスト入力欄追加
        self.entry = tk.Entry(justify="right", width=10, font=("", 40))
        self.entry.grid(row=1, column=0, columnspan=4)

        # 数字ボタン配置
        for i in range(10):
            button = tk.Button(root, text=i, width=4, height=2, font=("", 15))
            button.bind("<1>", self.button_click)
            button.grid(row=(3*7-i) // 3, column=(i-1) % 3)

        other_button = ["C", "/", "*" , "-", "+", "="]
        # +ボタン追加
        for i in range(len(other_button)):
            button = tk.Button(root, text=other_button[i], width=4, height=2, font=("", 15))
            button.bind("<1>", self.other_click)
            button.grid(row=2+i, column=3)

        # =ボタン追加
        #button = tk.Button(root, text="=", width=4, height=2, font=("", 15))
        #button.bind("<1>", self.equal_click)
        #button.grid(row=5, column=3)

        root.mainloop()
    
    # ボタンがクリックされたときの動作(メッセージボックス表示)
    def button_click(self, e):
        btn = e.widget
        txt = btn["text"]
        if App.num_flag == False:
            self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, txt)
        App.num_flag = True

    def other_click(self, e):
        btn = e.widget
        txt = btn["text"]
        if txt == "=":
            self.equal_click(e)
        else:
            if App.num_flag == True:
                if self.label["text"] == "":
                    self.label["text"] = self.entry.get()
                else:
                    if txt in ["+", "-", "*", "/"]:
                        self.label["text"] = eval(
                            self.label["text"] + txt + self.entry.get())
                App.num_flag = False
            else:
                pass
        

    # =ボタンがクリックされたときの動作
    def equal_click(self, e):
        formula = self.entry.get()
        ans = eval(formula)
        self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, ans)




def main():
    root = tk.Tk()
    app = App(root)
    app.root.mainloop()

if __name__ == "__main__":
    main()
