import tkinter as tk
import tkinter.messagebox as tkm

class App:

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
            button.grid(row=(15-i) // 3, column=(15-i) % 3)


        # +ボタン追加
        button = tk.Button(root, text="+", width=4, height=2, font=("", 15))
        button.bind("<1>", self.button_click)
        button.grid(row=4, column=3)

        # =ボタン追加
        button = tk.Button(root, text="=", width=4, height=2, font=("", 15))
        button.bind("<1>", self.equal_click)
        button.grid(row=5, column=3)

        root.mainloop()
    
    # ボタンがクリックされたときの動作(メッセージボックス表示)
    def button_click(self, e):
        btn = e.widget
        txt = btn["text"]
        self.entry.insert(tk.END, txt)

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
